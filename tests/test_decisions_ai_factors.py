##########################
# Test script to check for decisions and selectable without ai factors
# The decisions/missions should have icons set for script to work
# Both missing and excessive ai factors will be reported
# Add files with empty decisions/ missions to files_to_skip
# By Pelmen, https://github.com/Pelmen323
##########################


from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.generic_test_class import ResultsReporter

NON_AI_DECISIONS = (
    "turn_off_plpc_debug",
    "turn_on_plpc_debug",
)


def test_check_decisions_ai_factors(test_runner: object):
    results = []
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)

    for i in decisions:
        decision = DecisionsFactory(dec=i)
        if decision.token in NON_AI_DECISIONS:
            continue
        if decision.mission_subtype:
            if decision.selectable_mission:
                if not decision.has_ai_factor:
                    results.append((decision.token, paths[i], "Selectable mission doesn't have AI factor"))
            elif decision.has_ai_factor:
                results.append((decision.token, paths[i], "Non-selectable mission has AI factor"))

        elif not decision.has_ai_factor:
            results.append((decision.token, paths[i], "Regular decision doesn't have AI factor"))

    ResultsReporter.report_results(results=results, message="Issues with decisions AI factors encountered. Check console output")
