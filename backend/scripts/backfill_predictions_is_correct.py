"""
One-off script for backfilling is_correct values in the predictions data table
"""

import os
import sys

import django

PROJECT_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), "../"))

if PROJECT_PATH not in sys.path:
    sys.path.append(PROJECT_PATH)

django.setup()

from server.models import Prediction


def main():
    for prediction in Prediction.objects.select_related(
        "match", "predicted_winner"
    ).all():
        prediction.is_correct = Prediction.calculate_whether_correct(
            prediction.match, prediction.predicted_winner
        )
        prediction.save()


if __name__ == "__main__":
    main()
