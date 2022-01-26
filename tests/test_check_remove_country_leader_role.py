##########################
# Test script to check remove_country_leader_role effect (it consistently causes crashes)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
from .imports.decorators import util_decorator_no_false_positives
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FILES_TO_SKIP = ('common\\scripted_effects\\_useful_scripted_effects.txt')


@pytest.mark.parametrize("filepath", [(FILEPATH)])
@util_decorator_no_false_positives
def test_check_remove_country_leader_role(filepath: str):
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if filename == f"{FILEPATH}{FILES_TO_SKIP}":
            continue
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        errors_found = text_file.count('remove_country_leader_role')
        if errors_found > 0:
            results[filename] = errors_found

    if results != {}:
        for i in results.items():
            print(f'- [ ] {i}')
        print(f'{len(results)} times "remove_country_leader_role" is used.')
        raise AssertionError("'remove_country_leader_role' usage has been encountered! Check console output")
