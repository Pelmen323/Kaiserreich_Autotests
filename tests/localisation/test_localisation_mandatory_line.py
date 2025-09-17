##########################
# Test script to check if loc line has mandatory 'l_xxx:' line
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_localisation_mandatory_line(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}localisation\\'
    results = []
    for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename).split('\n')
        if text_file == [""]:                                                       # Empty file
            continue
        text_file = [i for i in text_file if "#" not in i]                          # Exclude comments
        if text_file[0] != "l_english:" and "play_in_english" not in filename:
            results.append(os.path.basename(filename))

    ResultsReporter.report_results(results=results, message="l_xxx: line is absent in localisation file.")
