##########################
# Find duplicated loc keys
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.generic_test_class import ResultsReporter
from test_classes.localization_class import Localization
from collections import Counter


def test_localisation_keys_duplicated(test_runner: object):
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False)
    loc_keys_2 = {key:loc_keys[key] for key in loc_keys if "STATE_" in key or "VICTORY_POINTS_" in key and key[-1].isdigit()}
    values = loc_keys_2.values()
    counts = Counter(values)
    results = sorted([i for i in counts if counts[i] > 1])

    ResultsReporter.report_results(results=results, message="Duplicated loc keys were encountered.")
