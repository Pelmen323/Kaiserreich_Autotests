##########################
# Test script to check remove_country_leader_role effect (it consistently causes crashes)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_remove_country_leader_role(test_runner: object):
    filepath = test_runner.full_path_to_mod
    file_to_skip = f'{filepath}common\\scripted_effects\\_useful_scripted_effects.txt'
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if filename == file_to_skip:
            continue

        text_file = FileOpener.open_text_file(filename)

        errors_found = text_file.count('remove_country_leader_role')
        if errors_found > 0:
            results[filename] = errors_found

    ResultsReporter.report_results(results=results, message="'remove_country_leader_role' usage encountered - don't use it, it causes crashed. Check console output")
