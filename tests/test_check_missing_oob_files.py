##########################
# Test script to check for unused oob files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re
from .imports.file_functions import open_text_file, clear_false_positives_flags
import logging
FALSE_POSITIVES = ('[OOB_NAME]',)


def test_check_unused_oob_files(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_oob_files = f'{test_runner.full_path_to_mod}history\\units\\'
    oob_files = {}
# Part 1 - get the dict of oob usages in files
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        if 'oob =' in text_file:
            oob_invoked_file2 = re.findall('oob = [\\[\\]a-zA-Z0-9_"]*', text_file)
            if len(oob_invoked_file2) > 0:
                for oob in oob_invoked_file2:
                    oob = oob[5:]
                    oob = oob.strip().strip('"')
                    oob_files[oob] = 0

        if 'OOB =' in text_file:
            oob_invoked_file2 = re.findall('oob = [\\[\\]a-zA-Z0-9_"]*', text_file)
            if len(oob_invoked_file2) > 0:
                for oob in oob_invoked_file2:
                    oob = oob[5:]
                    oob = oob.strip().strip('"')
                    oob_files[oob] = 0

# Part 2 - find if oob file is present
    clear_false_positives_flags(flags_dict=oob_files, false_positives=FALSE_POSITIVES)
    logging.debug(f'{len(oob_files)} unique usages of oob files found')

    for filename in glob.iglob(path_to_oob_files + '**/*.txt', recursive=True):
        for oob in oob_files:
            if oob == os.path.basename(filename)[:-4]:
                oob_files[oob] += 1

# Part 3 - throw the error if oob file is not found
    results = [i for i in oob_files if oob_files[i] == 0]
    if results != []:
        logging.warning("Following oob files are missing:")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} missing oob files found.')
        raise AssertionError("Missing oob files were encountered! Check console output")
