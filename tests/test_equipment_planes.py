##########################
# Test script to check if BBA planes are spawned with version name passed
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_equipment_planes_spawn(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}history\\units'
    results = []
    key_string = "_airframe_"
    pattern = '(^(\\t+)[\\w_]+_airframe_. = \\{.*?^\\2\\})'
    pattern2 = '^\\t+[\\w_]+_airframe_. = \\{.*?\\}'

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "_bba" not in filename:
            continue
        text_file = FileOpener.open_text_file(filename)
        if key_string in text_file:

            pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "version_name =" not in match[0]:
                        results.append((match[0].replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

            pattern_matches = re.findall(pattern2, text_file, flags=re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    if "version_name =" not in match:
                        results.append((match.replace('\t', '').replace('\n', '  '), os.path.basename(filename)))

    ResultsReporter.report_results(results=results, message="Planes w/o version name passed are spawned. This will cause unusable planes to spawn")
