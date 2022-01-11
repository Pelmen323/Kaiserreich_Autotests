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
FALSE_POSITIVES = ['HNN_rigged_last_days',
                  'cubsuccconstscore',
                  'cublibconstscore',
                  'cubconconstscore',
                  'cubradconstscore',
                  'is_han_chinese_tag',
                  'is_non_han_chinese_tag',
]


@pytest.mark.parametrize("false_positives", [FALSE_POSITIVES])
@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_unused_country_flags(filepath: str, false_positives: str):
    print("The test is started. Please wait...")
    country_flags = {}
    # Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        country_flags_in_file = re.findall('set_country_flag = \\w.*\n', text_file)
        if len(country_flags_in_file) > 0:
            for flag in country_flags_in_file:
                flag = flag[19:-1]                 # cut the 'set_country_flag =' part and \n symbol
                if '}' in flag:
                    flag = flag.replace('}', '')
                if '#' in flag:
                    flag = flag[:flag.index('#')]  # cut the comments
                flag = flag.strip()
                country_flags[flag] = 0

    # Part 1.5 - clear false positives:
    for key in false_positives:
        try:
            country_flags.pop(key)
        except KeyError:
            continue

    false_keys = [key for key in country_flags if '@' in key]
    for key in false_keys:
        country_flags.pop(key)

    # Part 2 - count the number of their occurrences
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        for flag in country_flags.keys():
            country_flags[flag] += text_file.count(f'has_country_flag = {flag}')
            country_flags[flag] += text_file.count(f'has_country_flag = {{ flag = {flag}')

    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        print("Following country flags are not checked via has_country_flag! Recheck them")
        for i in results:
            print(i)
        print(f'{len(results)} unused country flags found. Probably some of these are false positives, but they should be rechecked!')
        raise AssertionError("Unused country flags were encountered! Check console output")
    print("The test is finished!")
