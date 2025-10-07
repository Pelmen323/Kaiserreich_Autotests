##########################
# Test script to check for event targets that are not used
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from test_classes.event_targets import Event_Targets
from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ["wca_usa_floyd_olson", "wca_usa_al_smith", "target_value"]


def test_unused_event_targets(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    potential_results = []
    set_targets, paths = Event_Targets.get_all_set_targets(test_runner=test_runner, lowercase=True, return_paths=True)
    used_targets = Event_Targets.get_all_used_targets(test_runner=test_runner, lowercase=True)
    set_targets = DataCleaner.clear_false_positives_partial_match(set_targets, FALSE_POSITIVES)

    for i in set_targets:
        if i not in used_targets:
            potential_results.append(i)

    # Additionally checking yml files for loc functions
    targets_used_in_loc = []
    for filename in glob.iglob(filepath + "**/*.yml", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if ".get" in text_file:
            not_encountered_targets = [i for i in potential_results if i not in targets_used_in_loc]
            for target in not_encountered_targets:
                if f"[{target}.getname" in text_file or f"[{target}.getadjective" in text_file:
                    targets_used_in_loc.append(target)

    for i in potential_results:
        if i not in targets_used_in_loc:
            results.append(f"{i:<55} {os.path.basename(paths[i])}")

    ResultsReporter.report_results(results=results, message="Unused event targets were encountered.")
