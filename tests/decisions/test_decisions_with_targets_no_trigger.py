##########################
# Test script to check for decisions that have targets but no target trigger (they instead check available/visible which are hourly checks)
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = [
    "usa_develop_ally",
]


def test_decisions_with_tartets_no_trigger(test_runner: object):
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for i in decisions:
        decision = DecisionsFactory(dec=i)
        if decision.token in FALSE_POSITIVES:
            continue

        if decision.targets or decision.target_array:
            if not decision.target_trigger:
                results.append(f"{decision.token:<55}{paths[i]:<55}")

    ResultsReporter.report_results(
        results=results, message="Decisions with targets but no target trigger are found. This means available and visible will be checked instead, which is many times worse in terms of performance."
    )
