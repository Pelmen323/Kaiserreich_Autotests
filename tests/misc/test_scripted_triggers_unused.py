##########################
# Test script to check if there are scripted triggers that are not used via "xxx = yes" or "xxx = no"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ...test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FILES_TO_SKIP = ['diplomacy_scripted_triggers',
                 'diplo_action_valid_triggers',
                 '00_resistance',
                 '_renaming_scripted_triggers',
                 '_useful_scripted_triggers',
                 '_government_scripted_triggers',
                 '_on_action_scripted_triggers',
                 '_region_scripted_triggers',
                 '_dlc_scripted_triggers',
                 '_ideology_plurality_scripted_triggers',
                 '_character_scripted_triggers',
                 '_annexation_scripted_triggers',
                 'AI_scripted_triggers']
FALSE_POSITIVES = [
    'is_controlled_by_ger_or_ally',
    'is_owned_by_ger_or_ally',
    'spa_spr_swf_has_fervor_idea',
    'owned_by_austria_or_puppet2',
    'yun_has_federalist_government',
    'yun_has_unaligned_government'
]


def test_check_scripted_triggers_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_effects = f'{test_runner.full_path_to_mod}common\\scripted_triggers\\'
    dict_with_scripted_triggers = {}
    paths = {}
    # 1. Get the dict of all scripted effects
    for filename in glob.iglob(filepath_to_effects + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue

        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line - 1]
            pattern_matches = re.findall(
                '^[a-zA-Z0-9_\\.]* = \\{', current_line)
            if len(pattern_matches) > 0:
                match = pattern_matches[0][:-4].strip()
                dict_with_scripted_triggers[match] = 0
                paths[match] = os.path.basename(filename)

    # 2. Find if scripted effects are used:
    dict_with_scripted_triggers = DataCleaner.clear_false_positives(
        input_iter=dict_with_scripted_triggers, false_positives=FALSE_POSITIVES)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_triggers = [i for i in dict_with_scripted_triggers.keys() if dict_with_scripted_triggers[i] == 0]
        if ' = yes' in text_file or ' = no' in text_file:
            for key in not_encountered_triggers:
                if f'{key} = yes' in text_file:
                    dict_with_scripted_triggers[key] += 1
                if f'{key} = no' in text_file:
                    dict_with_scripted_triggers[key] += 1

    results = [i for i in dict_with_scripted_triggers.keys() if dict_with_scripted_triggers[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused scripted triggers were encountered. Check console output")
