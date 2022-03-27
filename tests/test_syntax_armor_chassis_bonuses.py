##########################
# Test script to check for outdated armor bonuses syntax
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import glob
import re
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
import logging


def test_check_armor_chassis_bonuses_syntax(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}common\\ideas\\'
    results = {}
    os.chdir(filepath)
# Part 1 - Check ideas files
    for filename in glob.glob("*.txt"):
        text_file = FileOpener.open_text_file(filename)

        if '_tank_' in text_file:
            pattern_matches = re.findall('[^\t]*_tank.*_equipment', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'anti_tank_equipment' not in match:
                        results[filename] = match

# Part 2 - Check country leader files
    filepath = f'{test_runner.full_path_to_mod}common\\country_leader\\'
    os.chdir(filepath)

    for filename in glob.glob("*.txt"):
        try:
            text_file = FileOpener.open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        if '_tank_' in text_file:
            pattern_matches = re.findall('[^\t]*_tank.*_equipment', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if 'anti_tank_equipment' not in match:
                        results[filename] = match

# Report the results
    ResultsReporter.report_results(results=results, message="Outdated armor bonuses were encountered. Check console output")
