##########################
# Test script to check for non-dlc techs usage
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_non_dlc_techs_usage(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_tanks = f'{test_runner.full_path_to_mod}common\\technologies\\armor.txt'
    filepath_to_ships = f'{test_runner.full_path_to_mod}common\\technologies\\naval.txt'
    filepath_to_planes = f'{test_runner.full_path_to_mod}common\\technologies\\air_techs.txt'
    results = []
    non_dlc_techs = []

    # Extract non-dlc techs names
    for i in [filepath_to_tanks, filepath_to_ships, filepath_to_planes]:
        text_file = FileOpener.open_text_file(i)
        pattern_matches = re.findall("^\t([^\t]+?) =", text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                non_dlc_techs.append(match)

    # Check non-dlc tech usage
    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "transfer_technology" in filename or "history\\countries" in filename or "technologies" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        for i in non_dlc_techs:
            if i in text_file:
                if f'technology = {i}' in text_file:
                    pattern = "technology = " + i + "\\b"
                    pattern_matches = re.findall(pattern, text_file)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            results.append((match, os.path.basename(filename)))
                if f'has_tech = {i}' in text_file:
                    pattern = "has_tech = " + i + "\\b"
                    pattern_matches = re.findall(pattern, text_file)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            results.append((match, os.path.basename(filename)))
                if f'{i} = 1' in text_file:
                    results.append((f"{i} = 1", os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Non-DLC techs usage encountered. Check console output")
