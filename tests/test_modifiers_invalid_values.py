##########################
# Test script to check if specific modifier values are too big/small
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

import pytest

from ..test_classes.generic_test_class import FileOpener, ResultsReporter

FALSE_POSITIVES = ["BHU", "BAT", "KR_high_command"]

input_list = [
    ["conscription_factor", "< 0.05", "> -0.05"],
    ["land_reinforce_rate", "> 0.05", "< -0.069"],
#     ["compliance_gain", "> 0.05", "None"],
#     ["research_speed_factor", "> 0.15", "None"],
#     ["local_resources_factor", "> 0.25", "None"],
#     ["political_power_factor", "> 0.25", "None"],
#     ["consumer_goods_factor", "None", "< -0.1"],
#     ["industrial_capacity_factory", "> 0.25", "None"],
#     ["industrial_capacity_dockyard", "> 0.25", "None"],
#     ["offence", "> 0.09", "None"],
#     ["defence", "> 0.09", "None"],
#     ["army_attack_factor", "> 0.19", "None"],
#     ["army_defence_factor", "> 0.19", "None"],
#     ["army_org", "> 5", "None"],
#     ["army_org_factor", "> 0.19", "None"],
#     ["army_org_regain", "> 0.19", "None"],
#     ["breakthrough_factor", "> 0.19", "None"],
]


@pytest.mark.parametrize("input_list", input_list)
def test_modifiers_innvalid_values(test_runner: object, input_list):
    filepath = test_runner.full_path_to_mod
    results = []
    modifier = input_list[0]
    value_above_zero = float(input_list[1][2:]) if input_list[1] != "None" else False
    value_above_zero_condition = input_list[1][0] if input_list[1] != "None" else False
    value_below_zero = float(input_list[2][2:]) if input_list[2] != "None" else False
    value_below_zero_condition = input_list[2][0] if input_list[2] != "None" else False
    pattern = '\\b' + modifier + ' = ([^ \t\n]*)'

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if "ideas" not in filename and "country_leader" not in filename:
            continue
        if [i for i in FALSE_POSITIVES if i in filename]:
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
