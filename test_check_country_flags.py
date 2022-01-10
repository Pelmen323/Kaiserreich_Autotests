import glob
import pytest
import re
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"
# FALSE_POSITIVES = ['JAP_war_vs_ENT', 'CAN_king_busy', 'first_inter_congress_@ROOT', 'first_inter_congress_CUB', 'PAP_pontine_marshes']


# @pytest.mark.parametrize("false_positives", [FALSE_POSITIVES])
@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_unused_country_flags(filepath: str):
    print("The test is started. Please wait...")
    country_flags = {}
    # Part 1 - get the dict of all global flags
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:
                text_file = text_file.read()
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        country_flags_in_file = re.findall('set_country_flag = \\w.*\n', text_file)
        if len(country_flags_in_file) > 0:
            for flag in country_flags_in_file:
                flag = flag[19:-1]
                if '}' in flag:
                    flag = flag.replace('}', '')
                if '#' in flag:
                    flag = flag[:flag.index('#')]
                flag = flag.strip()
                country_flags[flag] = 0

    # Part 1.5 - clear false positives:
    # for key in false_positives:
    #     try:
    #         country_flags.pop(key)
    #     except:
    #         pass

    # Part 2 - count the number of their occurrences
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:
                text_file = text_file.read()
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        for flag in country_flags.keys():
            country_flags[flag] += text_file.count(f'has_country_flag = {flag}')

    results = [i for i in country_flags if country_flags[i] == 0]
    if results != []:
        print("Following country flags are not checked via has_country_flag! Recheck them")
        for i in results:
            print(i)
        print(f'{len(results)} unused country flags found. Probably some of these are false positives, but they should be rechecked!')
        raise AssertionError("Unused country flags were encountered! Check console output")
    print("The test is finished!")
