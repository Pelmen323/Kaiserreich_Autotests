##########################
# Test script to check for the presence of brackets in scripted loc
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_localisation_brackets(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "localisation") + "/"
    results = []
    for filename in glob.iglob(filepath + "**/*.yml", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split("\n")[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]

            bracket1 = current_line.count("[")
            bracket2 = current_line.count("]")
            if bracket1 != bracket2:
                results.append(f"{os.path.basename(filename)} - line {line+2} - unpaired bracket")

    ResultsReporter.report_results(results=results, message="Unpaired brackets were found in loc")
