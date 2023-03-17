##########################
# Test script to check if advisors have duplicated idea tokens
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..test_classes.characters_class import Characters
from ..test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = [
    "chi_dai_chunfeng_sic",
    "chi_dai_chunfeng_political_advisor",
    "qie_liu_menggeng_army_chief",
]


def test_check_advisors_duplicate_idea_tokens(test_runner: object):
    advisors, paths = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
    idea_tokens = []
    results = []

    for adv in advisors:
        if "characters" not in paths[adv]:      # Workaround for advisors from not characters file that can be defined multiple times
            continue
        try:
            token = re.findall("idea_token = (.+)", adv)[0]
        except IndexError:
            results.append((adv, paths[adv], "Advisor with missing idea token encountered"))
            continue
        idea_tokens.append(token)

    duplicated_tokens = sorted(list(set([i for i in idea_tokens if idea_tokens.count(i) > 1])))

    for i in [i for i in duplicated_tokens if i not in FALSE_POSITIVES]:
        results.append((i, "Duplicated advisor token encountered"))

    ResultsReporter.report_results(results=results, message="Advisors with non-unique idea tokens were encountered. Check console output")
