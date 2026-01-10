##########################
# Test script to check if there are scripted triggers that are not used via "xxx = yes" or "xxx = no"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.scripted_triggers_class import ScriptedTriggers
from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FILES_TO_SKIP = [
    'Annexation triggers',
    '00_diplo',
    '00_resistance',
]
FALSE_POSITIVES = [
    'gea_can_send_volunteers_to_target',
    'maf_can_send_volunteers_to_target',
]


def test_scripted_triggers_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    scripted_triggers = ScriptedTriggers.get_all_scripted_triggers_names(test_runner=test_runner, skip_system_triggers=True, exclude_files=FILES_TO_SKIP)
    scripted_triggers = set(DataCleaner.clear_false_positives(scripted_triggers, FALSE_POSITIVES))

    potential_match_pattern = re.compile(r'(\w+)\s*=\s*(yes|no)')

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if not scripted_triggers:
            break

        text_file = FileOpener.open_text_file(filename)
        if ' = yes' not in text_file and ' = no' not in text_file:
            continue

        for key, _ in potential_match_pattern.findall(text_file):
            if key in scripted_triggers:
                scripted_triggers.remove(key)

    results = sorted(scripted_triggers)
    ResultsReporter.report_results(results=results, message="Unused scripted triggers were encountered.")
