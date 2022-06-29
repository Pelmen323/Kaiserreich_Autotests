##########################
# Test script to check if equipment modifiers have instant application
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.characters_class import Characters
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.ideas_class import Ideas


def test_equipment_bonus_without_instant_application(test_runner: object):
    results = []

    ideas, paths = Ideas.get_all_ideas(test_runner=test_runner, lowercase=True, return_paths=True, include_country_ideas=True, include_manufacturers=False, include_laws=True, include_army_spirits=True)
    for idea in ideas:
        if "equipment_bonus = {" in idea:
            if 'instant = yes' not in idea:
                results.append((idea.replace('\t', '').replace('\n', '  '), paths[idea]))

    advisors_traits = []
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="air_chief")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="army_chief")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="high_command")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="navy_chief")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="theorist")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="political_advisor")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, trait_type="second_in_command")
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\head_of_state.txt')
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\USA_head_of_state.txt')
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\RUS_head_of_state.txt')
    advisors_traits += Characters.get_advisors_traits_code(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\FNG_political_advisor_traits.txt')
    for trait in advisors_traits:
        if "equipment_bonus = {" in trait:
            if 'instant = yes' not in trait:
                results.append((trait.replace('\t', '').replace('\n', '  ')))

# Part 2 - throw the error if those combinations are encountered
    ResultsReporter.report_results(results=results, message="Equipment bonuses without instant = yes were encountered. Check console output")
