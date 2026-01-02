##########################
# Test script to check for decisions that generate wargoals if they have required parts
# By Pelmen, https://github.com/Pelmen323
##########################
import pytest
from test_classes.decisions_class import Decisions, DecisionsFactory
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = [
    "china_joint_strike_gxc_decision",  # Handled by event
    "ca_attack_socialist_bukhara_timer",
    "pol_operation_parasol"             # Non cancellable
]


# Uncomment once linked ticket is solved
@pytest.mark.skip(reason='https://github.com/Kaiserreich/Kaiserreich-4-Development/issues/11276')
def test_decisions_wargoals(test_runner: object):
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for i in decisions:
        setup_decision = "setup_decision_attack_ai" in i
        cancel_decision = "clear_decision_attack_ai" in i

        if setup_decision or cancel_decision:
            decision = DecisionsFactory(dec=i)

            if decision.token in FALSE_POSITIVES:
                continue

            # 1 - Does the remove_effect have clear_decision_attack_ai?
            if decision.remove_effect:
                if "clear_decision_attack_ai" not in decision.remove_effect:
                    results.append(f'{decision.token}, {paths[i]} - Missing "clear_decision_attack_ai" in "remove_effect"')

            else:
                results.append(f'{decision.token}, {paths[i]} - Missing "remove_effect"')

            # 2 - Does the complete_effect have setup_decision_attack_AI?
            if decision.complete_effect:
                if "setup_decision_attack_ai" not in decision.complete_effect:
                    results.append(f'{decision.token}, {paths[i]} - Missing "setup_decision_attack_ai" in "complete_effect"')

            else:
                results.append(f'{decision.token}, {paths[i]} - Missing "complete_effect"')

            # 3 - Does the cancel_effect have clear_decision_attack_ai?
            if decision.cancel_effect:
                if "clear_decision_attack_ai" not in decision.cancel_effect:
                    results.append(f'{decision.token}, {paths[i]} - Missing "clear_decision_attack_ai" in "cancel_effect"')

            # 4 - Does the decision have a cancel_trigger or cancel_if_not_visible?
            if decision.cancel_trigger is False and decision.cancel_if_not_visible is False:
                results.append(f'{decision.token}, {paths[i]} - The decision doesnt have either "cancel_trigger" or "cancel_if_not_visible = yes"')

            # 5 - Does the decision have a cancel_trigger and cancel_effect?
            if decision.cancel_trigger or decision.cancel_if_not_visible:
                if decision.cancel_effect is False:
                    results.append(f'{decision.token}, {paths[i]} - The decision has "cancel_trigger"/"cancel_if_not_visible = yes" but dont have cancel effect')

            # 6 - Does the decision have war_with_on_remove = TAG or war_with_target_on_remove = yes?
            if not decision.war_with_on_remove and not decision.war_with_target_on_remove and not decision.war_with_target_on_complete:
                results.append(f'{decision.token}, {paths[i]} - The decision doesn\'t have either "war_with_on_remove" or "war_with_target_on_remove" or "war_with_target_on_complete"')

        if "declare_war_on = {" in i or "create_wargoal = {" in i:
            if not setup_decision or not cancel_decision:
                decision = DecisionsFactory(dec=i)
                results.append(f'{decision.token:<45}-{paths[i]:<45}-Missing setup_decision_attack_ai or clear_decision_attack_ai or both')

            if "can_declare_war_on" not in i:
                decision = DecisionsFactory(dec=i)
                results.append(f'{decision.token:<45}-{paths[i]:<45}-Missing can_declare_war_on')

    ResultsReporter.report_results(results=results, message="Issues with decisions that start wars were encountered.")
