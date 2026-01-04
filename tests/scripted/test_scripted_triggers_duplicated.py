##########################
# Test script to check duplicated scripted triggers
# By Pelmen, https://github.com/Pelmen323
##########################
from collections import Counter

from test_classes.scripted_triggers_class import ScriptedTriggers, ScriptedTriggerFactory
from test_classes.generic_test_class import ResultsReporter


def test_scripted_triggers_duplicated(test_runner: object):
    all_triggers_code = ScriptedTriggers.get_all_scripted_triggers(test_runner=test_runner)
    all_triggers_names = [ScriptedTriggerFactory(i).id for i in all_triggers_code]
    all_triggers_counter = Counter(all_triggers_names)
    results = [i for i in all_triggers_counter if all_triggers_counter[i] > 1]

    ResultsReporter.report_results(results=results, message="Duplicated scripted triggers found.")
