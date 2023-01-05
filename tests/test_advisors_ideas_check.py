##########################
# Test script to check for checks of advisor ideas instead of checking character roles
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from ..test_classes.characters_class import Advisors, Characters
from ..test_classes.generic_test_class import ResultsReporter, FileOpener


def test_advisors_ideas_check(test_runner: object):
    filepath = test_runner.full_path_to_mod
    advisors = Characters.get_all_advisors(test_runner=test_runner)
    results = []
    advisor_tokens = []

    for advisor_code in advisors:
        adv = Advisors(adv=advisor_code)
        advisor_tokens.append(adv.token)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "has_idea =" in text_file:
            for i in advisor_tokens:
                if f"has_idea = {i}" in text_file:
                    results.append(f"{i} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Issues with advisors were encountered. Check console output")
