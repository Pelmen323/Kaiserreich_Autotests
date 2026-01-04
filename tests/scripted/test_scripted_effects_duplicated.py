##########################
# Test script to check duplicated scripted effects
# By Pelmen, https://github.com/Pelmen323
##########################
from collections import Counter

from test_classes.scripted_effects_class import ScriptedEffects, ScriptedEffectFactory
from test_classes.generic_test_class import ResultsReporter


def test_scripted_effects_duplicated(test_runner: object):
    all_effects_code = ScriptedEffects.get_all_scripted_effects(test_runner=test_runner)
    all_effects_names = [ScriptedEffectFactory(i).id for i in all_effects_code]
    all_effects_counter = Counter(all_effects_names)
    results = [i for i in all_effects_counter if all_effects_counter[i] > 1]

    ResultsReporter.report_results(results=results, message="Duplicated scripted effects found.")
