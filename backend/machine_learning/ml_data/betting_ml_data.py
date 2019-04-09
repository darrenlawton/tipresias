"""Module with wrapper class for Lasso model and its associated data class"""

from typing import List, Callable
import pandas as pd

from machine_learning.types import DataFrameTransformer, YearPair
from machine_learning.data_processors import TeamDataStacker, FeatureBuilder, OppoFeatureBuilder
from machine_learning.data_readers import FootywireDataReader
from machine_learning.data_processors.feature_functions import (
    add_result,
    add_cum_percent,
    add_cum_win_points,
    add_ladder_position,
    add_win_streak,
    add_betting_pred_win,
    add_shifted_team_features,
)
from machine_learning.data_processors.feature_calculation import (
    feature_calculator,
    calculate_rolling_rate,
)
from machine_learning.ml_data import BaseMLData
from machine_learning.data_config import TEAM_TRANSLATIONS, INDEX_COLS
from machine_learning.utils import DataTransformerMixin


FEATURE_FUNCS: List[DataFrameTransformer] = [
    add_result,
    add_shifted_team_features(shift_columns=["score", "oppo_score", "result"]),
    add_cum_win_points,
    add_betting_pred_win,
    add_win_streak,
    feature_calculator([(calculate_rolling_rate, [("betting_pred_win",)])]),
]
REQUIRED_COLS: List[str] = ["year", "score", "oppo_score"]
DATA_TRANSFORMERS: List[DataFrameTransformer] = [
    TeamDataStacker().transform,
    FeatureBuilder(feature_funcs=FEATURE_FUNCS).transform,
    OppoFeatureBuilder(
        match_cols=[
            "year",
            "score",
            "oppo_score",
            "round_number",
            "team",
            "at_home",
            "line_odds",
            "oppo_line_odds",
            "win_odds",
            "oppo_win_odds",
            "oppo_team",
        ]
    ).transform,
    # Features dependent on oppo columns
    FeatureBuilder(feature_funcs=[add_cum_percent, add_ladder_position]).transform,
]

MODEL_ESTIMATORS = ()


class BettingMLData(BaseMLData, DataTransformerMixin):
    """Load and clean betting data"""

    def __init__(
        self,
        data_readers: List[Callable] = [],
        data_transformers: List[DataFrameTransformer] = DATA_TRANSFORMERS,
        train_years: YearPair = (None, 2015),
        test_years: YearPair = (2016, 2016),
        index_cols: List[str] = INDEX_COLS,
        fetch_data: bool = False,
    ) -> None:
        super().__init__(
            train_years=train_years, test_years=test_years, fetch_data=fetch_data
        )

        if any(data_readers):
            self.data_readers = data_readers
        else:
            self.data_readers = [
                FootywireDataReader().get_betting_odds,
                FootywireDataReader().get_fixture,
            ]

        self._data_transformers = data_transformers

        data_frame = self.__concated_data_input.rename(
            columns={"season": "year", "round": "round_number"}
        ).drop(
            [
                "crowd",
                "home_win_paid",
                "home_line_paid",
                "away_win_paid",
                "away_line_paid",
            ],
            axis=1,
        )

        self._data = (
            self._compose_transformers(data_frame)  # pylint: disable=E1102
            .astype({"year": int})
            .fillna(0)
            .set_index(index_cols, drop=False)
            .rename_axis([None] * len(index_cols))
            .sort_index()
        )

    @property
    def data(self):
        return self._data

    @property
    def data_transformers(self):
        return self._data_transformers

    @property
    def __concated_data_input(self) -> pd.DataFrame:
        betting_data = (
            self.data_readers[0](fetch_data=self.fetch_data)
            .drop(
                [
                    "date",
                    "venue",
                    "round_label",
                    "home_score",
                    "home_margin",
                    "away_score",
                    "away_margin",
                ],
                axis=1,
            )
            .assign(
                home_team=lambda df: df["home_team"].map(
                    self.__map_betting_teams_to_match_teams
                ),
                away_team=lambda df: df["away_team"].map(
                    self.__map_betting_teams_to_match_teams
                ),
            )
        )
        match_data = self.data_readers[1](fetch_data=self.fetch_data).drop(
            ["date", "venue", "round_label"], axis=1
        )

        return betting_data.merge(
            match_data, on=["home_team", "away_team", "round", "season"]
        )

    @staticmethod
    def __map_betting_teams_to_match_teams(team_name: str) -> str:
        if team_name in TEAM_TRANSLATIONS.keys():
            return TEAM_TRANSLATIONS[team_name]

        return team_name
