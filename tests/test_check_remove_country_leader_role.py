##########################
# Test script to check remove_country_leader_role effect (it consistently causes crashes)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
from ..test_classes.generic_test_class import FileOpener, DataCleaner
import logging


def test_check_remove_country_leader_role(test_runner: object):
    filepath = test_runner.full_path_to_mod
    file_to_skip = f'{filepath}common\\scripted_effects\\_useful_scripted_effects.txt'
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if filename == file_to_skip: continue

        text_file = FileOpener.open_text_file(filename)

        errors_found = text_file.count('remove_country_leader_role')
        if errors_found > 0:
            results[filename] = errors_found

    if results != {}:
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} times "remove_country_leader_role" is used.')
        raise AssertionError("'remove_country_leader_role' usage has been encountered! Check console output")
