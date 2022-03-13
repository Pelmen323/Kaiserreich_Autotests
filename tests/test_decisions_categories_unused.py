##########################
# Test script to check for unused decisions categories
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
import logging


def test_check_unused_decisions_categories(test_runner: object):
    filepath_to_decisions = f'{test_runner.full_path_to_mod}common\\decisions\\'
    filepath_to_categories = f'{test_runner.full_path_to_mod}common\\decisions\\categories\\'
    decision_categories = {}
# Part 1 - get the dict of all decision categories
    for filename in glob.iglob(filepath_to_categories + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            pattern_matches = re.findall('^\\w+ =', current_line)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[:-1].strip().lower()
                    decision_categories[match] = 0


# Part 2 - count the number of entity occurrences
    logging.debug(f'{len(decision_categories)} decision categories found')
    for filename in glob.iglob(filepath_to_decisions + '**/*.txt', recursive=True):
        if '\\categories' in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        not_encountered_categories = [i for i in decision_categories.keys() if decision_categories[i] == 0]

        for category in not_encountered_categories:
            if f'{category} = {{' in text_file:
                decision_categories[category] += 1


# Part 3 - throw the error if entity is not used
    results = [i for i in decision_categories if decision_categories[i] == 0]
    ResultsReporter.report_results(results=results, message="Unused decisions categories were encountered. Check console output")