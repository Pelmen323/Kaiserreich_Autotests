##########################
# Test script to check if there are scripted triggers that are not used via "xxx = yes" or "xxx = no"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.scripted_triggers_class import ScriptedTriggers
from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)

FILES_TO_SKIP = [
    'Annexation triggers',
    '00_diplo',
    '00_resistance',
]
# FALSE_POSITIVES = [
#     'is_controlled_by_ger_or_ally',
#     'is_owned_by_ger_or_ally',
#     'spa_spr_swf_has_fervor_idea',
#     'owned_by_austria_or_puppet2',
#     'yun_has_federalist_government',
#     'yun_has_unaligned_government'
# ]


def test_check_scripted_triggers_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    scripted_triggers = set(ScriptedTriggers.get_all_scripted_triggers_names(test_runner=test_runner, skip_system_triggers=True, exclude_files=FILES_TO_SKIP))

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
