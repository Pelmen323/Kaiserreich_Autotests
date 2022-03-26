##########################
# Test script to check if generals and admirals have relevant stats
# If admiral uses general stats, the game will not throw an error :pdx: pls
# Checks if generals/admirals use correct stats and correct sums of stats
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.characters_class import Characters


def test_check_generals_and_admiral_stats(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    results = {}

    # Check stats in characters files
    for char in characters:

        char_name = re.findall('^\\t(.+) =', char)[0]
        admiral_role = char.count("navy_leader =") > 0
        corps_commander_role = char.count("corps_commander =") > 0
        field_marshal_role = char.count("field_marshal =") > 0
        if not any([corps_commander_role, field_marshal_role, admiral_role]):
            continue
        # Check if unit leaders have relevant stats
        if any([corps_commander_role, field_marshal_role]):
            try:
                atk_skill = re.findall("attack_skill = (\\d+)", char)[0]
                dfs_skill = re.findall("defense_skill = (\\d+)", char)[0]
                pln_skill = re.findall("planning_skill = (\\d+)", char)[0]
                log_skill = re.findall("logistics_skill = (\\d+)", char)[0]
                sum_of_stats = int(atk_skill) + int(dfs_skill) + int(pln_skill) + int(log_skill)
            except IndexError:
                results[(char_name, paths[char])] = 'Unit leader is missing skills'
                continue

        elif admiral_role:
            try:
                atk_skill = re.findall("attack_skill = (\\d+)", char)[0]
                dfs_skill = re.findall("defense_skill = (\\d+)", char)[0]
                mnvr_skill = re.findall("maneuvering_skill = (\\d+)", char)[0]
                coord_skill = re.findall("coordination_skill = (\\d+)", char)[0]
                sum_of_stats = int(atk_skill) + int(dfs_skill) + int(mnvr_skill) + int(coord_skill)
            except IndexError:
                results[(char_name, paths[char])] = 'Admiral is missing skills'
                continue

        try:
            skill_level = int(re.findall("skill = (\\d+)", char)[0])
        except IndexError:
            results[(char_name, paths[char])] = 'Character is missing skill level'
            continue

        # Check sums of stats
        if skill_level < 1:
            results[(char_name, paths[char])] = 'Unit leader has < 1 level'
        if skill_level == 1:
            if sum_of_stats != 4:
                results[(char_name, paths[char])] = 'Level 1 unit leader has more or less than 4 skill points'
        if skill_level == 2:
            if sum_of_stats != 7:
                results[(char_name, paths[char])] = 'Level 2 unit leader has more or less than 7 skill points'
        if skill_level == 3:
            if sum_of_stats != 10:
                results[(char_name, paths[char])] = 'Level 3 unit leader has more or less than 10 skill points'
        if skill_level == 4:
            if sum_of_stats != 13:
                results[(char_name, paths[char])] = 'Level 4 unit leader has more or less than 13 skill points'
        if skill_level == 5:
            if sum_of_stats != 16:
                results[(char_name, paths[char])] = 'Level 5 unit leader has more or less than 16 skill points'
        if skill_level > 5:
            results[(char_name, paths[char])] = 'This unit leader level is > 5'

    ResultsReporter.report_results(results=results, message="Issues with characters stats sums encountered. Check console output")
