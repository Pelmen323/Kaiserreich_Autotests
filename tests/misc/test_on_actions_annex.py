##########################
# Test script to check annex state variables
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_unsupported_on_actions(test_runner: object):
    filename = f'{test_runner.full_path_to_mod}common\\on_actions\\01_on_actions_annexations.txt'
    filepath = f'{test_runner.full_path_to_mod}common\\scripted_triggers\\'
    scripted_triggers = []
    annex_targets_used = []
    results = []

    text_file = FileOpener.open_text_file(filename)
    annex_targets_defined = re.findall(r"(\d+) = \{ set_variable = \{ annexation_target = this \} \}", text_file)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "Annex" in filename:
            print(filename)
            text_file = FileOpener.open_text_file(filename)
            if "can_release_" in text_file:
                pattern_matches = re.findall(r"^can_release_\S+ = \{.*?^\}", text_file, flags=re.DOTALL | re.MULTILINE)
                for i in pattern_matches:
                    scripted_triggers.append(i)

    for trigger in scripted_triggers:
        trigger_name = re.findall(r'^(can_release_\S+) = \{', trigger, flags=re.DOTALL | re.MULTILINE)[0]
        # if trigger.count("\tstate =") > 1:
        #     results.append(f'{trigger_name} - multiple state triggers found')
        if "\tstate =" in trigger:
            pattern_matches = re.findall(r'\tstate = (\d+)', trigger, flags=re.DOTALL | re.MULTILINE)
            for i in pattern_matches:
                annex_targets_used.append(i)

    for i in set(annex_targets_defined):
        if i not in set(annex_targets_used):
            results.append(f'{i} - is defined as annex target but not used')

    for i in set(annex_targets_used):
        if i not in set(annex_targets_defined):
            results.append(f'{i} - is used as annex target but not defined')

    ResultsReporter.report_results(results=results, message="Annex targets issues found.")
