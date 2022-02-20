##########################
# Test script to check if 'limit' is not used in if/elif conditions
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import glob
import re
from ..test_classes.generic_test_class import TestClass
import logging
FILES_TO_SKIP = ['\\history\\', '\\tanks\\',]
re.DOTALL


def test_check(test_runner: object):
    test = TestClass()
    filepath = test_runner.full_path_to_mod
    results = {}
    container = {}
    os.chdir(filepath)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if test.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        text_file = test.open_text_file(filename)

        if_count = re.findall('(\\bif = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(if_count) > 0:
            for match in if_count:
                match = match[0]                                            # Counter empty capture groups
                container[match] = os.path.basename(filename)

        else_if_count = re.findall('(\\belse_if = \\{.*\n(.|\n*?)*\n\t+\\})', text_file)
        if len(else_if_count) > 0:
            for match in else_if_count:
                match = match[0]                                            # Counter empty capture groups
                container[match] = os.path.basename(filename)

    for effect in container.keys():
        if 'limit = {' not in effect:
            results[effect] = container[effect]
        
    if results != {}:
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} issues found.')
        raise AssertionError("Issues with ifs/elifs found! Check console output")
