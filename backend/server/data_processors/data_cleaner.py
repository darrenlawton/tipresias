import re
from typing import Pattern, List
from functools import partial
import pandas as pd

DIGITS: Pattern = re.compile(r"round\s+(\d+)$", flags=re.I)
QUALIFYING: Pattern = re.compile(r"qualifying", flags=re.I)
ELIMINATION: Pattern = re.compile(r"elimination", flags=re.I)
SEMI: Pattern = re.compile(r"semi", flags=re.I)
PRELIMINARY: Pattern = re.compile(r"preliminary", flags=re.I)
GRAND: Pattern = re.compile(r"grand", flags=re.I)
REQUIRED_COLUMNS: List[str] = ["venue", "crowd", "datetime", "season_round"]


class DataCleaner:
    """Clean and format data in preparation of feature engineering.

    Args:
        min_year (integer): Minimum year (inclusive) for match data.
        max_year (integer): Maximum year (inclusive) for match data.
        drop_cols (string, list): Column(s) to drop at the end of transformation.

    Attributes:
        min_year (integer): Minimum year (inclusive) for match data.
        max_year (integer): Maximum year (inclusive) for match data.
        drop_cols (string, list): Column(s) to drop at the end of transformation.
    """

    def __init__(
        self,
        min_year: int = 1,
        max_year: int = 2016,
        drop_cols: List[str] = ["venue", "crowd"],
    ) -> None:
        self.min_year = min_year
        self.max_year = max_year
        self.drop_cols = drop_cols

    def transform(self, data_frame: pd.DataFrame) -> pd.DataFrame:
        """Filter data frame by year, transform round_number & year,
        and drop unneeded columns

        Args:
            data_frame (pandas.DataFrame): Data frame that will be cleaned

        Returns:
            pandas.DataFrame
        """

        if not isinstance(data_frame, pd.DataFrame):
            raise TypeError(
                "Must receive a pandas DataFrame as an argument, "
                f"but got {type(data_frame)} instead."
            )

        if any((req_col not in data_frame.columns for req_col in REQUIRED_COLUMNS)):
            raise ValueError(
                "data_frame argument must have the columns 'venue', "
                "'crowd', 'datetime', 'season_round', but the columns "
                f"given are {data_frame.columns.values}"
            )

        df_copy = data_frame.copy()

        return (
            df_copy[
                (df_copy["datetime"] >= f"{self.min_year}-01-01")
                & (df_copy["datetime"] <= f"{self.max_year}-12-31")
            ]
            .assign(year=self.__extract_year)
            # Need to convert round strings to numbers by year, so has to be in a step
            # after creating the year column
            .assign(round_number=self.__extract_round_number)
            .drop(self.drop_cols + ["datetime", "season_round"], axis=1)
        )

    def __extract_round_number(self, data_frame: pd.DataFrame) -> pd.Series:
        year_groups = data_frame.groupby("year")
        year_series = []

        for _, year_data_frame in year_groups:
            year_season_round = year_data_frame["season_round"]
            round_numbers = year_season_round.str.extract(r"(\d+)", expand=False)
            max_regular_round = pd.to_numeric(round_numbers, errors="coerce").max()

            year_series.append(
                year_season_round.map(partial(self.match_round, max_regular_round))
            )

        return pd.concat(year_series).sort_index()

    @staticmethod
    def match_round(max_regular_round: int, round_string: str) -> int:
        digits = DIGITS.search(round_string)

        if digits is not None:
            return int(digits.group(1))
        if (
            QUALIFYING.search(round_string) is not None
            or ELIMINATION.search(round_string) is not None
        ):
            return max_regular_round + 1
        if SEMI.search(round_string) is not None:
            return max_regular_round + 2
        if PRELIMINARY.search(round_string) is not None:
            return max_regular_round + 3
        if GRAND.search(round_string) is not None:
            return max_regular_round + 4

        raise ValueError(f"Round label {round_string} doesn't match any known patterns")

    @staticmethod
    def __extract_year(data_frame: pd.DataFrame) -> pd.Series:
        return data_frame["datetime"].map(lambda date_time: date_time.year)