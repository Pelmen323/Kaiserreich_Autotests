##########################
# Test script to check for decisions that generate wargoals if they have required parts
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = [
    'mex_reconquista_decision',
    'acw_federal_deadline_looms',
    'ser_attack_austria',
    'ott_alliance_with_azerbaijan',
    'cos_legion_del_caribe_attack',
    'per_sulaymaniyah_revolt',
    'sri_attack_italy',
    'ita_attack_italy',
    'srd_attack_sri',
    'srd_attack_italy',
    'pap_attack_sri',
    'pol_operation_parasol',
    'nee_liberate_states',
    'china_integrate_subjects',
    'qie_fangs_on_the_border',
    'shx_joint_strike_decision',
    'shx_joint_strike_attack_mission',
    'sik_remove_mongol_mission',
    'sqi_intervene_lep',
    'sqi_intervene_southeast',
    'sqi_intervene_southwest',
    'china_integration_timer',
    'pol_found_intermarium',
]


def test_check_decisions_wargoals(test_runner: object):
    # Part 1 - get the dict of all decisions
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    results = []

    for i in decisions:
        if 'create_wargoal' in i or 'declare_war_on = {' in i:
            decision = DecisionsFactory(dec=i)
            if decision.token in FALSE_POSITIVES:
                continue
            # 1 - Does the remove_effect have clear_decision_attack_AI?
            if decision.remove_effect:
                if "clear_decision_attack_ai" not in decision.remove_effect:
                    results.append(f'{decision.token}, {paths[i]} - Missing "clear_decision_attack_ai" in "remove_effect"')
                elif "imminent_war" in decision.remove_effect:
                    results.append(f'{decision.token}, {paths[i]} - imminent_war flag and "clear_decision_attack_ai" in "remove_effect" at the same time')

            # 2 - Does the complete_effect have setup_decision_attack_AI?
            if decision.complete_effect:
                if "setup_decision_attack_ai" not in decision.complete_effect:
                    results.append(f'{decision.token}, {paths[i]} - Missing "setup_decision_attack_ai" in "complete_effect"')
                elif "imminent_war" in decision.complete_effect:
                    results.append(f'{decision.token}, {paths[i]} - imminent_war flag and "setup_decision_attack_ai" in "complete_effect" at the same time')

            # 3 - Does the cancel_effect have clear_decision_attack_AI?
            if decision.cancel_effect:
                if "clear_decision_attack_ai" not in decision.cancel_effect:
                    results.append(f'{decision.token}, {paths[i]} - Missing "clear_decision_attack_ai" in "cancel_effect"')
                elif "imminent_war" in decision.cancel_effect:
                    results.append(f'{decision.token}, {paths[i]} - imminent_war flag and "clear_decision_attack_ai" in "cancel_effect" at the same time')

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

            # 7. Notifications
            if decision.complete_effect:
                if "warning event" not in decision.complete_effect and "kr.political.30" not in decision.complete_effect:
                    results.append(f'{decision.token}, {paths[i]} - The decision doesnt contain notification for a target. If it is - add #warning event comment to complete_effect section"')

            if decision.days_remove:
                if decision.days_remove > 50 and "set_country_flag = { flag = imminent_war days = " + str(decision.days_remove) not in decision.complete_effect:
                    results.append(f'{decision.token}, {paths[i]} - The decision is removed more than in 50 days but doesnt have custom imminent_war flag setup')

                if decision.days_remove < 25:
                    results.append(f'{decision.token}, {paths[i]} - The decision is removed in {decision.days_remove} days, 25 days is a minimum')
    # Part 2 - throw the error if entity is duplicated
    ResultsReporter.report_results(results=results, message="Issues with decisions that start wars were encountered. Check console output")
