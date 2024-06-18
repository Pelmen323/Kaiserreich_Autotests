##########################
# Test script to check if scripted loc is unused
# By Pelmen, https://github.com/Pelmen323
##########################
import glob

from ...test_classes.generic_test_class import FileOpener, ResultsReporter
from ...test_classes.scripted_loc_class import Scripted_localisation

FALSE_POSITIVES = (
    "getsecondincommand",
    "getrulingideologycolour",
    "gethavengaorhertzog",
)


def test_check_localisation_scripted_brackets(test_runner: object):
    scripted_loc, paths = Scripted_localisation.get_scripted_loc_names(test_runner=test_runner, lowercase=True, return_paths=True)
    filepath = test_runner.full_path_to_mod
    results = {i: 0 for i in scripted_loc}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_results = [i for i in results if results[i] == 0]
        for loc in not_encountered_results:
            if f'{loc}]' in text_file:
                results[loc] += 1
            elif f'{loc}|' in text_file:
                results[loc] += 1

    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_results = [i for i in results if results[i] == 0]
        for loc in not_encountered_results:
            if f'{loc}]' in text_file:
                results[loc] += 1

    for filename in glob.iglob(filepath + '**/*.gui', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_results = [i for i in results if results[i] == 0]
        for loc in not_encountered_results:
            if loc in text_file:
                results[loc] += 1

    results = [i for i in results if results[i] == 0 and i not in FALSE_POSITIVES]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused scripted loc was found. Check console output")
