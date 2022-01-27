##########################
# Test script to check remove_all_country_leader_roles effect (it consistently causes crashes)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from .imports.file_functions import open_text_file


def test_check_remove_all_country_leader_roles(test_runner: object):
    filepath = test_runner.full_path_to_mod
    file_to_skip = f'{filepath}common\\scripted_effects\\_useful_scripted_effects.txt'
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if filename == file_to_skip:
            continue
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        errors_found = text_file.count('remove_all_country_leader_roles')
        if errors_found > 0:
            results[filename] = errors_found

    if results != {}:
        for i in results.items():
            print(f'- [ ] {i}')
        print(f'{len(results)} times "remove_all_country_leader_roles" is used.')
        raise AssertionError("'remove_all_country_leader_roles' usage has been encountered! Check console output")
