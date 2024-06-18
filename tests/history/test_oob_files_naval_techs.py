##########################
# Test script to check for ship oobs with missing techs
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ...test_classes.generic_test_class import (
    FileOpener,
    ResultsReporter,
)

USA_TECHS = """
USA_starting_techs = {
    ### Starting Technologies ###
    set_technology = {
        ### General ###
        electronic_mechanical_engineering = 1

        ### Infantry ###
        infantry_weapons = 1
        infantry_weapons1 = 1
        tech_support = 1
        tech_engineers = 1
        tech_recon = 1
        motorised_infantry = 1
        gw_artillery = 1
        marines = 1
        tech_mountaineers = 1

        ### Trains ###
        basic_train = 1
    }

    ### Planes ###
    if = {
        limit = { has_dlc_bba = yes }
        set_technology = {
            iw_small_airframe = 1
            basic_small_airframe = 1
            iw_medium_airframe = 1
            basic_medium_airframe = 1
            engines_1 = 1
            engines_2 = 1
            aa_lmg = 1
            early_bombs = 1
            aircraft_construction = 1
        }
    }
    else = {
        set_technology = {
            early_fighter = 1
            cv_early_fighter = 1
            cv_naval_bomber1 = 1
            cv_CAS1 = 1
            naval_bomber1 = 1
            CAS1 = 1
            early_bomber = 1
        }
    }

    ### Tanks ###
    if = {
        limit = { has_dlc_nsb = yes }
        set_technology = {
            gwtank_chassis = 1
            basic_light_tank_chassis = 1
        }
        add_ideas = bureau_of_ordnance_spirit
    }
    else = {
        set_technology = {
            gwtank = 1
            basic_light_tank = 1
        }
    }

    ### Navy ###
    if = {
        limit = { has_dlc_mtg = yes }
        set_technology = {
            early_ship_hull_light = 1
            basic_ship_hull_light = 1
            early_ship_hull_cruiser = 1
            basic_ship_hull_cruiser = 1
            early_ship_hull_submarine = 1
            basic_ship_hull_submarine = 1
            cruiser_submarines = 1
            early_ship_hull_carrier = 1
            basic_ship_hull_carrier = 1
            early_ship_hull_heavy = 1
            basic_ship_hull_heavy = 1
            ship_hull_super_heavy = 1

            ## Modules##
            basic_depth_charges = 1
            basic_torpedo = 1
            basic_battery = 1
            basic_light_battery = 1
            basic_cruiser_armor_scheme = 1
            basic_heavy_armor_scheme = 1
            basic_medium_battery = 1
            basic_heavy_battery = 1
            sonar = 1
            basic_naval_mines = 1
            submarine_mine_laying = 1

            ### Transport ###
            mtg_transport = 1
        }
    }
    else = {
        set_technology = {
            early_destroyer = 1
            basic_destroyer = 1
            early_light_cruiser = 1
            basic_light_cruiser = 1
            early_submarine = 1
            basic_submarine = 1
            early_heavy_cruiser = 1
            basic_heavy_cruiser = 1
            early_battleship = 1
            basic_battleship = 1
            heavy_battleship = 1
            early_carrier = 1
            basic_carrier = 1

            ### Transport ###
            transport = 1
        }
    }
}
"""

RUS_TECHS = """
"""


def test_check_naval_oob_files(test_runner: object):
    path_to_oob_files = f'{test_runner.full_path_to_mod}history\\units\\'
    path_to_history_files = f'{test_runner.full_path_to_mod}history\\countries\\'
    oob_files = {}
    results = []
