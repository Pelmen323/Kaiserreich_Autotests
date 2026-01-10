##########################
# Test script to check duplicated scripted loc
# By Pelmen, https://github.com/Pelmen323
##########################
from collections import Counter

from test_classes.scripted_loc_class import ScriptedLocalisation
from test_classes.generic_test_class import ResultsReporter


def test_scripted_loc_duplicated(test_runner: object):
    all_loc_names = ScriptedLocalisation.get_all_scripted_loc_names(test_runner=test_runner)
    all_loc_counter = Counter(all_loc_names)
    results = [i for i in all_loc_counter if all_loc_counter[i] > 1]

    ResultsReporter.report_results(results=results, message="Duplicated scripted loc found.")
