##########################
# Test script to check for event targets that are cleared but not set
# By Pelmen, https://github.com/Pelmen323
##########################
import os
from test_classes.generic_test_class import ResultsReporter
from test_classes.event_targets import Event_Targets


def test_check_cleared_event_targets(test_runner: object):
    results = []
    cleared_targers, paths = Event_Targets.get_all_cleared_targets(test_runner=test_runner, lowercase=True, return_paths=True)
    set_targets = Event_Targets.get_all_set_targets(test_runner=test_runner, lowercase=True)

    for i in cleared_targers:
        if i not in set_targets:
            results.append(f"{i:<55}{os.path.basename(paths[i])}")

    ResultsReporter.report_results(results=results, message="Cleared event targets that are not set were encountered.")
