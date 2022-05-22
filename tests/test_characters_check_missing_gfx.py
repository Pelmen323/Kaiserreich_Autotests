##########################
# Test script to check for duplicated characters
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import pytest
import os
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters


@pytest.mark.skip(reason="Currently disabled")
def test_characters_check_gfx(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    filepath = test_runner.full_path_to_mod
    portraits_paths = []
    results = []

    for char in characters:
        char_name = re.findall('^\\t(.+) =', char)[0]
        portraits_small = re.findall('small = ([^\\t\\n ]+)', char)
        portraits_large = re.findall('large = ([^\\t\\n ]+)', char)
        portraits = portraits_small + portraits_large
        if portraits == []:
            results.append((char_name, paths[char], "This character doesn't have any portraits"))
            continue
        for i in portraits:
            portraits_paths.append([i.strip('"').replace('/', '\\'), char_name, paths[char], "Missing portrait"])

    for i in portraits_paths:
        link = f'{filepath}{i[0]}'
        if os.path.exists(link) is False:
            results.append(i)

    ResultsReporter.report_results(results=results, message="Missing portrait links were encountered. Check console output")
