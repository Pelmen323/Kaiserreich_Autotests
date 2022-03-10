##########################
# Test script to check is unoptimised combination of conditions is used, that can be replaced by "is_ally_with"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner
import logging
import pytest
from itertools import permutations


@pytest.mark.skip(reason='Only for manual execution and reviewing')
def test_check_conditions_is_ally_with(test_runner: object):
    filepath = test_runner.full_path_to_mod
    conditions = []
    paths = []

# Part 1 - prepare the list of patterns    
    possible_parts_of_pattern = ['.*tag.*\\n', '.*is_in_faction_with.*\\n', '.*is_subject_of.*\\n']
    all_regex_patterns_raw = list(permutations(possible_parts_of_pattern))
    all_regex_patterns = []
    for pattern in all_regex_patterns_raw:
        all_regex_patterns.append(''.join(pattern))
    all_regex_patterns.append('.*\\{.*\\n.*is_in_faction_with.*\\n.*is_subject_of.*\\n.*\\}')
    all_regex_patterns.append('.*\\{.*\\n.*is_subject_of.*\\n.*is_in_faction_with.*\\n.*\\}')


# Part 2 - perform search 
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if 'is_subject_of' in text_file:
            for pattern in all_regex_patterns:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        conditions.append(match)
                        paths.append(os.path.basename(filename))


# Part 3 - throw the error if those combinations are encountered
    results = conditions
    if results != []:
        logging.warning("Following files can use 'is_ally_with' condition instead:")
        for i in results:
            logging.error(f"- [ ] {i} - {paths[results.index(i)]}")
        logging.warning(f'{len(results)} issues found.')
        raise AssertionError("'is_ally_with' condition can be used in the mentioned files. Check console output")
