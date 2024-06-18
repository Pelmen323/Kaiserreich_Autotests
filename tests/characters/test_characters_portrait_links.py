##########################
# Test script to check if characters (unit leaders) have small portraits
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ...test_classes.characters_class import Characters
from ...test_classes.generic_test_class import ResultsReporter


def test_check_characters_already_hired(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    results = []
    pattern_army = r"\t\t\tarmy = \{.*?\}"
    pattern_navy = r"\t\t\tnavy = \{.*?\}"

    for char in characters:
        unit_leader_role_land = any([char.count("field_marshal =") > 0, char.count("corps_commander =") > 0])
        unit_leader_role_navy = char.count("navy_leader =") > 0
        if unit_leader_role_land or unit_leader_role_navy:
            char_name = re.findall("^\\t(.+) =", char)[0]
            army_portraits = str(re.findall(pattern_army, char, flags=re.DOTALL | re.MULTILINE))
            navy_portraits = str(re.findall(pattern_navy, char, flags=re.DOTALL | re.MULTILINE))

            if unit_leader_role_land:
                if "small =" not in army_portraits:
                    results.append((char_name, paths[char], "Character (army) is missing small portrait link"))
                if "large =" not in army_portraits:
                    results.append((char_name, paths[char], "Character (army) is missing large portrait link"))

            if unit_leader_role_navy:
                if "small =" not in army_portraits and "small =" not in navy_portraits:
                    results.append((char_name, paths[char], "Character (navy) is missing small portrait link"))

                if "large =" not in army_portraits and "large =" not in navy_portraits:
                    results.append((char_name, paths[char], "Character (navy) is missing large portrait link"))

    ResultsReporter.report_results(results=results, message="Missing unit leaders portrait links were encountered. Check console output")
