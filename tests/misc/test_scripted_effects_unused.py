##########################
# Test script to check if there are scripted effects that are not used via "xxx = yes"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob

from test_classes.scripted_effects_class import ScriptedEffects, ScriptedEffectFactory
from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)


FALSE_POSITIVES = [
    # 'add_core_and_transfer_if_owned_else_add_claim',
    # 'add_research_slot_until_six',
    # 'ant_setpr_leaders',
    # 'china_autonomy_level_up',
    # 'clear_air_chief',
    # 'clear_embargo_from',
    # 'clear_navy_chief',
    # 'clear_relations_with_prev',
    # 'clear_sabotaged_resources_if_necesary',
    # 'clear_week_flags',
    'cwtools_dummy_effect',
    # 'day_of_week_flag',
    # 'decrease_state_category_by_one_level',
    # 'destroy_all_ships',
    # 'disband_fifty_percent_units',
    # 'fng_nupop',
    # 'fng_zppop',
    # 'fra_transfer_internationale_leader',
    # 'generate_generic_military_advisors_low_level',
    # 'get_day_of_week',
    # 'leap_year_check',
    # 'lec_american_fall',
    # 'log_rp_eastern_military',
    # 'modulo_date_check',
    # 'occupy_huge_country',
    # 'puppet_country_without_changing_government',
    # 'puppet_country_without_changing_government_from',
    # 'reduce_conscription_to_disarmed',
    # 'reduce_conscription_to_volunteer',
    # 'temporarily_disable_country_annexation',
    # 'transfer_all_unit_leaders_to_root',
    # 'transfer_and_occupy_state_annexation',
    # 'transfer_control_during_war',
    # 'add_core_if_owned_else_add_claim',
]


def test_check_scripted_effects_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    effects = ScriptedEffects.get_all_scripted_effects(test_runner=test_runner, lowercase=True)
    effects_names = [ScriptedEffectFactory(i).id for i in effects]
    dict_with_scripted_effects = {i: 0 for i in effects_names}
    dict_with_scripted_effects = DataCleaner.clear_false_positives(input_iter=dict_with_scripted_effects, false_positives=FALSE_POSITIVES)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_effects = [i for i in dict_with_scripted_effects.keys() if dict_with_scripted_effects[i] == 0]
        if ' = yes' in text_file:
            for key in not_encountered_effects:
                if f'{key} = yes' in text_file:
                    dict_with_scripted_effects[key] += 1

    results = [i for i in dict_with_scripted_effects.keys() if dict_with_scripted_effects[i] == 0 and "#" not in i]
    ResultsReporter.report_results(results=results, message="Unused scripted effects were encountered.")
