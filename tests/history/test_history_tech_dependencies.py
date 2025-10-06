##########################
# Test script to check if depending techs are not added in history files
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter

aircraft_techs_dependencies = {
    # BBA checks
    "iw_small_airframe": ["engines_1", "aa_lmg"],
    "basic_small_airframe": ["engines_2"],
    "iw_medium_airframe": ["early_bombs"],
    "engines_2": ["basic_small_airframe"],
    # BBA to legacy checks
    "photo_reconnaisance": ["scout_plane1"],
    # Legacy to BBA checks
    "CAS1": ["early_bombs"],
    "cv_early_fighter": ["early_ship_hull_carrier"],
}


def test_history_tech_dependencies(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "history" / "countries") + "/"
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        f = os.path.basename(filename)

        for i in aircraft_techs_dependencies:
            dependency_list = aircraft_techs_dependencies[i]
            if f"{i} = 1" in text_file:
                for d in dependency_list:
                    if f"{d} = 1" not in text_file:
                        results.append(f"{f} - has tech {i} but its counterpart {d} is missing")

    ResultsReporter.report_results(results=results, message="Issues with DLC techs in history files were encountered.")
