##########################
# Test script to check for duplicated decisions categories
# By Pelmen, https://github.com/Pelmen323
# Deprecated - replaced with assert check in decisions class
##########################
import glob
import logging
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_duplicated_decisions_categories(test_runner: object):
    filepath_to_categories = f"{test_runner.full_path_to_mod}common\\decisions\\categories\\"
    decision_categories = []
    # 1. get the dict of all decision categories
    for filename in glob.iglob(filepath_to_categories + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split("\n")[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            pattern_matches = re.findall(r"^\w+ =", current_line)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[:-1].strip().lower()
                    decision_categories.append(match)

    logging.debug(f"{len(decision_categories)} decision categories found")

    # 2. throw the error if entity is duplicated
    results = [i for i in decision_categories if decision_categories.count(i) > 1]
    ResultsReporter.report_results(results=results, message="Duplicated decisions categories were encountered.")
