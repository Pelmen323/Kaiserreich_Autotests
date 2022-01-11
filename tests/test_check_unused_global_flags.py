##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or vatiables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
from .imports.file_functions import open_text_file
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FALSE_POSITIVES = ['JAP_war_vs_ENT', 'CAN_king_busy', 'first_inter_congress_CUB', 'PAP_pontine_marshes']


@pytest.mark.parametrize("false_positives", [FALSE_POSITIVES])
@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_unused_global_flags(filepath: str, false_positives: str):
    print("The test is started. Please wait...")
    global_flags = {}
    # Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        global_flags_in_file = re.findall('set_global_flag = \\w.*\n', text_file)
        if len(global_flags_in_file) > 0:
            for flag in global_flags_in_file:
                flag = flag[18:-1]                  # cut the 'set_global_flag =' part and \n symbol
                if '}' in flag:
                    flag = flag.replace('}', '')
                if '#' in flag:
                    flag = flag[:flag.index('#')]   # cut the comments
                flag = flag.strip()
                global_flags[flag] = 0

    # Part 1.5 - clear false positives:
    for key in false_positives:
        try:
            global_flags.pop(key)
        except KeyError:
            continue

    false_keys = [key for key in global_flags if '@' in key]
    for key in false_keys:
        global_flags.pop(key)

    # Part 2 - count the number of their occurrences
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        for flag in global_flags.keys():
            global_flags[flag] += text_file.count(f'has_global_flag = {flag}')

    results = [i for i in global_flags if global_flags[i] == 0]
    if results != []:
        print("Following global flags are not checked via has_global_flag! Recheck them")
        for i in results:
            print(i)
        raise AssertionError("Unused global flags were encountered! Check console output")
    print("The test is finished!")
