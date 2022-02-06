##########################
# Test script to check for unused oob files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from .imports.file_functions import open_text_file, clear_false_positives_flags
import logging
FALSE_POSITIVES = ('TUN_revolt',    # NFA revolt tags with non-standard syntax
                   'CHA_revolt',
                   'NGR_revolt',
                   'MLI_revolt',
                   'MRT_revolt',
                   'VOL_revolt',
                   'GNA_revolt',
                   'IVO_revolt',
                   'SEN_revolt',
                   'SIE_revolt',)


def test_check_unused_oob_files(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_oob_files = f'{test_runner.full_path_to_mod}history\\units\\'
    oob_files = {}
# Part 1 - get the dict of all oob files
    for filename in glob.iglob(path_to_oob_files + '**/*.txt', recursive=True):
        oob_files[os.path.basename(filename)[:-4]] = 0

# Part 2 - count the number of oob occurrences
    clear_false_positives_flags(flags_dict=oob_files, false_positives=FALSE_POSITIVES)
    logging.debug(f'{len(oob_files)} oob files found')

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        not_encountered_oob = [i for i in oob_files.keys() if oob_files[i] == 0]

        if 'load_oob =' in text_file:
            for file in not_encountered_oob:
                oob_files[file] += text_file.count(f'load_oob = {file}')
                oob_files[file] += text_file.count(f'load_oob = "{file}"')

        elif 'oob =' in text_file:
            for file in not_encountered_oob:
                oob_files[file] += text_file.count(f'oob = "{file}"')
                oob_files[file] += text_file.count(f'set_naval_oob = "{file}"')

# Part 3 - throw the error if oob files are not used
    results = [i for i in oob_files if oob_files[i] == 0]
    if results != []:
        logging.warning("Following oob files are not used:")
        for i in results:
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} unused oob files found.')
        raise AssertionError("Unused oob files were encountered! Check console output")
