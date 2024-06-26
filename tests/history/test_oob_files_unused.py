##########################
# Test script to check for unused oob files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os

from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ('tun_revolt',    # NFA revolt tags with non-standard syntax
                   'cha_revolt',
                   'ngr_revolt',
                   'mli_revolt',
                   'mrt_revolt',
                   'vol_revolt',
                   'gna_revolt',
                   'ivo_revolt',
                   'sen_revolt',
                   'sie_revolt',)


def test_check_unused_oob_files(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_oob_files = f'{test_runner.full_path_to_mod}history\\units\\'
    oob_files = {}
# Part 1 - get the dict of all oob files
    for filename in glob.iglob(path_to_oob_files + '**/*.txt', recursive=True):
        oob_files[os.path.basename(filename.lower())[:-4]] = 0

# Part 2 - count the number of oob occurrences
    oob_files = DataCleaner.clear_false_positives(input_iter=oob_files, false_positives=FALSE_POSITIVES)
    logging.debug(f'{len(oob_files)} oob files found')

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        not_encountered_oob = [i for i in oob_files.keys() if oob_files[i] == 0]

        if 'oob =' in text_file:
            for file in not_encountered_oob:
                oob_files[file] += text_file.count(f'oob = {file}')
                oob_files[file] += text_file.count(f'oob = "{file}"')

# Part 3 - throw the error if oob files are not used
    results = [i for i in oob_files if oob_files[i] == 0]
    ResultsReporter.report_results(results=results, message="Unused oob files were found. Check console output")
