##########################
# Test script to check if blurry vanilla dds icons are used for armour variants
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
from ..imports.file_functions import open_text_file
import logging
FALSE_POSITITVES = ('ITA_basic_light_tank.dds', 'mex_basic_light_tank.dds', 'USA_basic_light_tank.dds',
                    'USA_basic_heavy_tank.dds', 'rom_basic_light_tank.dds',)


def test_check_dds_usage_tank_icons(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = {}
    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        if 'interface' in filename:                 # They can be used in general pool of icons
            continue
        if '00_tank_icons' in filename:                 # They can be used in general pool of icons
            continue
        text_file = open_text_file(filename)

        text_file_splitted = text_file.split('\n')
        for line in range(len(text_file_splitted)):
            current_line = text_file_splitted[line-1]
            if 'tank.dds"' in current_line and [i for i in FALSE_POSITITVES if i in current_line] == []:
                results[f'{os.path.basename(filename)}, line {line}'] = current_line.strip('\t')

    if results != {}:
        logging.warning("Usage of dds icons for armor variants encountered:")
        for i in results.items():
            logging.error(f'- [ ] {i}')
        logging.warning(f'{len(results)} times dds icons for armor variants are used.')
        raise AssertionError("DDS icons are used in armour variants! Check console output")
