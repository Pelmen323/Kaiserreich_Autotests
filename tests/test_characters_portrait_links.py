##########################
# Test script to check if characters (unit leaders) have small portraits
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_characters_already_hired(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    results = []

    for char in characters:
        unit_leader_role = any([char.count('field_marshal =') > 0, char.count('corps_commander =') > 0, char.count('navy_leader =') > 0])
        try:
            char_name = re.findall('name = (\\w*)', char)[0]
        except IndexError:
            results.append((char, paths[char], "Missing char name"))
        if unit_leader_role:
            pattern_matches = re.findall('portraits = \\{.*army = \\{.*small =.*\\}.*\\}', char.replace("\n", "").replace('\t', ""))
            if len(pattern_matches) < 1:
                results.append((char_name, paths[char], "Character is missing small portrait link"))

    ResultsReporter.report_results(results=results, message="Missing unit leaders portrait links were encountered. Check console output")
