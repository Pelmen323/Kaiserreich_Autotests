##########################
# Test script to check if decisions have duplicated triggers
# By Pelmen, https://github.com/Pelmen323
##########################
from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.generic_test_class import ResultsReporter


def test_check_decisions_duplicated_triggers(test_runner: object):
    results = []
    decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=True, return_paths=True)
    decision_categories = Decisions.get_all_decisions_categories(test_runner=test_runner, lowercase=True)
    dict_decisions_categories = Decisions.get_decisions_categories_dict(test_runner=test_runner, lowercase=True)

    for i in decisions:
        decision = DecisionsFactory(dec=i)
        decision_category = [i for i in dict_decisions_categories.keys() if decision.token in dict_decisions_categories[i]][0]
        decision_category_code = decision_categories[decision_category][0]

        if decision.visible:
            visible_triggers = [i for i in decision.visible.replace('\t', '').split('\n') if len(i) > 8]

            # Category check
            for trigger in visible_triggers:
                if trigger in decision_category_code:
                    if "on_map_area" not in decision_category_code or decision_category_code.index("on_map_area") > decision_category_code.index(trigger):
                        results.append((decision.token, trigger, paths[i], "Visible and category"))

            if decision.allowed:
                allowed_triggers = [i for i in decision.allowed.replace('\t', '').split('\n') if len(i) > 8]

                for trigger in allowed_triggers:
                    if trigger in visible_triggers:
                        results.append((decision.token, trigger, paths[i], "Visible and Allowed"))

        if decision.available:
            available_triggers = [i for i in decision.available.replace('\t', '').split('\n') if len(i) > 8]

            # Category check
            for trigger in available_triggers:
                if trigger in decision_category_code:
                    if "on_map_area" not in decision_category_code or decision_category_code.index("on_map_area") > decision_category_code.index(trigger):
                        results.append((decision.token, trigger, paths[i], "Available and category"))

            if decision.allowed:
                allowed_triggers = [i for i in decision.allowed.replace('\t', '').split('\n') if len(i) > 8]

                for trigger in allowed_triggers:
                    if trigger in available_triggers:
                        results.append((decision.token, trigger, paths[i], "Available and Allowed"))

        if decision.visible:
            visible_triggers = [i for i in decision.visible.split('\n') if len(i) > 12]

            if decision.available:
                available_triggers = [i for i in decision.available.split('\n') if len(i) > 12]

                for trigger in visible_triggers:
                    if trigger in available_triggers:
                        results.append((decision.token, trigger.replace('\t', ''), paths[i], "Available and Visible"))

    ResultsReporter.report_results(results=sorted(set(results), key=lambda x: (x[2], x[0])), message="Possible performance improvements for decisions encountered. Check console output")
