##########################
# Test script to check for duplicated decisions
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.decisions_class import Decisions
from test_classes.generic_test_class import ResultsReporter


def test_decisions_duplicated(test_runner: object):
    # 1. get the dict of all decisions
    decisions = Decisions.get_all_decisions_names(test_runner=test_runner, lowercase=True)

    # 2. throw the error if entity is duplicated
    results = [i for i in decisions if decisions.count(i) > 1]
    ResultsReporter.report_results(results=results, message="Duplicated decisions were encountered.")
