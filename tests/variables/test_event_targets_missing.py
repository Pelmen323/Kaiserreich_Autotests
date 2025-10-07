##########################
# Test script to check for event targets that are used but not set
# By Pelmen, https://github.com/Pelmen323
##########################
import os
from test_classes.generic_test_class import ResultsReporter, DataCleaner
from test_classes.event_targets import Event_Targets

FALSE_POSITIVES = ['.']


def test_missing_event_targets(test_runner: object):
    results = []
    used_targets, paths = Event_Targets.get_all_used_targets(test_runner=test_runner, lowercase=True, return_paths=True)
    set_targets = Event_Targets.get_all_set_targets(test_runner=test_runner, lowercase=True)
    used_targets = DataCleaner.clear_false_positives_partial_match(used_targets, FALSE_POSITIVES)

    for i in used_targets:
        if i not in set_targets:
            results.append(f"{i:<55}{os.path.basename(paths[i])}")

    ResultsReporter.report_results(results=results, message="Used event targets that are not set were encountered.")
