##########################
# Test script to check for military having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters, Advisors
import pytest
list_of_trait_types = [
    "air_chief",
    "army_chief",
    "high_command",
    "navy_chief",
    "theorist",
    "political_advisor",
    "second_in_command",
]


@pytest.mark.parametrize("trait_type", list_of_trait_types)
def test_check_advisors_military_invalid_traits(test_runner: object, trait_type):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    allowed_advisor_traits = Characters.get_advisors_traits(test_runner=test_runner, trait_type=trait_type, lowercase=True)
    if trait_type == "political_advisor":
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\head_of_state.txt')
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\USA_head_of_state.txt')
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        if adv.slot == trait_type:
            if adv.traits == []:
                results.append((adv.token, paths[advisor_code], 'This advisor trait syntax is multiline - single-line syntax is strongly recommended'))
                continue

            if not adv.sic_role:
                if len(adv.traits) == 1:
                    found_trait = ''.join(adv.traits)
                    if found_trait not in allowed_advisor_traits:
                        results.append((adv.token, paths[advisor_code], f'Invalid {trait_type} trait encountered - {found_trait}'))
                else:
                    results.append((adv.token, paths[advisor_code], 'This advisor has < 1 or > 1 traits'))

            elif adv.sic_role:
                if len(adv.traits) == 2:
                    if 'second_in_command_trait' not in adv.traits:
                        results.append((adv.token, paths[advisor_code], 'This SIC is missing second_in_command_trait trait'))
                    for trait in adv.traits:
                        if trait not in allowed_advisor_traits:
                            results.append((adv.token, paths[advisor_code], f'Invalid SIC trait encountered - {trait}'))
                else:
                    results.append((adv.token, paths[advisor_code], 'This SIC has < 2 or > 2 traits'))

            else:
                results.append((adv.token, paths[advisor_code], 'Huh?'))

    ResultsReporter.report_results(results=results, message=f"{trait_type} advisors with invalid traits encountered. Check console output")
