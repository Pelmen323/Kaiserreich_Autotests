##########################
# Test script to check for unused oob files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from ..test_classes.generic_test_class import TestClass
import logging
FALSE_POSITIVES = ('[oob_name]',)


def test_check_unused_oob_files(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    path_to_oob_files = f'{test_runner.full_path_to_mod}history\\units\\'
    oob_files = {}
# Part 1 - get the dict of oob usages in files
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = test.open_text_file(filename)

        if 'oob =' in text_file:
            pattern_matches = re.findall('oob = [\\[\\]a-zA-Z0-9_"]*', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[5:].strip().strip('"')
                    oob_files[match] = 0

        if 'OOB =' in text_file:
            pattern_matches2 = re.findall('oob = [\\[\\]a-zA-Z0-9_"]*', text_file)
            if len(pattern_matches2) > 0:
                for match in pattern_matches2:
                    match = match[5:].strip().strip('"')
                    oob_files[match] = 0

# Part 2 - find if oob file is present
    oob_files = test.clear_false_positives_dict(input_dict=oob_files, false_positives=FALSE_POSITIVES)
    logging.debug(f'{len(oob_files)} unique usages of oob files found')

    for filename in glob.iglob(path_to_oob_files + '**/*.txt', recursive=True):
        for oob in oob_files:
            if oob == os.path.basename(filename.lower())[:-4]:
                oob_files[oob] += 1

# Part 3 - throw the error if oob file is not found
    results = [i for i in oob_files if oob_files[i] == 0]
    if results != []:
        logging.warning("Following oob files are missing:")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} missing oob files found.')
        raise AssertionError("Missing oob files were encountered! Check console output")
