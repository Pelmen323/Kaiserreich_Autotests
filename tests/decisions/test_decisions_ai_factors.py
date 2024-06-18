##########################
# Test script to check for decisions and selectable without ai factors
# The decisions/missions should have icons set for script to work
# Both missing and excessive ai factors will be reported
# Add files with empty decisions/ missions to files_to_skip
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.generic_test_class import ResultsReporter

NON_AI_DECISIONS = (
    "demobilization_economic",
    "demobilization_manpower",
    "ger_factories_for_colonies_full",
    "ger_factories_for_colonies_partly",
    "ger_agricultural_help",
)


def test_check_decisions_ai_factors(test_runner: object):
    results = []
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    decision_categories = Decisions.get_all_decisions_categories(test_runner=test_runner, lowercase=True)
    dict_decisions_categories = Decisions.get_decisions_categories_dict(test_runner=test_runner, lowercase=True)

    for i in decisions:
        decision = DecisionsFactory(dec=i)
        if decision.token in NON_AI_DECISIONS:
            continue
        if decision.available and any(["is_ai = no" in decision.available, "always = no" in decision.available]):
            continue
        if decision.visible and any(["is_ai = no" in decision.visible, "always = no" in decision.visible]):
            continue
        decision_category = [i for i in dict_decisions_categories.keys() if decision.token in dict_decisions_categories[i]][0]
        if "is_ai = no" in decision_categories[decision_category][0] or "always = no" in decision_categories[decision_category][0]:
            continue
        if decision.mission_subtype:
            if decision.selectable_mission:
                if not decision.has_ai_factor:
                    results.append((decision.token, paths[i], "Selectable mission doesn't have AI factor"))
            elif decision.has_ai_factor:
                results.append((decision.token, paths[i], "Non-selectable mission has AI factor"))

        elif not decision.has_ai_factor and "debug" not in decision.token:
            results.append((decision.token, paths[i], "Regular decision doesn't have AI factor"))

        if decision.has_ai_factor:
            ai_factors_found = re.findall("(base = [^ \\t\\n]+|factor = [^ \\t\\n]+|add = [^ \\t\\n]+)", decision.ai_factor)
            # Base and factor
            if len(ai_factors_found) > 0 and "base =" in decision.ai_factor:
                if "factor = 0" in ai_factors_found:
                    num_of_zeroed_factors = ai_factors_found.count("factor = 0")
                    for d in range(1, num_of_zeroed_factors):
                        if ai_factors_found[d] != "factor = 0":
                            results.append((decision.token, paths[i], f"{ai_factors_found} -Zeroed ai factors that are not evaluated immediately"))
                            break
            # Factor and factor
            elif len(ai_factors_found) > 1:
                if "factor = 0" in ai_factors_found:
                    num_of_zeroed_factors = ai_factors_found.count("factor = 0")
                    for d in range(1, num_of_zeroed_factors):
                        if ai_factors_found[d] != "factor = 0":
                            results.append((decision.token, paths[i], f"{ai_factors_found} - Zeroed ai factors that are not evaluated immediately"))
                            break

    ResultsReporter.report_results(results=results, message="Issues with decisions AI factors encountered. Check console output")
