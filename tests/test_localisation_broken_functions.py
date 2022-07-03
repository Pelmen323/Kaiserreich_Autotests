##########################
# Test script to check for various loc syntax issues
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_localisation_files_syntax(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    results = {}
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.lower().split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            current_line_number = line + 2
            if "getheadofgovernment" in current_line:
                results[f'{os.path.basename(filename)}, line {current_line_number}, GetHeadOfGovernment'] = "GetHeadOfGovernment usage (this func is not working)"
            if "getadj]" in current_line:
                results[f'{os.path.basename(filename)}, line {current_line_number}, GetAdj'] = "GetAdj usage - replace with GetAdjective"

    ResultsReporter.report_results(results=results, message="Loc syntax issues were found. Check console output")
