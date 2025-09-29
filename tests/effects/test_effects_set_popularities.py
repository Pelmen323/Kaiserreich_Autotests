##########################
# Test script to check if set_popularities values == 100
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_effects_set_popularities(test_runner: object):
    filepath = test_runner.full_path_to_mod
    pattern = r'^(\t+)set_popularities = (\{\n.*?)^\1\}'
    number_pattern = r'= ([\d\.]+)'
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "set_popularities" in text_file:
            pattern_matches = re.findall(pattern, text_file, flags=re.MULTILINE | re.DOTALL)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    body = match[1]
                    number_matches = re.findall(number_pattern, body)
                    if len(number_matches) > 2:
                        x = sum([float(i) for i in number_matches])
                        body = body.replace('\t', ' ').replace('\n', '')
                        if x != 100:
                            body = body.replace('\t', ' ').replace('\n', '')
                            results.append(f"{body} - {os.path.basename(filename)} - {x} != 100")
                        for i in number_matches:
                            if str(float(i)) == i:
                                results.append(f"{body} - {os.path.basename(filename)} - float {i} detected")

    ResultsReporter.report_results(results=results, message="Party popularities != 100")
