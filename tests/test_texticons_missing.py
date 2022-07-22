##########################
# Test script to check for missing texticons
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_missing_texticons(test_runner: object):
    filepath_to_loc = f'{test_runner.full_path_to_mod}localisation\\'
    texticons_kr = f'{test_runner.full_path_to_mod}interface\\'
    texticons_vanilla = 'C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV\\interface\\'
    texticons = []
    results = {}

    # Get list of all texticons
    for path in [texticons_kr, texticons_vanilla]:
        for filename in glob.iglob(path + '**/*.gfx', recursive=True):
            text_file = FileOpener.open_text_file(filename)

            matches = re.findall('name = \\"(gfx_.*)\\"', text_file)
            for match in matches:
                texticons.append(match)

    for filename in glob.iglob(filepath_to_loc + '**/*.yml', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.lower().split('\n')[1:]
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line]
            current_line_number = line + 2

            if "£" in current_line:                                                            # 1. Get all texticon usages in yml files
                texticon_matches = re.findall("£[^ \\n]+?\\b", current_line)
                if len(texticon_matches) > 0:
                    for icon in texticon_matches:
                        icon = icon[1:]                                                         # 2. Cut £
                        if icon not in texticons and f'gfx_{icon}' not in texticons:
                            results[f'{os.path.basename(filename)}, line {current_line_number}'] = icon

    ResultsReporter.report_results(results=results, message="Missing texticons were found. Check console output")
