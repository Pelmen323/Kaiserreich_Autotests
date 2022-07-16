##########################
# Test script to check for decisions that generate wargoals if they have required parts
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.generic_test_class import ResultsReporter


def test_check_decisions_wargoals(test_runner: object):
    # Part 1 - get the dict of all decisions
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for i in decisions:
        if 'create_wargoal' in i or 'declare_war_on = {' in i:
            decision = DecisionsFactory(dec=i)
            # 1 - Does the remove_effect have clear_decision_attack_AI?
            if "clear_decision_attack_ai" not in decision.remove_effect:
                results.append(f'{decision.token}, {paths[i]} - Missing "clear_decision_attack_ai" in "remove_effect"')

            # 2 - Does the complete_effect have setup_decision_attack_AI?
            if "setup_decision_attack_ai" not in decision.complete_effect:
                results.append(f'{decision.token}, {paths[i]} - Missing "setup_decision_attack_ai" in "complete_effect"')

            # 3 - Does the cancel_effect have clear_decision_attack_AI?
            if "clear_decision_attack_ai" not in decision.cancel_effect:
                results.append(f'{decision.token}, {paths[i]} - Missing "clear_decision_attack_ai" in "cancel_effect"')

            # 4 - Does the decision have a cancel_trigger or cancel_if_not_visible?
            if decision.cancel_effect is False and decision.cancel_if_not_visible is False:
                results.append(f'{decision.token}, {paths[i]} - The decision doesnt have either "cancel_effect" or "cancel_if_not_visible = yes"')

            # 5 - Does the decision have war_with_on_remove = TAG or war_with_target_on_remove = yes?
            if decision.war_with_on_remove is False and decision.war_with_target_on_remove is False:
                results.append(f'{decision.token}, {paths[i]} - The decision doesnt have either "war_with_on_remove" or "war_with_target_on_remove = yes"')

            # 6. Notifications
            if "warning event" not in decision.complete_effect and "kr.political.30" not in decision.complete_effect:
                results.append(f'{decision.token}, {paths[i]} - The decision doesnt contain notification for a target. If it is - add #warning event comment to complete_effect section"')

    # Part 2 - throw the error if entity is duplicated
    ResultsReporter.report_results(results=results, message="Issues with decisions that start wars were encountered. Check console output")
