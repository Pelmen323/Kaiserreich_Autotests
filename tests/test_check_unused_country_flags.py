##########################
# Test script to check for unused country flags
# If flag is not used via "has_country_flag" at least once, it will appear in test results
# Flags with values or variables (ROOT/THIS/FROM) should be added to false positives
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import pytest
import re
from timeit import default_timer as timer
from .imports.file_functions import open_text_file, clear_false_positives_flags
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
FALSE_POSITIVES = ['HNN_rigged_last_days',
                'cubsuccconstscore',
                'cublibconstscore',
                'cubconconstscore',
                'cubradconstscore',
                'is_han_chinese_tag',
                'is_non_han_chinese_tag',
                'gre_balkans_coop',
                'YUN_republican_support',
                'INT_alliance_refused_',
                'DEN_awareness_raised',
                'women_suffrage',
                'LOM_crown_refused_',
                'ACW_new_england_war',
                'RUS_don_kuban_isolated']


@pytest.mark.parametrize("false_positives", [FALSE_POSITIVES])
@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_unused_country_flags(filepath: str, false_positives: str):
    print("The test is started. Please wait...")
    start = timer()
    country_flags = {}
# Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            text_file = open_text_file(filename)
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        country_flags_in_file = re.findall('set_country_flag = \\b\\w*\\b', text_file)
        if len(country_flags_in_file) > 0:
            for flag in country_flags_in_file:
                flag = flag[19:]
                flag = flag.strip()
                country_flags[flag] = 0

        country_flags_in_file2 = re.findall('set_country_flag = \\{ flag = \\b\\w*\\b', text_file)
        if len(country_flags_in_file2) > 0:
            for flag in country_flags_in_file2:
                flag = flag[27:]
                flag = flag.strip()
                country_flags[flag] = 0

        # For flags with values. DO NOT UNCOMMENT unless manually verifying those flags
        # country_flags_in_file3 = re.findall('set_country_flag = \\{\\n\\t*flag = \\b\\w*\\b', text_file)
        # if len(country_flags_in_file3) > 0:
        #     for flag in country_flags_in_file3:
        #         flag2 = re.search(r'\bflag = \b\w*\b', flag).group(0)
        #         flag2 = flag2[7:].strip()
        #         country_flags[flag2] = 0

# Part 2 - clear false positives and flags with variables:
    print(f'{len(country_flags)} global flags were found')
    clear_false_positives_flags(flags_dict=country_flags, false_positives=false_positives)

# Part 3 - count the number of flag occurrences
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

# Part 4 - throw the error if flag is not used
    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        print("Following country flags are not checked via has_country_flag! Recheck them")
        for i in results:
            print(i)
        raise AssertionError("Unused country flags were encountered! Check console output")
    end = timer()
    print(f"The test is finished in {end-start} seconds!")
