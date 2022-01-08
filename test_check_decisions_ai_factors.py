import os
import glob
import pytest
import re
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\common\\decisions\\"
FILES_TO_SKIP = ('00_demobilization_decisions.txt', 'ZZ_debug_decisions.txt')

@pytest.mark.parametrize("filepath", [(FILEPATH)])
def test_check_decisions_ai_factors(filepath: str):
    print("Starting the test...")
    results_dict = {}
    try:
        os.chdir(filepath)
    except Exception:
        print("Unable to open the folder")

    for file in glob.glob("*.txt"):
        if file in FILES_TO_SKIP:
            continue
        try:
            with open(file, 'r', encoding='utf-8-sig') as text_file:
                text_file = text_file.read()
        except Exception as ex:
            print(f'Skipping the file {file}')
            print(ex)
            continue

        icon_counter = len(re.findall('icon =', text_file))
        ai_will_do_counter = len(re.findall('ai_will_do =', text_file))
        missions_counter = len(re.findall('\\bdays_mission_timeout ', text_file))
        selectable_missions_counter = len(re.findall('selectable_mission = yes', text_file))
        expected_num_of_ai_factors = icon_counter - missions_counter + selectable_missions_counter
        if expected_num_of_ai_factors > ai_will_do_counter:
            results_dict[file] = f'There are more decisions and selectable missions in the file ({expected_num_of_ai_factors}) than ai factors ({ai_will_do_counter}). Not all decisions will be available for AI!)'
        elif expected_num_of_ai_factors < ai_will_do_counter:
            results_dict[file] = f'Huh? We found {ai_will_do_counter} ai factors and only {expected_num_of_ai_factors} selectable decisions and missions. Lets recheck that file... Probably not all decisions have icons'

    if results_dict != {}:
        for error in results_dict.items():
            print(error)
        raise AssertionError("Issues were encountered! Check console output")
    print("The test is finished!")
