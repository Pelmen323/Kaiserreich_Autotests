##########################
# Test script to check if history files have both DLC and non-DLC checks for each DLC. It usually means that, while DLC/non-dlc techs are added, their counterparts are not
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from pathlib import Path

from test_classes.generic_test_class import FileOpener, ResultsReporter

armor_techs = {
    "gwtank": "gwtank_chassis",
    "basic_light_tank": "basic_light_tank_chassis",
    "improved_light_tank": "improved_light_tank_chassis",
    "advanced_light_tank": "advanced_light_tank_chassis",
    "basic_medium_tank": "basic_medium_tank_chassis",
    "improved_medium_tank": "improved_medium_tank_chassis",
    "advanced_medium_tank": "advanced_medium_tank_chassis",
    "basic_heavy_tank": "basic_heavy_tank_chassis",
    "improved_heavy_tank": "improved_heavy_tank_chassis",
    "advanced_heavy_tank": "advanced_heavy_tank_chassis",
    "super_heavy_tank": "super_heavy_tank_chassis",
    "land_cruiser_armor": "land_cruiser_chassis",
    "main_battle_tank": "main_battle_tank_chassis",
    "amphibious_tank": "amphibious_tank_chassis",
}

aircraft_techs = {
    "early_fighter": "iw_small_airframe",
    "early_bomber": "iw_medium_airframe",
    "fighter1": "basic_small_airframe",
    "tactical_bomber1": "basic_medium_airframe",
    "strategic_bomber1": "basic_large_airframe",
    "naval_bomber1": "air_torpedoe_1",
}


def test_history_dlc_techs(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "history" / "countries") + "/"
    results = []
    nsb_techs = [armor_techs[i] for i in armor_techs]
    non_nsb_techs = [i for i in armor_techs]
    bba_techs = [aircraft_techs[i] for i in aircraft_techs]
    non_bba_techs = [i for i in aircraft_techs]

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)
        f = os.path.basename(filename)

        test_map = {"nsb": [non_nsb_techs, nsb_techs, armor_techs], "bba": [non_bba_techs, bba_techs, aircraft_techs]}

        for t in test_map:
            dlc_name = t
            non_dlc_list = test_map[t][0]
            dlc_list = test_map[t][1]
            linked_dict = test_map[t][2]
            for i in non_dlc_list:
                if f"{i} = 1" in text_file:
                    if f"has_dlc_{dlc_name} = no" not in text_file:
                        results.append(f"{f} - has non-{dlc_name} techs but no non-{dlc_name} DLC check")
                    if f"{linked_dict[i]} = 1" not in text_file:
                        results.append(f"{f} - has non-{dlc_name} tech {i} but its {dlc_name} counterpart {linked_dict[i]} is missing")
                elif f"{linked_dict[i]} = 1" in text_file:
                    results.append(f"{f} - has {dlc_name} tech {linked_dict[i]} but its non_{dlc_name} counterpart {i} is missing")

            for i in dlc_list:
                if f"{i} = 1" in text_file:
                    if f"has_dlc_{dlc_name} = no" not in text_file:
                        results.append(f"{f} - has {dlc_name} techs but no {dlc_name} DLC check")

    ResultsReporter.report_results(results=results, message="Issues with DLC techs in history files were encountered.")
