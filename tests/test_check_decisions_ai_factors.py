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
from ..test_classes.generic_test_class import TestClass
import logging
FILES_TO_SKIP = ('00_demobilization_decisions.txt',
                 'ZZ_debug_decisions.txt',
                 'Cyrenaica_decisions.txt',      # Caravans empty decisions
                 'Germany_decisions.txt',        # Empty decisions with modifier
                 'Hunan_decisions.txt',          # Missing icons
                 'Intermarium_decisions.txt',    # 2 non-ai decisions
                 'New_England_decisions.txt',)   # 9 empty decisions


def test_check_decisions_ai_factors(test_runner: object):
    test = TestClass()
    filepath = f'{test_runner.full_path_to_mod}common\\decisions\\'
    results = {}
    os.chdir(filepath)

    for filename in glob.glob("*.txt"):
        if filename in FILES_TO_SKIP:
            continue
        text_file = test.open_text_file(filename).lower()

        icon_counter = len(re.findall('icon =', text_file))
        ai_will_do_counter = len(re.findall('ai_will_do =', text_file))
        missions_counter = len(re.findall('\\bdays_mission_timeout ', text_file))
        selectable_missions_counter = len(re.findall('selectable_mission = yes', text_file))
        expected_num_of_ai_factors = icon_counter - missions_counter + selectable_missions_counter
        if expected_num_of_ai_factors > ai_will_do_counter:
            results[filename] = f'There are more decisions and selectable missions in the file ({expected_num_of_ai_factors}) than ai factors ({ai_will_do_counter})!)'
        elif expected_num_of_ai_factors < ai_will_do_counter:
            results[filename] = f'Huh? We found {ai_will_do_counter} ai factors and only {expected_num_of_ai_factors} selectable decisions and missions. \
                Probably not all decisions have icons or missions that are not selectable have ai factors'

    if results != {}:
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} decisions with issues found.')
        raise AssertionError("Issues with decision ai factors were encountered! Check console output")
