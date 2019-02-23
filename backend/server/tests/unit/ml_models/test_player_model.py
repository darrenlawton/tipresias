from unittest import TestCase
from unittest.mock import Mock
import pandas as pd
from faker import Faker

from project.settings.common import BASE_DIR
from server.ml_models.player_model import PlayerModelData

FAKE = Faker()

get_afltables_stats_df = pd.read_csv(
    f"{BASE_DIR}/server/tests/fixtures/fitzroy_get_afltables_stats.csv"
)
match_results_df = pd.read_csv(
    f"{BASE_DIR}/server/tests/fixtures/fitzroy_match_results.csv"
)
get_afltables_stats_mock = Mock(return_value=get_afltables_stats_df)
match_results_mock = Mock(return_value=match_results_df)


class TestPlayerModelData(TestCase):
    def setUp(self):
        self.data = PlayerModelData(
            data_readers=[get_afltables_stats_mock, match_results_mock]
        )

    def test_train_data(self):
        X_train, y_train = self.data.train_data()

        self.assertIsInstance(X_train, pd.DataFrame)
        self.assertIsInstance(y_train, pd.Series)
        self.assertNotIn("score", X_train.columns)
        self.assertNotIn("oppo_score", X_train.columns)
        self.assertNotIn("goals", X_train.columns)
        self.assertNotIn("oppo_goals", X_train.columns)
        self.assertNotIn("behinds", X_train.columns)
        self.assertNotIn("oppo_behinds", X_train.columns)

        # Applying StandardScaler to integer columns raises a warning
        self.assertFalse(
            any([X_train[column].dtype == int for column in X_train.columns])
        )

    def test_test_data(self):
        X_test, y_test = self.data.test_data()

        self.assertIsInstance(X_test, pd.DataFrame)
        self.assertIsInstance(y_test, pd.Series)
        self.assertNotIn("score", X_test.columns)
        self.assertNotIn("oppo_score", X_test.columns)
        self.assertNotIn("goals", X_test.columns)
        self.assertNotIn("oppo_goals", X_test.columns)
        self.assertNotIn("behinds", X_test.columns)
        self.assertNotIn("oppo_behinds", X_test.columns)

        # Applying StandardScaler to integer columns raises a warning
        self.assertFalse(
            any([X_test[column].dtype == int for column in X_test.columns])
        )

    def test_train_test_data_compatibility(self):
        self.maxDiff = None

        X_train, _ = self.data.train_data()
        X_test, _ = self.data.test_data()

        self.assertCountEqual(list(X_train.columns), list(X_test.columns))
