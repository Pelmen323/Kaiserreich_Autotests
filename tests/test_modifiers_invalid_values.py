##########################
# Test script to check if specific modifier values are too big/small
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

import pytest

from ..test_classes.generic_test_class import FileOpener, ResultsReporter

input_list = [
    ["conscription_factor", "< 0.05", "> -0.05"],
    ["land_reinforce_rate", "> 0.05", "< -0.069"],
]


@pytest.mark.parametrize("input_list", input_list)
def test_modifiers_innvalid_values(test_runner: object, input_list):
    filepath = test_runner.full_path_to_mod
    results = []
    modifier = input_list[0]
    value_above_zero = float(input_list[1][2:]) if input_list[1] != "None" else False
    value_above_zero_condition = input_list[1][0] if input_list[1] != "None" else False
    value_below_zero = float(input_list[2][2:]) if input_list[2] != "None" else False
    value_below_zero_condition = input_list[2][0] if input_list[1] != "None" else False
    pattern = '\\b' + modifier + ' = ([^ \t\n]*)'

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "technologies" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)
        if f'{modifier} =' in text_file:
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    try:
                        match_float = float(match)
                    except ValueError:              # Ignore variables
                        continue

                    if value_above_zero and match_float > 0:
                        if value_above_zero_condition == ">":
                            if match_float > value_above_zero:
                                results.append((modifier, f'{match_float} {value_above_zero_condition} {value_above_zero}', filename.split("Kaiserreich Dev Build\\")[1]))

                        elif value_above_zero_condition == "<":
                            if match_float < value_above_zero:
                                results.append((modifier, f'{match_float} {value_above_zero_condition} {value_above_zero}', filename.split("Kaiserreich Dev Build\\")[1]))

                    elif value_below_zero and match_float < 0:
                        if value_below_zero_condition == ">":
                            if match_float > value_below_zero:
                                results.append((modifier, f'{match_float} {value_below_zero_condition} {value_below_zero}', filename.split("Kaiserreich Dev Build\\")[1]))

                        elif value_below_zero_condition == "<":
                            if match_float < value_below_zero:
                                results.append((modifier, f'{match_float} {value_below_zero_condition} {value_below_zero}', filename.split("Kaiserreich Dev Build\\")[1]))

    ResultsReporter.report_results(results=results, message=f"{modifier} is used with too big/small values")
