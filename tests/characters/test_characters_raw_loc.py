##########################
# Test script to check for characters that use raw loc for name instead of keys
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.characters_class import Characters
from test_classes.generic_test_class import ResultsReporter


def test_characters_raw_loc(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, lowercase=False, return_paths=True)
    results = []

    for char in characters:
        char_name = re.findall(r"^\t(.+) =", char)[0]
        char_code = re.findall(r"^\t(\w.+) = \{", char)

        if "_" in char_name:
            continue

        if 'name = "' in char and "placeholder" not in char_code:
            results.append((f'{"".join(char_name)}', paths[char]))

    if results != []:
        ResultsReporter.report_results(results=results, message="Usage of raw loc in name line of characters was encountered.")
