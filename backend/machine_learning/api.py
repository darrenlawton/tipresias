from typing import List, Optional, Dict, Tuple
import os
from datetime import date
from functools import partial
import itertools

import pandas as pd
from sklearn.externals import joblib
from mypy_extensions import TypedDict

from machine_learning.ml_data import JoinedMLData, BaseMLData
from machine_learning.ml_estimators import BaseMLEstimator
from machine_learning.data_import import FitzroyDataImporter
from machine_learning.data_transformation.data_cleaning import (
    clean_match_data,
    clean_fixture_data,
)
from machine_learning.settings import ML_MODELS, BASE_DIR
from machine_learning.data_config import TEAM_NAMES, DEFUNCT_TEAM_NAMES, VENUES


PredictionData = TypedDict(
    "PredictionData",
    {
        "team": str,
        "year": int,
        "round_number": int,
        "at_home": int,
        "oppo_team": str,
        "ml_model": str,
        "predicted_margin": float,
    },
)

MlModel = TypedDict("MlModel", {"name": str, "filepath": str})

DataConfig = TypedDict(
    "DataConfig",
    {"team_names": List[str], "defunct_team_names": List[str], "venues": List[str]},
)

# We calculate rolling sums/means for some features that can span over 5 seasons
# of data, so we're setting it to 10 to be on the safe side.
N_SEASONS_FOR_PREDICTION = 10
# We want to limit the amount of data loaded as much as possible,
# because we only need the full data set for model training and data analysis,
# and we want to limit memory usage and speed up data processing for tipping
PREDICTION_DATA_START_DATE = f"{date.today().year - N_SEASONS_FOR_PREDICTION}-01-01"


def _train_model(ml_model: BaseMLEstimator, data: BaseMLData) -> BaseMLEstimator:
    X_train, y_train = data.train_data()

    # On the off chance that we try to run predictions for years that have no relevant
    # prediction data
    if X_train.empty or y_train.empty:
        raise ValueError(
            "Some required data was missing for training for year range "
            f"{data.train_years}.\n"
            f"{'X_train is empty' if X_train.empty else ''}"
            f"{'and ' if X_train.empty and y_train.empty else ''}"
            f"{'y_train is empty' if y_train.empty else ''}"
        )

    ml_model.fit(X_train, y_train)

    return ml_model


def _make_model_predictions(
    year: int,
    data: BaseMLData,
    ml_model: Dict[str, str],
    round_number: Optional[int] = None,
    verbose=1,
    train=False,
) -> pd.DataFrame:
    if verbose == 1:
        print(f"Making predictions with {ml_model['name']}")

    loaded_model = joblib.load(os.path.join(BASE_DIR, ml_model["filepath"]))
    data.train_years = (None, year - 1)
    data.test_years = (year, year)

    trained_model = _train_model(loaded_model, data) if train else loaded_model

    X_test, _ = data.test_data(test_round=round_number)

    if not X_test.any().any():
        raise ValueError(
            "X_test doesn't have any rows, likely due to some data for the "
            "upcoming round not being available yet."
        )

    y_pred = trained_model.predict(X_test)

    data_row_slice = (slice(None), year, slice(round_number, round_number))

    return (
        data.data.loc[data_row_slice, :]
        .assign(predicted_margin=y_pred, ml_model=ml_model["name"])
        .set_index("ml_model", append=True, drop=False)
        .loc[
            :,
            [
                "team",
                "year",
                "round_number",
                "oppo_team",
                "at_home",
                "ml_model",
                "predicted_margin",
            ],
        ]
    )


def _make_predictions_by_year(
    year: int,
    data: BaseMLData,
    ml_models: List[Dict[str, str]],
    round_number: Optional[int] = None,
    verbose=1,
    train=False,
) -> pd.DataFrame:
    partial_make_model_predictions = partial(
        _make_model_predictions,
        year,
        data,
        round_number=round_number,
        verbose=verbose,
        train=train,
    )

    return [partial_make_model_predictions(ml_model) for ml_model in ml_models]


def make_predictions(
    year_range: Tuple[int, int],
    round_number: Optional[int] = None,
    data: BaseMLData = JoinedMLData(
        fetch_data=True, start_date=PREDICTION_DATA_START_DATE
    ),
    ml_models: List[Dict[str, str]] = ML_MODELS,
    verbose=1,
    train=False,
) -> List[PredictionData]:
    partial_make_predictions_by_year = partial(
        _make_predictions_by_year,
        data,
        ml_models,
        round_number=round_number,
        verbose=verbose,
        train=train,
    )

    predictions = [
        partial_make_predictions_by_year(year) for year in range(*year_range)
    ]

    return pd.concat(list(itertools.chain.from_iterable(predictions))).to_dict(
        "records"
    )


def fetch_fixture_data(
    start_date: str, end_date: str, data_import=FitzroyDataImporter(), verbose: int = 1
) -> pd.DataFrame:
    """
    Fetch fixture data (doesn't include match results) from afl_data service.

    Args:
        start_date (str): Stringified date of form yyy-mm-dd that determines
            the earliest date for which to fetch data.
        end_date (str): Stringified date of form yyy-mm-dd that determines
            the latest date for which to fetch data.
        verbose (0 or 1): Whether to print info messages while fetching data.

    Returns:
        List of fixture data dictionaries.
    """

    data_import.verbose = verbose

    return (
        data_import.fetch_fixtures(start_date=start_date, end_date=end_date)
        .pipe(clean_fixture_data)
        .to_dict("records")
    )


def fetch_match_results_data(
    start_date: str,
    end_date: str,
    fetch_data: bool = False,
    data_import=FitzroyDataImporter(),
    verbose: int = 1,
) -> pd.DataFrame:
    """
    Fetch results data for past matches from afl_data service.

    Args:
        start_date (str): Stringified date of form yyy-mm-dd that determines
            the earliest date for which to fetch data.
        end_date (str): Stringified date of form yyy-mm-dd that determines
            the latest date for which to fetch data.
        fetch_data (bool): Whether to fetch fresh data or use saved data
            (usually a few weeks old).
        verbose (0 or 1): Whether to print info messages while fetching data.

    Returns:
        List of match results data dictionaries.
    """

    data_import.verbose = verbose

    return (
        data_import.match_results(
            start_date=start_date, end_date=end_date, fetch_data=fetch_data
        )
        .pipe(clean_match_data)
        .to_dict("records")
    )


def fetch_ml_model_info() -> List[MlModel]:
    """Fetch general info about all saved ML models"""

    return ML_MODELS


def fetch_data_config() -> DataConfig:
    return {
        "team_names": TEAM_NAMES,
        "defunct_team_names": DEFUNCT_TEAM_NAMES,
        "venues": VENUES,
    }