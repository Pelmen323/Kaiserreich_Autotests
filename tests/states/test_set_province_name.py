##########################
# Test script to check for loc keys that are used in set_province_name effect
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import glob

from ...test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_endonyms_scripted_loc(test_runner: object):
    filepath_to_keys_vp = f'{test_runner.full_path_to_mod}localisation\\KR_common\\00 Map Victory Points l_english.yml'
    filepath = test_runner.full_path_to_mod

    set_province_name_keys = []
    defined_vp_loc_keys = []
    defined_vp_loc_keys_full = []
    results = []

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "rename_scripted_effects" in filename:
            continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "set_province_name" in text_file:
            pattern_matches = re.findall("set_province_name = \\{ .*? \\}", text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    vp = re.findall("id = (.*?) ", match)[0]
                    key = re.findall(" name = (.*?) ", match)[0]
                    set_province_name_keys.append(key)
                    if f"_{vp}" not in key:
                        results.append(f"{match} - Key doesn't reference correct province")

    # Get vp scripted loc defined keys
    vp_loc_file = FileOpener.open_text_file(filepath_to_keys_vp, lowercase=False)
    pattern_matches = re.findall("((VICTORY_POINTS_\\S*): .*)", vp_loc_file)
    if len(pattern_matches) > 0:
        for match in pattern_matches:
            defined_vp_loc_keys_full.append(match[0])
            defined_vp_loc_keys.append(match[1])

    # Check if there are missing loc keys:
    for i in set_province_name_keys:
        if i not in defined_vp_loc_keys:
            results.append(f"{i} - this key is not DEFINED in VP loc file")

    ResultsReporter.report_results(results=results, message="Issues with set_province_name keys were encountered. Check console output")
