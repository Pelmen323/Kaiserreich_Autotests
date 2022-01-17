##########################
# Test script to check remove_all_country_leader_roles effect (it consistently causes crashes)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FILES_TO_SKIP = ('_useful_scripted_effects.txt')


@pytest.mark.parametrize("filepath", [(FILEPATH)])
def test_check_remove_all_country_leader_roles(filepath: str):
    print("Starting the test...")
    results_dict = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        errors_found = text_file.count('remove_all_country_leader_roles')
        if errors_found > 0:
            results_dict[filename] = errors_found

    if results_dict != {}:
        for error in results_dict.items():
            print(error)
        raise AssertionError("'remove_all_country_leader_roles' usage has been encountered! Check console output")
    print("The test is finished!")
