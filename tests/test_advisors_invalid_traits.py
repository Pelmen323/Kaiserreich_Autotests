##########################
# Test script to check for military having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import pytest

from ..test_classes.characters_class import Advisors, Characters
from ..test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = [
    "pap_eugenio_pacelli_sic",
    "asy_malik_qambar_political_advisor_lar",
    "irq_hashim_al_alawi_political_advisor_lar",
    "chi_dai_chunfeng_political_advisor",
]
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
    if trait_type in ["political_advisor", "second_in_command"]:
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\head_of_state.txt')
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\USA_head_of_state.txt')
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\RUS_head_of_state.txt')
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\FNG_political_advisor_traits.txt')
    results = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)

        # Skip false positives
        if adv.token in FALSE_POSITIVES:
            continue

        if adv.slot == trait_type:
            if adv.traits == []:
                results.append((adv.token, paths[advisor_code], 'This advisor trait syntax is multiline - single-line syntax is strongly recommended'))
                continue

            if "kr_head_of_intelligence" in adv.traits and "has_dlc_lar = yes" not in advisor_code:
                results.append((adv.token, paths[advisor_code], "Head of intelligence doesn't have LaR check"))

            if len(adv.traits) < 1:
                results.append((adv.token, paths[advisor_code], 'This advisor has < 1 traits'))

            elif len(adv.traits) == 1:
                found_trait = ''.join(adv.traits)
                if found_trait not in allowed_advisor_traits:
                    results.append((adv.token, paths[advisor_code], f'Invalid {trait_type} trait encountered - {found_trait}'))

            elif len(adv.traits) > 1:
                for trait in adv.traits:
                    if trait not in allowed_advisor_traits:
                        results.append((adv.token, paths[advisor_code], f'Invalid {trait_type} trait encountered - {trait}'))

            else:
                results.append((adv.token, paths[advisor_code], 'Huh?'))

    ResultsReporter.report_results(results=results, message=f"{trait_type} advisors with invalid traits encountered. Check console output")
