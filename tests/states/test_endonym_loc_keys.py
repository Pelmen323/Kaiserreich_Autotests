##########################
# Test script to check fol loc keys that are not used in endonym scripted loc
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.states_class import States


def test_check_endonyms_scripted_loc(test_runner: object):
    filepath_to_scripted_loc_state = f'{test_runner.full_path_to_mod}common\\scripted_localisation\\00 - Scripted State Endonyms.txt'
    filepath_to_scripted_loc_vp = f'{test_runner.full_path_to_mod}common\\scripted_localisation\\00 - Scripted VP Endonyms.txt'
    filepath_to_keys_states = f'{test_runner.full_path_to_mod}localisation\\english\\KR_common\\00 Map States l_english.yml'
    filepath_to_keys_vp = f'{test_runner.full_path_to_mod}localisation\\english\\KR_common\\00 Map Victory Points l_english.yml'

    states_scripted_loc = []
    defined_state_loc_keys = []
    vp_scripted_loc = []
    defined_vp_loc_keys = []
    defined_vp_loc_keys_full = []
    results = []

    # 1. Get states scripted loc used keys
    states_scripted_loc_file = FileOpener.open_text_file(filepath_to_scripted_loc_state, lowercase=False)
    pattern_matches = re.findall("localization_key = (STATE_\\S*)", states_scripted_loc_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            states_scripted_loc.append(match)

    # 1.1 Get states scripted loc defined keys
    states_loc_file = FileOpener.open_text_file(filepath_to_keys_states, lowercase=False)
    pattern_matches = re.findall("(STATE_\\S*):", states_loc_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            defined_state_loc_keys.append(match)
            # Check if key is not used
            if match not in states_scripted_loc and "RENAME" not in match:
                results.append(f"{match} - this key is not USED in states scripted loc")

    # 1.2 - Check if there are missing loc keys:
    for i in states_scripted_loc:
        if i not in defined_state_loc_keys:
            results.append(f"{i} - this key is not DEFINED in states loc file")

    # 2. Get vp scripted loc used keys
    vp_scripted_loc_file = FileOpener.open_text_file(filepath_to_scripted_loc_vp, lowercase=False)
    pattern_matches = re.findall("localization_key = (VICTORY_POINTS_\\S*)", vp_scripted_loc_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            vp_scripted_loc.append(match)

    # 2.1 Get vp scripted loc defined keys
    vp_loc_file = FileOpener.open_text_file(filepath_to_keys_vp, lowercase=False)
    pattern_matches = re.findall("((VICTORY_POINTS_\\S*): .*)", vp_loc_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            defined_vp_loc_keys_full.append(match[0])
            defined_vp_loc_keys.append(match[1])
            # Check if key is not used
            if match[1] not in vp_scripted_loc and "RENAME" not in match[1]:
                results.append(f"{match[1]} - this key is not USED in VP scripted loc")

    # 2.2 - Check if there are missing loc keys:
    for i in vp_scripted_loc:
        if i not in defined_vp_loc_keys:
            results.append(f"{i} - this key is not DEFINED in VP loc file")

    # 3 - Check if correct province is targeted
    for i in defined_vp_loc_keys_full:
        if "RENAME" in i:
            vp_from_key = i[i.index("POINTS_") + 7: i.index("_RENAME")]
            value_str = i[i.index(":") + 2:]

            if f".GetVictoryPointName_{vp_from_key}" not in value_str:
                results.append(f"{i} - this key's value doesn't reference to the correct province")

    ResultsReporter.report_results(results=results, message="Issues with endonym loc keys were encountered. Check console output")
