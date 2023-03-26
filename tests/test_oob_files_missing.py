##########################
# Test script to check for unused oob files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import logging
import os
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = ('[oob_name]',)


def test_check_missing_oob_files(test_runner: object):
    filepath = test_runner.full_path_to_mod
    path_to_oob_files = f'{test_runner.full_path_to_mod}history\\units\\'
    oob_files = {}
# Part 1 - get the dict of oob usages in files
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'oob =' in text_file:
            pattern_matches = re.findall('^[^#]+oob = ([\\[\\]a-zA-Z0-9_"]*)', text_file, flags=re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    oob_files[match.strip('"')] = 0

# Part 2 - find if oob file is present
    oob_files = DataCleaner.clear_false_positives(input_iter=oob_files, false_positives=FALSE_POSITIVES)
    logging.debug(f'{len(oob_files)} unique usages of oob files found')

    for filename in glob.iglob(path_to_oob_files + '**/*.txt', recursive=True):
        for oob in oob_files:
            if oob == os.path.basename(filename.lower())[:-4]:
                oob_files[oob] += 1

# Part 3 - throw the error if oob file is not found
    results = [i for i in oob_files if oob_files[i] == 0]
    ResultsReporter.report_results(results=results, message="Missing oob files were found. Check console output")
