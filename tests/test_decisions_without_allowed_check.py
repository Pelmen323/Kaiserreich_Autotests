##########################
# Test script to check for event targets that are cleared but not set
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from ..test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)

FALSE_POSITIVES = [
    "promises_of_peace",
    "generic_raise_stability",
    "generic_raise_support",
    "war_propaganda",
    "war_propaganda_against_warmonger",
    "return_cores_to_ally",
    "return_cores_to_subject",
    "seize_some_trains_woo",
    "restructure_supply_system",
    "ai_set_up_templates",
    "turn_off_plpc_debug",
    "turn_on_plpc_debug",
    "turn_off_stt_debug",
    "turn_on_stt_debug",
    "war_propaganda_casualties",
    "war_propaganda_convoys",
    "war_propaganda_bombing",
    "can_invite_into_iedc",
    "can_iedc_economic_investment_home",
    "can_iedc_economic_investment",
    "can_join_isac_decision",
    "war_propaganda_radio_industry",
    "war_propaganda_film_industry",
]


def test_decisions_without_allowed_check(test_runner: object):
    filepath_to_decisions_categories = f'{test_runner.full_path_to_mod}common\\decisions\\categories\\'
    filepath_to_decisions = f'{test_runner.full_path_to_mod}common\\decisions\\'
    categories_without_allowed_trigger = []
    results = []

    # 1. Get all decision categories without allowed check:

    for filename in glob.iglob(filepath_to_decisions_categories + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        pattern_matches = re.findall("^\\w* = \\{.*?^\\}", text_file, flags=re.DOTALL | re.MULTILINE)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                category_name = re.findall("^(.*) = \\{", match)
                if "allowed = {" not in match:
                    categories_without_allowed_trigger.append(category_name[0])

    # 2. Extract the decisions for specific categories

    for filename in glob.iglob(filepath_to_decisions + '**/*.txt', recursive=True):
        if '\\categories\\' in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        for category in categories_without_allowed_trigger:
            if f'{category} =' in text_file:
                pattern = '^' + category + ' = \\{.*?^\\}'
                pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        decisions_matches = re.findall("^\\t\\w* = \\{.*?^\\t\\}", match, flags=re.DOTALL | re.MULTILINE)
                        if len(decisions_matches) > 0:
                            for decision_match in decisions_matches:
                                decision_name = re.findall("^\\t(.*) = \\{", decision_match)
                                if "allowed = {" not in decision_match:
                                    results.append(decision_name[0])

# Part 3 - throw the error if entity is not used
    results = DataCleaner.clear_false_positives(input_iter=results, false_positives=FALSE_POSITIVES)
    ResultsReporter.report_results(results=results, message="Decisions without allowed trigger were encountered. Check console output")
