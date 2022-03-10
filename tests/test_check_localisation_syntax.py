##########################
# Test script to check for various loc syntax issues
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter


def test_check_localisation_files_syntax(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    results = {}
    loc_keys = {}
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.lower().split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            if "#" not in current_line and [i for i in ['', ' ', 'l_english:'] if i == current_line] == []:
                if [i for i in [':0 "', ':1 "', ':2 "', ':5 "', ':9 "', ': "'] if i in current_line] == []:
                    results[f'{os.path.basename(filename)}, line {line+2}, syntax'] = "Missing key-value syntax"
                if current_line.count('"') < 2 or current_line[-1] != '"':
                    results[f'{os.path.basename(filename)}, line {line+2}, "s'] = "Quotes syntax"
                if '_desc:' not in current_line:
                    loc_keys[current_line.split(':')[0].strip()] = 0

    ResultsReporter.report_results(results=results, message="Loc syntax issues were found. Check console output")
