##########################
# Test script to check if generals and admirals have relevant stats
# If admiral uses general stats, the game will not throw an error :pdx: pls
# Checks if generals/admirals use correct stats
# Checks both character files and each other file
# By Pelmen, https://github.com/Pelmen323
##########################
import os
import glob
import re
from .imports.file_functions import open_text_file
import logging


def test_check_generals_and_admiral_stats(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}common\\characters\\'
    results = {}
    os.chdir(filepath)

    for filename in glob.glob("*.txt"):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.warning(f'Skipping the file {filename}')
            logging.warning(ex)
            continue

        admirals_in_file = len(re.findall("navy_leader = \\{", text_file))
        corps_commanders_in_file = len(re.findall("corps_commander = \\{", text_file))
        field_marshals_in_file = len(re.findall("field_marshal = \\{", text_file))

        atk_skill_num = len(re.findall("attack_skill = ", text_file))
        dfs_skill_num = len(re.findall("defense_skill = ", text_file))
        pln_skill_num = len(re.findall("planning_skill = ", text_file))
        log_skill_num = len(re.findall("logistics_skill = ", text_file))
        mnvr_skill_num = len(re.findall("maneuvering_skill = ", text_file))
        coord_skill_num = len(re.findall("coordination_skill = ", text_file))

        total_num_of_commanders = admirals_in_file + corps_commanders_in_file + field_marshals_in_file
        total_num_of_land_commanders = corps_commanders_in_file + field_marshals_in_file

        if atk_skill_num != total_num_of_commanders:
            results[f'{os.path.basename(filename)}, attack_skill'] = f'Num of attack_skill encountered ({atk_skill_num}) is not equal to commanders number ({total_num_of_commanders})'
        if dfs_skill_num != total_num_of_commanders:
            results[f'{os.path.basename(filename)}, defense_skill'] = f'Num of defense_skill encountered ({dfs_skill_num}) is not equal to commanders number ({total_num_of_commanders})'
        if pln_skill_num != total_num_of_land_commanders:
            results[f'{os.path.basename(filename)}, planning_skill'] = f'Num of planning_skill encountered ({pln_skill_num}) is not equal to commanders number ({total_num_of_land_commanders})'
        if log_skill_num != total_num_of_land_commanders:
            results[f'{os.path.basename(filename)}, logistics_skill'] = f'Num of logistics_skill encountered ({log_skill_num}) is not equal to commanders number ({total_num_of_land_commanders})'
        if mnvr_skill_num != admirals_in_file:
            results[f'{os.path.basename(filename)}, maneuvering_skill'] = f'Num of maneuvering_skill encountered ({mnvr_skill_num}) is not equal to admirals number ({admirals_in_file})'
        if coord_skill_num != admirals_in_file:
            results[f'{os.path.basename(filename)}, coordination_skill'] = f'Num of coordination_skill encountered ({coord_skill_num}) is not equal to admirals number ({admirals_in_file})'


# Part 2 - check add_naval_commander_role
    filepath = test_runner.full_path_to_mod
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if '\\characters\\' in filename:
            continue
        elif '_traits.txt' in filename:
            continue

        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            logging.debug(f"Skipping the file {filename}")
            logging.warning(ex)
            continue
        if "add_naval_commander_role = {" in text_file or "add_field_marshal_role = {" in text_file or "add_corps_commander_role = {":
            admirals_in_file = len(re.findall("add_naval_commander_role = \\{", text_file))
            corps_commanders_in_file = len(re.findall("add_field_marshal_role = \\{", text_file))
            field_marshals_in_file = len(re.findall("add_corps_commander_role = \\{", text_file))

            atk_skill_num = len(re.findall("attack_skill = ", text_file))
            dfs_skill_num = len(re.findall("defense_skill = ", text_file))
            pln_skill_num = len(re.findall("planning_skill = ", text_file))
            log_skill_num = len(re.findall("logistics_skill = ", text_file))
            mnvr_skill_num = len(re.findall("maneuvering_skill = ", text_file))
            coord_skill_num = len(re.findall("coordination_skill = ", text_file))

            total_num_of_commanders = admirals_in_file + corps_commanders_in_file + field_marshals_in_file
            total_num_of_land_commanders = corps_commanders_in_file + field_marshals_in_file

            if atk_skill_num != total_num_of_commanders:
                results[f'{os.path.basename(filename)}, attack_skill'] = f'Num of attack_skill encountered ({atk_skill_num}) is not equal to commanders number ({total_num_of_commanders})'
            if dfs_skill_num != total_num_of_commanders:
                results[f'{os.path.basename(filename)}, defense_skill'] = f'Num of defense_skill encountered ({dfs_skill_num}) is not equal to commanders number ({total_num_of_commanders})'
            if pln_skill_num != total_num_of_land_commanders:
                results[f'{os.path.basename(filename)}, planning_skill'] = f'Num of planning_skill encountered ({pln_skill_num}) is not equal to commanders number ({total_num_of_land_commanders})'
            if log_skill_num != total_num_of_land_commanders:
                results[f'{os.path.basename(filename)}, logistics_skill'] = f'Num of logistics_skill encountered ({log_skill_num}) is not equal to commanders number ({total_num_of_land_commanders})'
            if mnvr_skill_num != admirals_in_file:
                results[f'{os.path.basename(filename)}, maneuvering_skill'] = f'Num of maneuvering_skill encountered ({mnvr_skill_num}) is not equal to admirals number ({admirals_in_file})'
            if coord_skill_num != admirals_in_file:
                results[f'{os.path.basename(filename)}, coordination_skill'] = f'Num of coordination_skill encountered ({coord_skill_num}) is not equal to admirals number ({admirals_in_file})'

# Part 3 - Report the results
    if results != {}:
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} times incorrect sum of stats found.')
        raise AssertionError("These files don't have matching sums of stats - this means character characters stats is wrong! Check console output")
