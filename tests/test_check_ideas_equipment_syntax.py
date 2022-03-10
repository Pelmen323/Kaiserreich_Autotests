##########################
# Test script to check if invalid equipment syntax is used in ideas
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from ..test_classes.generic_test_class import FileOpener, DataCleaner
import logging


def test_check_ideas_equipment_syntax(test_runner: object):
    filepath = f'{test_runner.full_path_to_mod}common\\ideas'
    results = {}
    equipment_names = ('scout_plane = {',
'cv_fighter = {',
'heavy_fighter = {',
'jet_fighter = {',
'cas = {',
'cv_cas = {',
'nav_bomber = {',
'cv_nav_bomber = {',
'tac_bomber = {',
'jet_tac_bomber = {',
'strat_bomber = {',
'jet_strat_bomber = {',
'transport_plane = {',
'rocket_interceptor = {',
'guided_missile = {',
'suicide_craft = {',
'amphibious_armor = {',
'amphibious_light_armor = {',
'amphibious_medium_armor = {',
'amphibious_heavy_armor = {',
'amphibious_mechanized = {',
'anti_air = {',
'anti_air_brigade = {',
'mot_anti_air_brigade = {',
'anti_tank = {',
'anti_tank_brigade = {',
'mot_anti_tank_brigade = {',
'armored_car = {',
'artillery = {',
'rocket_artillery = {',
'artillery_brigade = {',
'mot_artillery_brigade = {',
'rocket_artillery_brigade = {',
'mot_rocket_artillery_brigade = {',
'motorized_rocket_brigade = {',
'battle_cruiser = {',
'battleship = {',
'cavalry = {',
'camelry = {',
'engineer = {',
'field_hospital = {',
'light_flame_tank = {',
'medium_flame_tank = {',
'heavy_flame_tank = {',
'heavy_armor = {',
'heavy_cruiser = {',
'infantry = {',
'bicycle_battalion = {',
'marine = {',
'mountaineers = {',
'paratrooper = {',
'motorized = {',
'mechanized = {',
'fake_intel_unit = {',
'penal_battalion = {',
'light_armor = {',
'light_cruiser = {',
'logistics_company = {',
'maintenance_company = {',
'medium_armor = {',
'military_police = {',
'modern_armor = {',
'railway_gun = {',
'recon = {',
'mot_recon = {',
'armored_car_recon = {',
'light_tank_recon = {',
'signal_company = {',
'light_sp_anti_air_brigade = {',
'medium_sp_anti_air_brigade = {',
'heavy_sp_anti_air_brigade = {',
'super_heavy_sp_anti_air_brigade = {',
'modern_sp_anti_air_brigade = {',
'light_sp_artillery_brigade = {',
'medium_sp_artillery_brigade = {',
'heavy_sp_artillery_brigade = {',
'super_heavy_sp_artillery_brigade = {',
'modern_sp_artillery_brigade = {',
'super_heavy_armor = {',
'light_tank_destroyer_brigade = {',
'medium_tank_destroyer_brigade = {',
'heavy_tank_destroyer_brigade = {',
'super_heavy_tank_destroyer_brigade = {',
'modern_tank_destroyer_brigade = {',
)
   
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename)

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            for equipment in equipment_names:
                if f'\t{equipment}' in current_line:
                    results[f'{os.path.basename(filename)}, line {line}'] = current_line.strip('\t')

    if results != {}:
        logging.warning("Invalid equipment syntax is used:")
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} errors found.')
        raise AssertionError("Invalid equipment syntax in ideas is used! Check console output")
