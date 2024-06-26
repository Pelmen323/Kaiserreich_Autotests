##########################
# Test script to check for the presence of brackets in scripted loc
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from data.scripted_localisation_functions import \
    scripted_localisation_functions as test_data_list
from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_localisation_scripted_brackets(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    results = {}
    test_data = [i.lower() for i in test_data_list]
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]

            for function in test_data:
                if function in current_line:
                    num_of_functions_in_line = current_line.count(function)
                    pattern = f'\\[[^\\[]*{function}[a-z]*(?:\\.getsurname)*(?:\\.getfullname)*(?:\\.getshehe)*(?:\\.getshehecap)*(?:\\.getherhim)*(?:\\.getherhimcap)*(?:\\.getherhis)*(?:\\.getherhiscap)*(?:\\.gethershis)*(?:\\.gethershiscap)*(?:\\.getherselfhimself)*(?:\\.getherselfhimselfcap)*\\]'
                    pattern_matches = re.findall(pattern, current_line)
                    if num_of_functions_in_line != len(pattern_matches):
                        results[f'{function}, {os.path.basename(filename)}, line {line+2}'] = current_line

    ResultsReporter.report_results(results=results, message="Scripted loc syntax issues were found. Check console output")
