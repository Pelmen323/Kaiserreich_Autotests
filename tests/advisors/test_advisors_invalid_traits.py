##########################
# Test script to check for military having invalid traits
# By Pelmen, https://github.com/Pelmen323
##########################
import pytest
import glob
from pathlib import Path

from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import ResultsReporter

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
def test_advisors_invalid_traits(test_runner: object, trait_type):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    allowed_advisor_traits = Characters.get_advisors_traits(test_runner=test_runner, trait_type=trait_type, lowercase=True)
    if trait_type in ["political_advisor", "second_in_command"]:
        base_path = Path(test_runner.full_path_to_mod) / "common" / "country_leader"
        path1 = str(base_path / '**head_of_state.txt')
        path2 = str(base_path / '**political_advisor_traits.txt')
        for filename in glob.iglob(path1):
            allowed_advisor_traits += Characters.get_advisors_traits(
                test_runner=test_runner,
                lowercase=True,
                path=filename
            )
        for filename in glob.iglob(path2):
            allowed_advisor_traits += Characters.get_advisors_traits(
                test_runner=test_runner,
                lowercase=True,
                path=filename
            )

    results = []
    assert len(allowed_advisor_traits) > 0, "Allowed advisor traits list is empty"

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        if adv.slot == trait_type:
            if adv.traits != []:
                for trait in adv.traits:
                    if trait not in allowed_advisor_traits:
                        results.append(f'{adv.token} - {paths[advisor_code]} - invalid {trait_type} trait encountered - {trait}')

            else:
                results.append(f'{adv.token} - {paths[advisor_code]} - This advisor has < 1 traits')

    ResultsReporter.report_results(results=results, message=f"{trait_type} advisors with invalid traits encountered, they should use 'class-specific' traits")
