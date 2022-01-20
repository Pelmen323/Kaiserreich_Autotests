##########################
# Test script to check for unused global flags
# If flag is not used via "has_global_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
from timeit import default_timer as timer
from .imports.file_functions import open_text_file, clear_false_positives_flags
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FALSE_POSITIVES = ['first_inter_congress_CUB']


@pytest.mark.parametrize("false_positives", [FALSE_POSITIVES])
@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_unused_global_flags(filepath: str, false_positives: str):
    print("The test is started. Please wait...")
    start = timer()
    global_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        global_flags_in_file = re.findall('set_global_flag = \\b\\w*\\b', text_file)
        if len(global_flags_in_file) > 0:
            for flag in global_flags_in_file:
                flag = flag[18:]                  # cut the 'set_global_flag =' part and \n symbol
                flag = flag.strip()
                global_flags[flag] = 0

        global_flags_in_file = re.findall('set_global_flag = \\{ flag = \\b\\w*\\b', text_file)
        if len(global_flags_in_file) > 0:
            for flag in global_flags_in_file:
                flag = flag[27:]                 # cut the 'has_country_flag =' part and \n symbol
                flag = flag.strip()
                global_flags[flag] = 0

# Part 2 - clear false positives and flags with variables:
    print(f'{len(global_flags)} global flags were found')
    clear_false_positives_flags(flags_dict=global_flags, false_positives=false_positives)

# Part 3 - count the number of flag occurrences
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        for flag in global_flags.keys():
            global_flags[flag] += text_file.count(f'has_global_flag = {flag}')
            global_flags[flag] += text_file.count(f'has_global_flag = {{ flag = {flag}')

# Part 4 - throw the error if flag is not used
    results = [i for i in global_flags if global_flags[i] == 0]
    if results != []:
        print("Following global flags are not checked via has_global_flag! Recheck them")
        for i in results:
            print(i)
        raise AssertionError("Unused global flags were encountered! Check console output")
    end = timer()
    print(f"The test is finished in {end-start} seconds!")
