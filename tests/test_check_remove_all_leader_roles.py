##########################
# Test script to check remove_all_country_leader_roles effect (it consistently causes crashes)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
from timeit import default_timer as timer
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FILES_TO_SKIP = ('common\\scripted_effects\\_useful_scripted_effects.txt')


@pytest.mark.parametrize("filepath", [(FILEPATH)])
def test_check_remove_all_country_leader_roles(filepath: str):
    print("The test is started. Please wait...")
    start = timer()
    results_dict = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if filename == f"{FILEPATH}{FILES_TO_SKIP}":
            continue
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
    end = timer()
    print(f"The test is finished in {round(end-start, 3)} seconds!")
