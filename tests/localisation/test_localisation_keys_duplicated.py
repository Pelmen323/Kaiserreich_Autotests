##########################
# Find duplicated loc keys
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.generic_test_class import ResultsReporter
from test_classes.localization_class import Localization


def test_localisation_keys_duplicated(test_runner: object):
    loc_keys, duplicated_keys = Localization.get_all_loc_keys(test_runner=test_runner, return_duplicated_keys=True, lowercase=False)

    ResultsReporter.report_results(results=duplicated_keys, message="Duplicated loc keys were encountered.")
