##########################
# Test script to check for decisions and selectable without ai factors
# The decisions/missions should have icons set for script to work
# Both missing and excessive ai factors will be reported
# Add files with empty decisions/ missions to files_to_skip
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import glob
import re
from ..imports.file_functions import open_text_file
import logging


def test_check_armor_chassis_bonuses_syntax(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}common\\ideas\\'
    results = {}
    os.chdir(filepath)
# Part 1 - Check ideas files
    for filename in glob.glob("*.txt"):
        text_file = open_text_file(filename)

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
            text_file = open_text_file(filename)
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
    if results != {}:
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} violations of armor modifiers syntax encountered.')
        raise AssertionError("Issues with armor modifiers were encountered! Check console output")