# Part 1 - get the dict of all oob files
    for filename in glob.iglob(path_to_oob_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)
        if "fleet = {" in text_file:
            temp_list = []
            pattern_matches = re.findall("equipment = \\{ (.*?) = \\{", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    temp_list.append(match)
            oob_files[os.path.basename(filename)[:-4]] = [os.path.basename(filename)[:3], set(temp_list)]

    for key in oob_files:
        if oob_files[key][0] in ["SOV", "WLS", "SCO", "CAN"]:
            continue

        if oob_files[key][0] in ["ACW", "USA", "CSA", "PSA", "TEX", "NEE"]:
            text_file = USA_TECHS

        else:
            for filename in glob.iglob(path_to_history_files + '**/*.txt', recursive=True):
                if f'{oob_files[key][0]} -' in filename:
                    text_file = FileOpener.open_text_file(filename)
                    break

        # DD
        if (x := 'ship_hull_light_1') in oob_files[key][1]:
            if (y := 'early_ship_hull_light = 1') not in text_file:            # and 'early_destroyer = 1') not in text_file
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_light_2') in oob_files[key][1]:
            if (y := 'basic_ship_hull_light = 1') not in text_file:            # and 'basic_destroyer = 1') not in text_file
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_light_3') in oob_files[key][1]:
            if (y := 'improved_ship_hull_light = 1') not in text_file:         # and 'improved_destroyer = 1') not in text_file
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_light_4') in oob_files[key][1]:
            if (y := 'advanced_ship_hull_light = 1') not in text_file:         # and 'advanced_destroyer = 1') not in text_file
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        # CA/CL
        if (x := 'ship_hull_cruiser_1') in oob_files[key][1]:
            if (y := 'early_ship_hull_cruiser = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_cruiser_2') in oob_files[key][1]:
            if (y := 'basic_ship_hull_cruiser = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_cruiser_3') in oob_files[key][1]:
            if (y := 'improved_ship_hull_cruiser = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_cruiser_4') in oob_files[key][1]:
            if (y := 'advanced_ship_hull_cruiser = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        # BB
        if (x := 'ship_hull_heavy_1') in oob_files[key][1]:
            if (y := 'early_ship_hull_heavy = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_heavy_2') in oob_files[key][1]:
            if (y := 'basic_ship_hull_heavy = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_heavy_3') in oob_files[key][1]:
            if (y := 'improved_ship_hull_heavy = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_heavy_4') in oob_files[key][1]:
            if (y := 'advanced_ship_hull_heavy = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_super_heavy_1') in oob_files[key][1]:
            if (y := 'ship_hull_super_heavy = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        # Carrier
        if (x := 'ship_hull_carrier_conversion_bb') in oob_files[key][1]:
            if (y := 'early_ship_hull_carrier = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_carrier_conversion_ca') in oob_files[key][1]:
            if (y := 'early_ship_hull_carrier = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_carrier_1') in oob_files[key][1]:
            if (y := 'basic_ship_hull_carrier = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_carrier_2') in oob_files[key][1]:
            if (y := 'improved_ship_hull_carrier = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_carrier_3') in oob_files[key][1]:
            if (y := 'advanced_ship_hull_carrier = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        # Sub
        if (x := 'ship_hull_submarine_1') in oob_files[key][1]:
            if (y := 'early_ship_hull_submarine = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_submarine_2') in oob_files[key][1]:
            if (y := 'basic_ship_hull_submarine = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_submarine_3') in oob_files[key][1]:
            if (y := 'improved_ship_hull_submarine = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        if (x := 'ship_hull_submarine_4') in oob_files[key][1]:
            if (y := 'advanced_ship_hull_submarine = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

        # Misc
        if (x := 'ship_hull_cruiser_panzerschiff') in oob_files[key][1]:
            if (y := 'panzerschiffe = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))
        if (x := 'ship_hull_torpedo_cruiser') in oob_files[key][1]:
            if (y := 'torpedo_cruiser_mtg = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))
        if (x := 'ship_hull_pre_dreadnought') in oob_files[key][1]:
            if (y := 'pre_dreadnoughts = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))
        if (x := 'ship_hull_cruiser_coastal_defense_ship') in oob_files[key][1]:
            if (y := 'coastal_defense_ships = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))
        if (x := 'ship_hull_cruiser_submarine') in oob_files[key][1]:
            if (y := 'cruiser_submarines = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))
        if (x := 'ship_hull_midget_submarine') in oob_files[key][1]:
            if (y := 'midget_submarines = 1') not in text_file:
                results.append((key, f"Tag spawns {x} but doesn't have {y} tech in history file"))

    ResultsReporter.report_results(results=results, message="Issues with ships OOBs were found. Check console output")
