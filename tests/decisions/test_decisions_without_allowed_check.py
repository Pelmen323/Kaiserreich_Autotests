##########################
# Test script to check for event targets that are cleared but not set
# By Pelmen, https://github.com/Pelmen323
##########################
from test_classes.generic_test_class import (
    DataCleaner,
    ResultsReporter,
)
from test_classes.decisions_class import Decisions, DecisionsFactory

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
    "war_exhaustion_mission",
    "ai_expand_air_bases",
    "kr_fight_for_independence",
]


def test_decisions_without_allowed_check(test_runner: object):
    dict_decisions_categories = Decisions.get_all_decisions_categories_with_child_decisions(test_runner=test_runner, lowercase=True)
    decisions = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True)
    decision_categories = Decisions.get_all_decisions_categories_with_code(test_runner=test_runner, lowercase=True)
    categories_without_allowed_trigger = []
    decisions_to_validate = []
    results = []

    # 1. Get all decision categories without allowed check:
    for cat, cat_code in decision_categories.items():
        if "allowed = {" not in cat_code:
            categories_without_allowed_trigger.append(cat)

    # 2. Extract decisions from categories above:
    for i in dict_decisions_categories:
        if i in categories_without_allowed_trigger:
            for decision in dict_decisions_categories[i]:
                decisions_to_validate.append(decision)

    # 3. Check if allowed argument is present in decisions above:
    for d in decisions:
        decision = DecisionsFactory(dec=d)
        if decision.token in decisions_to_validate:
            if not decision.allowed:
                results.append(decision.token)

    results = DataCleaner.clear_false_positives(input_iter=results, false_positives=FALSE_POSITIVES)
    ResultsReporter.report_results(results=results, message="Decisions without allowed trigger were encountered.")
