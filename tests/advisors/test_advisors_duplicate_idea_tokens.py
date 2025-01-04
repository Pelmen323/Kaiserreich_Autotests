##########################
# Test script to check if advisors have duplicated idea tokens
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.characters_class import Characters
from test_classes.generic_test_class import ResultsReporter


def test_advisors_duplicate_idea_tokens(test_runner: object):
    characters = Characters.get_all_characters(test_runner=test_runner, return_paths=False)
    pattern_advisor = re.compile(r"^(\t*?)advisor = \{(.*?^)\1\}", flags=re.DOTALL | re.MULTILINE)
    pattern_token = re.compile(r"idea_token = \b(.*)\b")
    idea_tokens = []
    results = []

    for char in characters:
        advisor_roles = pattern_advisor.findall(char)

        # Skipping instanced characters as they can share tokens
        if "instance" in char:
            continue

        if len(advisor_roles) > 0:
            for i in advisor_roles:
                advisor_code = i[1]
                token = pattern_token.findall(advisor_code)[0]
                idea_tokens.append(token)

    duplicated_tokens = sorted(list(set([i for i in idea_tokens if idea_tokens.count(i) > 1])))
    for i in [i for i in duplicated_tokens]:
        results.append((i, "Duplicated advisor token encountered"))

    ResultsReporter.report_results(results=results, message="Advisors with non-unique idea tokens were encountered. They should always have a unique token")
