##########################
# Test script to check if NOT = { trigger = yes } code is present, to replace it with trigger = no
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.scripted_triggers_class import ScriptedTriggers


def test_trigger_simplification(test_runner: object):
    filepath = test_runner.full_path_to_mod
    triggers = ScriptedTriggers.get_all_triggers_names(test_runner=test_runner, lowercase=False)
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if " = yes" in text_file:
            for t in triggers:
                if t in text_file:
                    if 'NOT = { ' + t + ' = yes }' in text_file:
                        results.append(f"{t} - {os.path.basename(filename)}")
                    else:
                        pattern = r'NOT = \{\n\t+' + t + r' = yes\n\t+\}'
                        match = re.findall(pattern, text_file)
                        if len(match) > 0:
                            results.append(f"{t} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message="Triggers that can be simplified are detected")
