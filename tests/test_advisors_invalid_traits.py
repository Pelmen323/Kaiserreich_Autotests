##########################
# Test script to check for military having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters
import pytest
list_of_trait_types = [
    "air_chief",
    "army_chief",
    "high_command",
    "navy_chief",
    "theorist",
    "political_advisor",
]


@pytest.mark.parametrize("trait_type", list_of_trait_types)
def test_check_advisors_military_invalid_traits(test_runner: object, trait_type):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    advisor_traits = Characters.get_advisors_traits(test_runner=test_runner, trait_type=trait_type, lowercase=True)
    if trait_type == "political_advisor":
        advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\head_of_state.txt')
        advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\USA_head_of_state.txt')
    results = []

    for adv in advisors:
        if adv.count(f'slot = {trait_type}'):
            try:
                advisor_name = re.findall('idea_token = (\\w*)', adv)[0]
            except IndexError:
                results.append((adv, paths[adv], 'Missing idea_token'))
            invalid_trait_syntax = len(re.findall('traits = \\{\\n', adv)) > 0
            one_trait = re.findall('traits = \\{ (\\w*) \\}', adv)
            if invalid_trait_syntax:
                results.append((advisor_name, paths[adv], 'This advisor trait syntax is multiline - single-line syntax is strongly recommended'))
            elif one_trait != []:
                if one_trait[0] not in advisor_traits:
                    results.append((advisor_name, paths[adv], f'Invalid {trait_type} trait encountered - {one_trait[0]}'))
            else:
                results.append((advisor_name, paths[adv], 'This advisor has <1 or >1 traits'))

    ResultsReporter.report_results(results=results, message=f"{trait_type} advisors with invalid traits encountered. Check console output")


def test_check_advisors_sic_invalid_traits(test_runner: object):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    advisor_traits = Characters.get_advisors_traits(test_runner=test_runner, trait_type="second_in_command", lowercase=True)
    results = []

    for adv in advisors:
        if adv.count('slot = second_in_command') > 0:
            try:
                advisor_name = re.findall('idea_token = (\\w*)', adv)[0]
            except IndexError:
                results.append((adv, paths[adv], 'Missing idea_token'))
            invalid_trait_syntax = len(re.findall('traits = \\{\\n', adv)) > 0
            one_trait = re.findall('traits = \\{ (\\w*) \\}', adv)
            two_traits = re.findall('traits = \\{ (\\w*) (\\w*) \\}', adv)
            if invalid_trait_syntax:
                results.append((advisor_name, paths[adv], 'This SIC trait syntax is multiline - single-line syntax is strongly recommended'))
            elif one_trait != []:
                if 'second_in_command_trait' not in one_trait:
                    results.append((advisor_name, paths[adv], 'This SIC is missing second_in_command_trait trait'))
            elif two_traits != []:
                if 'second_in_command_trait' not in two_traits[0]:
                    results.append((advisor_name, paths[adv], 'This SIC is missing second_in_command_trait trait'))
                for trait in two_traits[0]:
                    if trait not in advisor_traits:
                        results.append((advisor_name, paths[adv], f'Invalid SIC trait encountered - {trait}'))

    ResultsReporter.report_results(results=results, message="SIC without second_in_command_trait trait encountered. Check console output")
