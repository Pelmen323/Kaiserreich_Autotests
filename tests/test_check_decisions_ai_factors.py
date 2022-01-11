##########################
# Test script to check for decisions and selectable without ai factors
# The decisions/missions should have icons set for script to work
# Both missing and excessive ai factors will be reported
# Add files with empty decisions/ missions to files_to_skip
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import glob
import pytest
import re
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\common\\decisions\\"
FILES_TO_SKIP = ('00_demobilization_decisions.txt',
                'ZZ_debug_decisions.txt',
                'Cyrenaica_decisions.txt',      # Caravans empty decisions
                'Germany_decisions.txt',        # Empty decisions with modifier
                'Hunan_decisions.txt',          # Missing icons
                'Intermarium_decisions.txt',    # 2 non-ai decisions
                'New_England_decisions.txt',    # 9 empty decisions
                )


@pytest.mark.parametrize("filepath", [(FILEPATH)])
def test_check_decisions_ai_factors(filepath: str):
    print("Starting the test...")
    results_dict = {}
    os.chdir(filepath)

    for filename in glob.glob("*.txt"):
        if filename in FILES_TO_SKIP:
            continue
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        icon_counter = len(re.findall('icon =', text_file))
        ai_will_do_counter = len(re.findall('ai_will_do =', text_file))
        missions_counter = len(re.findall('\\bdays_mission_timeout ', text_file))
        selectable_missions_counter = len(re.findall('selectable_mission = yes', text_file))
        expected_num_of_ai_factors = icon_counter - missions_counter + selectable_missions_counter
        if expected_num_of_ai_factors > ai_will_do_counter:
            results_dict[filename] = f'There are more decisions and selectable missions in the file ({expected_num_of_ai_factors}) than ai factors ({ai_will_do_counter}). Not all decisions will be available for AI!)'
        elif expected_num_of_ai_factors < ai_will_do_counter:
            results_dict[filename] = f'Huh? We found {ai_will_do_counter} ai factors and only {expected_num_of_ai_factors} selectable decisions and missions. Lets recheck that file... Probably not all decisions have icons or missions that are not selectable have ai factors'

    if results_dict != {}:
        for error in results_dict.items():
            print(error)
        raise AssertionError("Issues were encountered! Check console output")
    print("The test is finished!")
