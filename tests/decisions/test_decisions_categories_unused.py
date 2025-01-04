##########################
# Test script to check for unused decisions categories
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from pathlib import Path

from test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)
from test_classes.decisions_class import Decisions


def test_decisions_categories_unused(test_runner: object):
    dict_decisions_categories = Decisions.get_all_decisions_categories_with_child_decisions(test_runner=test_runner, lowercase=True)
    filepath_to_bop = str(Path(test_runner.full_path_to_mod) / "common" / "bop")
    cats_to_validate = {}

    for cat in dict_decisions_categories:
        if dict_decisions_categories[cat] == []:
            cats_to_validate[cat] = 0

    found_files = False
    for filename in glob.iglob(filepath_to_bop + "**/*.txt", recursive=True):
        found_files = True
        text_file = FileOpener.open_text_file(filename)

        not_encountered_categories = [i for i in cats_to_validate.keys() if cats_to_validate[i] == 0]

        for category in not_encountered_categories:
            if f"decision_category = {category}" in text_file:
                cats_to_validate[category] += 1

    assert found_files, "Bop file extraction failed"
    results = [i for i in cats_to_validate if cats_to_validate[i] == 0]
    ResultsReporter.report_results(results=results, message="Unused decisions categories were encountered.")
