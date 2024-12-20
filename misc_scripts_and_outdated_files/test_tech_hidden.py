##########################
# Test script to check for non-dlc techs usage
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_non_dlc_techs_usage(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_techs = f'{test_runner.full_path_to_mod}common\\technologies'
    techs = []
    sub_techs = []
    results = []

    # Extract non-dlc techs names
    for filename in glob.iglob(filepath_to_techs + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        pattern_matches = re.findall(r"^\t[^\t]+? = \{.*?\n\t\}", text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                if "sub_technologies = {" in match:
                    sub_techs_str = re.findall(r"sub_technologies = \{\n(.*?)\n\t+\}", match, flags=re.DOTALL | re.MULTILINE)[0]
                    sub_techs_str = sub_techs_str.strip('\t')
                    if '\n' in sub_techs_str:
                        l1 = sub_techs_str.split('\n')
                        for i in l1:
                            sub_techs.append(i.strip('\t'))
                    else:
                        sub_techs.append(sub_techs_str)
                if "folder = {" not in match:
                    if "hidden" not in os.path.basename(filename):
                        tech_name = re.findall(r"^\t([^\t]+?) = \{", match, flags=re.DOTALL | re.MULTILINE)[0]
                        if tech_name not in sub_techs:
                            results.append(f'{tech_name} - {os.path.basename(filename)}')

    ResultsReporter.report_results(results=results, message="Non-DLC techs usage encountered. Check console output")
