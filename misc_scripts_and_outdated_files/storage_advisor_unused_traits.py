import glob
import re

from ..test_classes.characters_class import Advisors, Characters
from ..test_classes.generic_test_class import ResultsReporter, FileOpener


list_of_trait_types = [
    "political_advisor",
    "second_in_command",
]


def test_check_unused_traits(test_runner: object):
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    allowed_advisor_traits = []
    for i in list_of_trait_types:
        allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, trait_type=i, lowercase=True)

    allowed_advisor_traits += Characters.get_advisors_traits(test_runner=test_runner, lowercase=True, path=f'{test_runner.full_path_to_mod}common\\country_leader\\FNG_political_advisor_traits.txt')
    results = []
    potential_results = {}
    used_advisors_traits_list = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        for i in adv.traits:
            used_advisors_traits_list.append(i)

    for trait in allowed_advisor_traits:
        # if len([i for i in used_advisors_traits_list if i == trait]) == 1:
        #     results.append(f'Trait {trait} is used only once')

        if len([i for i in used_advisors_traits_list if i == trait]) == 0:
            potential_results[trait] = 0

    filepath = test_runner.full_path_to_mod
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        list_to_search = [i for i in potential_results.keys() if potential_results[i] == 0]

        for trait in list_to_search:
            pattern = "add_trait = \\{[^}]*?trait = "+trait+"[^}]*?\\}"
            pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                potential_results[trait] += 1

    results = [i for i in potential_results.keys() if potential_results[i] == 0]
    ResultsReporter.report_results(results=results, message="Unused advisor traits found. Check console output")
