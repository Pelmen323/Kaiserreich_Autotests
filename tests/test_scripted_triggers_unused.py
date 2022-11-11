##########################
# Test script to check if there are scripted triggers that are not used via "xxx = yes" or "xxx = no"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FILES_TO_SKIP = ['diplomacy_scripted_triggers',
                 'diplo_action_valid_triggers', '00_resistance']
FALSE_POSITIVES = ['ai_is_naval_invader_trigger',
                   'aus_has_habsburgs',
                   'owned_by_austria_or_puppet2',
                   'is_ger_or_ally',
                   'is_controlled_by_ger_or_ally',
                   'is_owned_by_ger_or_ally',
                   'nee_is_supporting_an_american_faction',
                   'nee_backed_faction_is_alive',
                   'nee_backed_faction_has_won',
                   'yun_has_federalist_government',
                   'yun_has_lkmt_government',
                   'yun_has_unaligned_government',
                   'is_clear_other_claims',
                   'totalist_plurality',
                   'syndicalist_plurality',
                   'radical_socialist_plurality',
                   'social_liberal_plurality',
                   'state_same_continent_as_state_from',
                   'is_portugal',
                   'is_scandinavia',
                   'is_northern_china',
                   'is_eastern_china',
                   'is_southern_china',
                   'is_in_americas',
                   'state_same_continent_as_root',
                   'is_arab_tag',
                   'is_yiddish_tag',
                   'is_actual_major_without_exceptions',
                   'is_owned_by_root_or_war_ally',
                   'has_specialist_level_trigger',
                   'has_expert_level_trigger',
                   'has_genius_level_trigger',
                   'has_enough_reserve_manpower_per_battalion',
                   'will_have_right_democratic_government',
                   'will_have_left_democratic_government',
                   'will_have_any_authoritarian_government',
                   'is_second_in_command',
                   'has_free_political_advisor_slot',
                   'has_two_political_advisors',
                   'has_any_political_advisor',
                   'has_dlc_bftb',
                   'is_in_coalition_with_totalist',
                   'is_in_coalition_with_syndicalist',
                   'is_in_coalition_with_radical_socialist',
                   'is_in_coalition_with_social_democrat',
                   'is_in_coalition_with_social_liberal',
                   'is_in_coalition_with_market_liberal',
                   'is_in_coalition_with_social_conservative',
                   'is_in_coalition_with_paternal_autocrat',
                   'is_in_coalition_with_national_populist',
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
