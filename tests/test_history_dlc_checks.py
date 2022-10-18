##########################
# Test script to check if history files have both DLC and non-DLC checks for each DLC. It usually means that, while DLC/non-dlc techs are added, their counterparts are not
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


def test_check_history_files_armor_techs(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}history\\countries\\'
    results = {}
    os.chdir(filepath)

    for filename in glob.glob("*.txt"):
        text_file = FileOpener.open_text_file(filename)

        non_nsb_limit = text_file.count('limit = { not = { has_dlc_nsb = yes } }')
        nsb_limit = text_file.count('limit = { has_dlc_nsb = yes }')
        non_mtg_limit = text_file.count('limit = { not = { has_dlc_mtg = yes } }')
        mtg_limit = text_file.count('limit = { has_dlc_mtg = yes }')
        non_bba_limit = text_file.count('limit = { not = { has_dlc_bba = yes } }')
        bba_limit = text_file.count('limit = { has_dlc_bba = yes }')

        gwtank = text_file.count("gwtank = 1")
        basic_light_tank = text_file.count("basic_light_tank = 1")
        basic_heavy_tank = text_file.count("basic_heavy_tank = 1")

        gwtank_chassis = text_file.count("gwtank_chassis = 1")
        basic_light_tank_chassis = text_file.count("basic_light_tank_chassis = 1")
        basic_heavy_tank_chassis = text_file.count("basic_heavy_tank_chassis = 1")

        sum_of_nsb_techs = gwtank_chassis + basic_light_tank_chassis + basic_heavy_tank_chassis
        sum_of_non_nsb_techs = gwtank + basic_light_tank + basic_heavy_tank

        if sum_of_nsb_techs != sum_of_non_nsb_techs:
            results[f'{os.path.basename(filename)}, armor_techs'] = f'Expected nsb- and non-nsb armor techs num to be equal, got ({sum_of_nsb_techs}) nsb techs and ({sum_of_non_nsb_techs} non-nsb techs:\
                {gwtank_chassis} + {basic_light_tank_chassis} + {basic_heavy_tank_chassis} vs\
                    {gwtank} + {basic_light_tank} + {basic_heavy_tank})'

        if sum_of_nsb_techs > 0 and nsb_limit == 0:
            results[f'{os.path.basename(filename)}, missing dlc limit'] = 'Missing NSB dlc limit!'
        if sum_of_non_nsb_techs > 0 and non_nsb_limit == 0:
            results[f'{os.path.basename(filename)}, missing non-dlc limit'] = 'Missing non-NSB dlc limit!'

        if nsb_limit > 0 and non_nsb_limit == 0:
            results[f'{os.path.basename(filename)}, DLC'] = 'Expected both nsb- and non-nsb dlc limits to be present. NSB is present, non-NSB is not present'
        elif nsb_limit == 0 and non_nsb_limit > 0:
            results[f'{os.path.basename(filename)}, DLC'] = 'Expected both nsb- and non-nsb dlc limits to be present. NSB is not present, non-NSB is present'

        if mtg_limit > 0 and non_mtg_limit == 0:
            results[f'{os.path.basename(filename)}, DLC'] = 'Expected both mtg- and non-mtg dlc limits to be present. MTG is present, non-MTG is not present'
        elif mtg_limit == 0 and non_mtg_limit > 0:
            results[f'{os.path.basename(filename)}, DLC'] = 'Expected both mtg- and non-mtg dlc limits to be present. MTG is not present, non-MTG is present'

        if bba_limit > 0 and non_bba_limit == 0:
            results[f'{os.path.basename(filename)}, DLC'] = 'Expected both bba- and non-bba dlc limits to be present. BBA is present, non-BBA is not present'
        elif bba_limit == 0 and non_bba_limit > 0:
            results[f'{os.path.basename(filename)}, DLC'] = 'Expected both bba- and non-bba dlc limits to be present. BBA is not present, non-BBA is present'

    ResultsReporter.report_results(results=results, message="Issues with DLCs in history files were encountered. Check console output")
