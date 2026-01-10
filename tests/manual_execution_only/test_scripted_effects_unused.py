##########################
# Test script to check if there are scripted effects that are not used via "xxx = yes"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import pytest

from test_classes.scripted_effects_class import ScriptedEffects
from test_classes.generic_test_class import (
    DataCleaner,
    FileOpener,
    ResultsReporter,
)


FALSE_POSITIVES = [
    'ger_bm_cardgame_',
    '_idea_effect',
    '_calculate',
]

FILES_TO_SKIP = [
    '00_',
    '01_AI',
    '01_Annexation',
]


@pytest.mark.skip("Low-prio test")
def test_scripted_effects_unused(test_runner: object):
    filepath = test_runner.full_path_to_mod
    scripted_effects = ScriptedEffects.get_all_scripted_effects_names(test_runner=test_runner, exclude_files=FILES_TO_SKIP)
    scripted_effects = set(DataCleaner.clear_false_positives_partial_match(input_iter=scripted_effects, false_positives=FALSE_POSITIVES))
    pattern = re.compile(r'(\w+)\s*=\s*yes')

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        if ' = yes' in text_file:
            pattern_matches = pattern.findall(text_file)
            for key in tuple(scripted_effects):
                if key in pattern_matches:
                    scripted_effects.remove(key)

    results = sorted(scripted_effects)
    ResultsReporter.report_results(results=results, message="Unused scripted effects were encountered.")
