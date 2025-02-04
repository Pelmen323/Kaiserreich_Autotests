##########################
# Test script to check for checks of advisor ideas instead of checking character roles
# Too brittle - it's safer to use the is_<role> = yes checks instead
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import ResultsReporter, FileOpener


def test_advisors_direct_token_check(test_runner: object):
    filepath = test_runner.full_path_to_mod
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    pattern = re.compile(r"has_idea = \S*")
    found_files = False
    results = []
    advisor_tokens = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        advisor_tokens.append(adv.token)

    advisor_tokens = set(advisor_tokens)
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        found_files = True
        text_file = FileOpener.open_text_file(filename)

        if "has_idea =" in text_file:
            # Reduces execution time by 90% compared to searching just in text_file
            all_has_idea_matches = pattern.findall(text_file)
            for i in advisor_tokens:
                if f"has_idea = {i}" in all_has_idea_matches:
                    results.append(f"{i} - {os.path.basename(filename)}")

    assert found_files, f"No .txt files found matching pattern: {filepath}"
    ResultsReporter.report_results(results=results, message="Advisor token is checked directly. Use character checks, like `has_advisor_role`, instead")
