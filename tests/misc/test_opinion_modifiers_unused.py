##########################
# Test script to check if there are opinion modifiers that are not used via "modifier = xx"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FILES_TO_SKIP = ["Vanilla_Opinion_Modifiers"]
FALSE_POSITIVES = ("kr_deal_with_devil", "aided_cntfai", "aided_carlist", "aided_spain",)


def test_check_opinion_modifiers_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_modifiers = f'{test_runner.full_path_to_mod}common\\opinion_modifiers\\'
    dict_with_modifiers = {}
    paths = {}
    # 1. Get the dict of all modifiers
    for filename in glob.iglob(filepath_to_modifiers + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line - 1]
            pattern_matches = re.findall('^\t[a-zA-Z0-9_\\.]* = \\{', current_line)
            if len(pattern_matches) > 0:
                match = pattern_matches[0][:-4].strip('\t').strip()
                dict_with_modifiers[match] = 0
                paths[match] = os.path.basename(filename)

    # 2. Find if modifiers are used:
    dict_with_modifiers = DataCleaner.clear_false_positives(input_iter=dict_with_modifiers, false_positives=FALSE_POSITIVES)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_modifiers = [i for i in dict_with_modifiers.keys() if dict_with_modifiers[i] == 0]
        if 'modifier =' in text_file:
            for key in not_encountered_modifiers:
                if f'modifier = {key}' in text_file:
                    dict_with_modifiers[key] += 1

    results = [i for i in dict_with_modifiers.keys() if dict_with_modifiers[i] == 0]
    ResultsReporter.report_results(results=results, paths=paths, message="Unused opinion modifiers were found.")
