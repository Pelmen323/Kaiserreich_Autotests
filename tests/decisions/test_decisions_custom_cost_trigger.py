##########################
# Test script to check if decisions have `ai_hint_pp_cost` and correctness of its usage
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.generic_test_class import ResultsReporter


def test_decisions_custom_cost_trigger(test_runner: object):
    results = []
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    cost_map = {
        "command_power": "add_command_power",
        "has_political_power": "add_political_power",
        "has_army_experience": "army_experience",
        "has_air_experience": "air_experience",
        "has_navy_experience": "navy_experience",
    }

    for decision in decisions:
        d = DecisionsFactory(dec=decision)
        if d.custom_cost_trigger:
            if "has_political_power" in d.custom_cost_trigger:
                reversed_pp_cost = False
                custom_cost_trigger_pp_line = re.findall(r"has_political_power.*", d.custom_cost_trigger)[0]
                if "not = { has_political_power" in d.custom_cost_trigger:
                    reversed_pp_cost = True

                # Check #1 - if > is not used in has `has_political_power line`
                if ">" not in custom_cost_trigger_pp_line and not reversed_pp_cost:
                    results.append(f"{d.token:<45}{paths[decision]:<55}doesn't have comparison operator > in 'has_political_power' custom cost trigger line")
                elif "<" not in custom_cost_trigger_pp_line and reversed_pp_cost:
                    results.append(f"{d.token:<45}{paths[decision]:<55}doesn't have comparison operator < in 'has_political_power' custom cost trigger line")
                # Ignore decisions with variables in custom cost pp line
                try:
                    pp_value = float(custom_cost_trigger_pp_line[custom_cost_trigger_pp_line.index(">") + 2:])
                except ValueError:
                    continue

                # Check #2 - if `ai_hint_pp_cost` value is not valid
                expected_ai_hint_pp_cost_value = pp_value + 0.01
                expected_ai_hint_pp_cost_value_plus_1 = pp_value + 1
                if d.ai_hint_pp_cost:
                    hint_cost = float(d.ai_hint_pp_cost)
                    if hint_cost != expected_ai_hint_pp_cost_value and hint_cost != expected_ai_hint_pp_cost_value_plus_1:
                        results.append(f"{d.token:<45}{paths[decision]:<55}expected - {expected_ai_hint_pp_cost_value} ai_hint_pp_cost, actual - {hint_cost}")

                # Check #3 - if `ai_hint_pp_cost` is present
                else:
                    results.append(f"{d.token:<45}{paths[decision]:<55}missing 'ai_hint_pp_cost' line, should have `ai_hint_pp_cost = {expected_ai_hint_pp_cost_value}`")

            elif d.ai_hint_pp_cost:
                results.append(f"{d.token:<45}{paths[decision]:<55}useless 'ai_hint_pp_cost' line - no political power costs in custom_cost_trigger")

            for i in cost_map:
                if i in d.custom_cost_trigger and "<" in d.custom_cost_trigger and "check_variable" not in d.custom_cost_trigger and "var:" not in d.custom_cost_trigger:
                    custom_cost = re.findall(i + r" \< \d+", d.custom_cost_trigger)[0]
                    expected_cost_line = custom_cost.replace("< ", "= -").replace(i, cost_map[i])
                    expected_cost_line_refund = expected_cost_line.replace("-", "")
                    if d.cancel_effect:
                        if expected_cost_line_refund not in d.cancel_effect:
                            results.append(f"{d.token:<45}{paths[decision]:<55}cancel effect - unable to find expected refund value '{expected_cost_line_refund}'")
                    elif d.cancel_trigger:
                        results.append(f"{d.token:<45}{paths[decision]:<55}cancel effect - decision with custom cost '{custom_cost}' and cancel trigger but no cancel effect")

                    if d.complete_effect:
                        if expected_cost_line not in d.complete_effect:
                            results.append(f"{d.token:<45}{paths[decision]:<55}complete effect - unable to find expected cost value '{expected_cost_line}'")
                    else:
                        results.append(f"{d.token:<45}{paths[decision]:<55}complete effect - decision with custom cost '{custom_cost}' but no complete effect")

        elif d.ai_hint_pp_cost and d.cost:
            try:
                float(d.cost)
                results.append(f"{d.token:<45}{paths[decision]:<55}useless 'ai_hint_pp_cost' line - has non-variable cost line but no custom_cost_trigger")
            # Variable
            except ValueError:
                continue

        elif d.ai_hint_pp_cost:
            results.append(f"{d.token:<45}{paths[decision]:<55}useless 'ai_hint_pp_cost' line - has no custom_cost_trigger or cost")

    ResultsReporter.report_results(
        results=results, message="`ai_hint_pp_cost` should be used when AI needs help with figuring out how much PP to save in case where `cost` argument doesn't represent actual decision cost"
    )
