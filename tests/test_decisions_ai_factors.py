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
from ..test_classes.generic_test_class import FileOpener, ResultsReporter
FILES_TO_SKIP = ('00 demobilization decisions.txt',
                 'ZZ debug decisions.txt',
                 'LBA decisions (Cyrenaica).txt',      # Caravans empty decisions
                 'GER decisions (Germany).txt',        # Empty decisions with modifier
                 'HNN decisions (Hunan).txt',          # Missing icons
                 '01 Intermarium decisions.txt',    # 2 non-ai decisions
                 'NEE decisions (New England).txt',)   # 9 empty decisions


def test_check_decisions_ai_factors(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}common\\decisions\\'
    results = {}
    os.chdir(filepath)

    for filename in glob.glob("*.txt"):
        if filename in FILES_TO_SKIP:
            continue
        text_file = FileOpener.open_text_file(filename)

        icon_counter = len(re.findall('icon =', text_file))
        ai_will_do_counter = len(re.findall('ai_will_do =', text_file))
        missions_counter = len(re.findall('\\bdays_mission_timeout ', text_file))
        selectable_missions_counter = len(re.findall('selectable_mission = yes', text_file))
        advisors_ai_factors_counter = len(re.findall('\\badvisor = \\{', text_file))
        expected_num_of_ai_factors = icon_counter - missions_counter + selectable_missions_counter + advisors_ai_factors_counter
        if expected_num_of_ai_factors > ai_will_do_counter:
            results[filename] = f'There are more decisions and selectable missions in the file ({expected_num_of_ai_factors}) than ai factors ({ai_will_do_counter})!)'
        elif expected_num_of_ai_factors < ai_will_do_counter:
            results[filename] = f'Huh? We found {ai_will_do_counter} ai factors and only {expected_num_of_ai_factors} selectable decisions and missions. \
                Probably not all decisions have icons or missions that are not selectable have ai factors'

    ResultsReporter.report_results(results=results, message="Issues with decisions AI factors encountered - either not all decisions have icons or not all decisions have AI factors. Check console output")