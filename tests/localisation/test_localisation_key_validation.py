##########################
# Test script to check if `add_resistance` has a valid tooltip
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter
from test_classes.localization_class import Localization
from test_classes.gfx_class import GFX, GFXFactory
from test_classes.technologies_class import Technologies, TechFactory
from test_classes.buildings_class import Buildings, BuildFactory

FALSE_POSITIVES = [
    "ORIGINAL_TAG_IS",                       # Vanilla trigger w unusual name
    "GFX_news_event_india_protests"          # Vanilla GFX
]


def test_localisation_key_validation(test_runner: object):
    filepath = test_runner.full_path_to_mod
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner, lowercase=False)
    GFX_code = GFX.get_code(test_runner=test_runner, lowercase=False)
    tech_code = Technologies.get_code(test_runner=test_runner, lowercase=False)
    build_code = Buildings.get_code(test_runner=test_runner, lowercase=False)
    pattern = r"localization_key = ([^ \t\n]*)"
    results = []
    gfx_obj_names = [GFXFactory(i).name for i in GFX_code]
    tech_obj_names = [TechFactory(i).token for i in tech_code]
    build_obj_names = [BuildFactory(i).token for i in build_code]

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if "localization_key =" in text_file:
            pattern_matches = re.findall(pattern, text_file, flags=re.MULTILINE | re.DOTALL)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    k = match
                    if k not in loc_keys:
                        if '[' in k and ']' in k:
                            # scripted loc - skip for now
                            continue
                        elif k in gfx_obj_names:
                            # GFX reference - skip
                            continue
                        elif len(k) > 3 and k[0] == '"' and k[1:-1] in gfx_obj_names:
                            # GFX reference - skip
                            continue
                        elif 'GFX_' not in k and '"' in k:
                            # random inline bs
                            continue
                        elif "EFFECT_" in k or "TRIGGER_" in k:
                            # vanilla keys
                            continue
                        elif k in FALSE_POSITIVES:
                            continue
                        elif "tech_effect|" in k and any([i for i in tech_obj_names if f"|{i}" in k]):
                            continue
                        elif "building_state_modifier|" in k and any([i for i in build_obj_names if f"|{i}" in k]):
                            continue
                        elif "country_culture|" in k:
                            # country culture
                            continue

                        results.append(k)

    ResultsReporter.report_results(results=sorted(list(set(results))), message="Unable to find the listed loc keys in 'localization_key =' values")
