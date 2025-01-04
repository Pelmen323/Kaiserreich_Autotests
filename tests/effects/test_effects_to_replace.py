##########################
# Test script to check if specific pattern is used that can be replaced with scripted effect (in KR there are scripted effects that should be used instead)
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

import pytest

from test_classes.generic_test_class import FileOpener, ResultsReporter

input_list = [
    ["set_state_category", r".*set_state_category = [^o].*", "Singleline", "set_state_category is encountered - use 'increase_state_category_by_one_level = yes' instead"],
    ["add_research_slot", r".*add_research_slot = 1.*", "Singleline", "add_research_slot usage is encountered - use 'add_research_slot_until_four/five/six / add_temporary_research_slot' instead"],
    ["modifier = embargo", r".*modifier = embargo.*", "Singleline", "modifier = embargo usage is encountered - use 'embargo_XXX/clear_embargo_XXX' instead"],
    ["building slots", r"add_building_construction = \{[^\}]+?\}\n\t+add_extra_state_shared_building_slots", "Multiline", "add slots before buildings"],
    # ["any_neighbor_country", ".*any_neighbor_country[^\\}]*\\n.*tag =.*", "Singleline", "use is_neighbor_of instead"],
]


@pytest.mark.parametrize("input_list", input_list)
def test_effects_to_replace(test_runner: object, input_list):
    filepath = test_runner.full_path_to_mod
    results = []
    key_string, pattern, regex_mode, error_message = input_list

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        if "00_useful_scripted_effects" in filename:  # Skipped since the effects are stored here
            continue
        text_file = FileOpener.open_text_file(filename)
        if key_string in text_file:

            if regex_mode == "Singleline":
                pattern_matches = re.findall(pattern, text_file)
            elif regex_mode == "Multiline":
                pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    m = match.replace("\t", "").replace("\n", "  ")
                    results.append(f"{m} - {os.path.basename(filename)}")

    ResultsReporter.report_results(results=results, message=error_message)
