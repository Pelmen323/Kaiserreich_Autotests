##########################
# Test script to check if decisions have `ai_hint_pp_cost`
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.generic_test_class import ResultsReporter


def test_check_decisions_custom_cost_trigger(test_runner: object):
    results = []
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)

    for decision in decisions:

        # Check if decision has custom cost trigger
        if "custom_cost_trigger = {" in decision:
            pattern_matches = re.findall("(^\t*)custom_cost_trigger = \\{(.*?)^\\1\\}", decision, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:

                # If decision has this line - generate decision obj for name and check if it has has_political_power line
                custom_cost_trigger = pattern_matches[0][1]
                if "has_political_power" in custom_cost_trigger:
                    decision_object = DecisionsFactory(dec=decision)
                    custom_cost_trigger_pp_line = re.findall("has_political_power.*", custom_cost_trigger)[0]

                    # Check #1 - if > is not used in has has_political_power line
                    if ">" not in custom_cost_trigger_pp_line:
                        results.append(f"Decision `{decision_object.token}` - {paths[decision]} - doesn't have '>' in 'has_political_power' custom cost trigger line")

                    try:
                        pp_value = float(custom_cost_trigger_pp_line[custom_cost_trigger_pp_line.index(">") + 2:])
                    except ValueError:
                        continue        # Skip variables
                    expected_ai_hint_pp_cost_value = pp_value + 0.01

                    # Check #2 - if `ai_hint_pp_cost` value is not valid
                    if "ai_hint_pp_cost" in decision:
                        ai_hint_pp_cost_value = float(re.findall("ai_hint_pp_cost = (.*)", decision)[0])
                        if ai_hint_pp_cost_value != expected_ai_hint_pp_cost_value:
                            results.append(f"Decision `{decision_object.token}` - {paths[decision]} - doesn't have valid value in ai_hint_pp_cost line, expected - {expected_ai_hint_pp_cost_value}, actual - {ai_hint_pp_cost_value}")

                    # Check #3 - if `ai_hint_pp_cost` is present
                    else:
                        results.append(f"Decision `{decision_object.token}` - {paths[decision]} - doesn't have 'ai_hint_pp_cost' line, should have `ai_hint_pp_cost = {expected_ai_hint_pp_cost_value}`")

    ResultsReporter.report_results(results=results, message="Issues with `ai_hint_pp_cost` were encountered. Check console output")
