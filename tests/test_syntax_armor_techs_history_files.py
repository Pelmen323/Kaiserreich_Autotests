##########################
# Test script to check if history files have equal number of NSB and non-NSB armor techs
# If the error occurs, this means that there are issues with armor techs
# Like non-NSB techs given when NSB enabled, or when limits are not properly set
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

        non_nsb_limit = text_file.count('limit = { not = { has_dlc = "no step back" } }')
        gwtank = text_file.count("gwtank = 1")
        basic_light_tank = text_file.count("basic_light_tank = 1")
        basic_heavy_tank = text_file.count("basic_heavy_tank = 1")

        nsb_limit = text_file.count('limit = { has_dlc = "no step back" }')
        gwtank_chassis = text_file.count("gwtank_chassis = 1")
        basic_light_tank_chassis = text_file.count("basic_light_tank_chassis = 1")
        basic_heavy_tank_chassis = text_file.count("basic_heavy_tank_chassis = 1")

        sum_of_nsb_techs = gwtank_chassis + basic_light_tank_chassis + basic_heavy_tank_chassis
        sum_of_non_nsb_techs = gwtank + basic_light_tank + basic_heavy_tank

        if sum_of_nsb_techs != sum_of_non_nsb_techs:
            results[f'{os.path.basename(filename)}, armor_techs'] = f'Expected nsb- and non-nsb armor techs num to be equal, got ({sum_of_nsb_techs}) nsb techs and ({sum_of_non_nsb_techs} non-nsb techs:\
                {gwtank_chassis} + {basic_light_tank_chassis} + {basic_heavy_tank_chassis} vs\
                    {gwtank} + {basic_light_tank} + {basic_heavy_tank})'
        if nsb_limit != non_nsb_limit:
            results[f'{os.path.basename(filename)}, dlc_limits'] = f'Expected nsb- and non-nsb dlc limits num to be equal, got ({nsb_limit}) nsb limits and ({non_nsb_limit} non-nsb limits)'
        if sum_of_nsb_techs > 0 and nsb_limit == 0:
            results[f'{os.path.basename(filename)}, missing dlc limit'] = 'Missing NSB dlc limit!'
        if sum_of_non_nsb_techs > 0 and non_nsb_limit == 0:
            results[f'{os.path.basename(filename)}, missing non-dlc limit'] = 'Missing non-NSB dlc limit!'

    ResultsReporter.report_results(results=results, message="Issues with starting armor techs were encountered. Check console output")
