##########################
# Test script to check if there are scripted effects that are not used via "xxx = yes"
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

FALSE_POSITIVES = [
    'generate_generic_sics_and_activate',
    'destroy_all_ships',
    'decrease_state_category_by_one_level',
    'gain_random_agency_upgrade',
    'lec_american_fall',
    'clear_sabotaged_resources_if_necesary',
    'reduce_conscription_to_volunteer',
    'reduce_conscription_to_disarmed',
    'decrease_mobilisation',
    'disband_fifty_percent_units',
    'ant_setpr_leaders',
    'create_snp_right',
    'fng_nupop',
    'fng_zppop',
    'gal_characters_join_ukraine_immediate',
    'clear_relations_with_prev',
    'generate_generic_military_advisors_low_level',
    'remove_civilian_advisor_roles',
    'remove_military_advisor_roles',
    'log_rp_eastern_military',
    'transfer_control_during_war',
    'puppet_country_without_changing_government',
    'puppet_country_without_changing_government_from',
    'clear_army_chief',
    'clear_navy_chief',
    'clear_air_chief',
    'remove_all_ai_templates',
    'occupy_huge_country',
    'prioritize_state',
    'add_one_random_civilian_factory',
    'add_one_random_military_factory',
    'add_one_random_dockyard',
    'add_one_random_synthetic_refinery',
    'add_one_random_fuel_silo',
    'remove_current_second_in_command',
    'occupy_state_temporary',
    'transfer_and_occupy_state_temporary',
    'clear_occupy_state',
    'remove_puppet_and_leave_faction',
    'fra_transfer_internationale_leader',
    'cwtools_dummy_effect',
    'add_research_slot_until_six',
    'remove_cores_of_dead_tags',
    'transfer_all_unit_leaders_to_root',
    'china_autonomy_level_up',
]


def test_check_scripted_effects_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_effects = f'{test_runner.full_path_to_mod}common\\scripted_effects\\'
    dict_with_scripted_effects = {}
    paths = {}

    # 1. Get the dict of all scripted effects
    for filename in glob.iglob(filepath_to_effects + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        text_file_splitted = text_file.split('\n')
        for line in text_file_splitted:
            match = re.findall('^([a-zA-Z0-9_\\.]*) = \\{', line)
            if len(match) > 0:
                dict_with_scripted_effects[match[0]] = 0
                paths[match[0]] = os.path.basename(filename)

    # 2. Find if scripted effects are used:
    dict_with_scripted_effects = DataCleaner.clear_false_positives(input_iter=dict_with_scripted_effects, false_positives=FALSE_POSITIVES)
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_effects = [i for i in dict_with_scripted_effects.keys() if dict_with_scripted_effects[i] == 0]
        if ' = yes' in text_file:
            for key in not_encountered_effects:
                if f'{key} = yes' in text_file:
                    dict_with_scripted_effects[key] += 1

    results = [i for i in dict_with_scripted_effects.keys() if dict_with_scripted_effects[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused scripted effects were encountered. Check console output")
