from unittest.mock import Mock, patch
from django.test import TestCase
from sklearn.externals import joblib

from server.models import Match, TeamMatch, Team, MLModel, Prediction
from server.management.commands import seed_db
from server.tests.fixtures.data_factories import (
    fake_footywire_fixture_data,
    fake_footywire_betting_data,
)
from machine_learning.ml_data import BettingMLData
from machine_learning.tests.fixtures import TestEstimator


MATCH_COUNT_PER_YEAR = 5


class TestSeedDb(TestCase):
    def setUp(self):
        joblib.dump = Mock()

        min_seed_year = int(seed_db.YEAR_RANGE.split("-")[0])
        # Min year needs to be greather than 2010, or weird stuff can happen
        # due to betting data only going back to 2010
        self.assertGreater(min_seed_year, 2010)

        # We only need a couple of valid years to test functionality
        self.years = (int(min_seed_year), int(min_seed_year + 2))
        # Need to add extra year at the beginning to provide at least one year's worth
        # of training data
        data_years = (self.years[0] - 1, self.years[1])

        # Mock footywire fixture data
        self.fixture_data_frame = fake_footywire_fixture_data(
            MATCH_COUNT_PER_YEAR, data_years
        )
        self.betting_data_frame = fake_footywire_betting_data(
            MATCH_COUNT_PER_YEAR, data_years
        )

        with patch(
            "machine_learning.ml_data.betting_ml_data.FootywireDataImporter"
        ) as MockDataReader:
            MockDataReader.return_value.get_fixture = Mock(
                side_effect=self.__fixture_side_effect
            )
            MockDataReader.return_value.get_betting_odds = Mock(
                side_effect=self.__betting_side_effect
            )

            self.seed_command = seed_db.Command(
                estimators=[TestEstimator()],
                data_reader=MockDataReader(),
                data=BettingMLData(),
            )

    def test_handle(self):
        with patch(
            "machine_learning.ml_data.betting_ml_data.FootywireDataImporter"
        ) as MockDataReader:
            MockDataReader.return_value.get_fixture = Mock(
                side_effect=self.__fixture_side_effect
            )
            MockDataReader.return_value.get_betting_odds = Mock(
                side_effect=self.__betting_side_effect
            )

            self.seed_command.handle(
                year_range=f"{self.years[0]}-{self.years[1]}", verbose=0
            )

        self.assertGreater(Team.objects.count(), 0)
        self.assertEqual(MLModel.objects.count(), 1)
        self.assertEqual(
            Match.objects.count(), MATCH_COUNT_PER_YEAR * len(range(*self.years))
        )
        self.assertEqual(
            TeamMatch.objects.count(),
            MATCH_COUNT_PER_YEAR * len(range(*self.years)) * 2,
        )
        self.assertEqual(
            Prediction.objects.count(), MATCH_COUNT_PER_YEAR * len(range(*self.years))
        )
        self.assertEqual(TeamMatch.objects.filter(score=0).count(), 0)

    def test_handle_errors(self):
        with self.subTest(
            "with invalid year_range argument due to it being a single year"
        ):
            with self.assertRaises(ValueError):
                self.seed_command.handle(year_range="2015", verbose=0)

        with self.subTest(
            "with invalid year_range argument due to years being separated by an invalid symbol"
        ):
            for symbol in [".", "_", ",", "/", "|"]:
                with self.assertRaises(ValueError):
                    self.seed_command.handle(
                        year_range=f"{self.years[0]}{symbol}{self.years[1]}", verbose=0
                    )

    def __fixture_side_effect(
        self, year_range=None, fetch_data=False
    ):  # pylint: disable=W0613
        if year_range is None:
            return self.fixture_data_frame

        return self.fixture_data_frame.query(
            "season >= @year_range[0] & season < @year_range[1]"
        )

    def __betting_side_effect(
        self, year_range=None, fetch_data=False
    ):  # pylint: disable=W0613
        if year_range is None:
            return self.betting_data_frame

        return self.betting_data_frame.query(
            "season >= @year_range[0] & season < @year_range[1]"
        )

    @staticmethod
    def __clear_db():
        Team.objects.all().delete()
        Match.objects.all().delete()
        MLModel.objects.all().delete()
