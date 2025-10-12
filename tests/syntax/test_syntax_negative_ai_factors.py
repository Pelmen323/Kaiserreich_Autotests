##########################
# Test script to check if negative ai factors are used
# factor means multiplication, multiplying a value with negative value is not what you want in 99% of the cases
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os

from test_classes.generic_test_class import FileOpener, ResultsReporter

FALSE_POSITIVES = [
    "generic_leader_abilities",
    "_mtth",
]


def test_check_negative_ai_factors(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if any([i for i in FALSE_POSITIVES if i in filename]):
            continue
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split("\n")
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line - 1]
            if "\tfactor = -" in current_line:
                current_line = current_line.strip("\t")
                results.append(f"{os.path.basename(filename):<45}line {line:<20}{current_line}")

    ResultsReporter.report_results(
        results=results, message="Negative factors are found, factor means multiplication, multiplying a value with negative value is not what you want in 99% of the cases."
    )
