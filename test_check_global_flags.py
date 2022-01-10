import glob
import pytest
import re
FILEPATH = "C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\"


@pytest.mark.parametrize("filepath", [FILEPATH])
def test_check_decisions_ai_factors(filepath: str):
    print("The test is started. Please wait...")
    global_flags = {}
    # Part 1 - get the dict of all global flags 
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:
                text_file = text_file.read()
        except Exception as ex:
            print(f'Skipping the file {filename}')
            print(ex)
            continue

        global_flags_in_file = re.findall('set_global_flag = \\w.*\n', text_file)
        if len(global_flags_in_file) > 0:
            for flag in global_flags_in_file:
                flag = flag[18:-1]
                global_flags[flag] = 0

    # Part 2 - count the number of their occurencies
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:
                text_file = text_file.read()
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
