##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
from pathlib import Path

from test_classes.generic_test_class import FileOpener

input_dict = {
    '9':6,
    '17':30,
    '25':2,
    '26':2,
    '28':5,
    '34':5,
    '42':60,
    '43':4,
    '44':1,
    '48':1,
    '54':8,
    '55':8,
    '60':8,
    '65':13,
    '66':12,
    '67':57,
    '70':2,
    '72':4,
    '74':12,
    '79':1,
    '80':1,
    '84':3,
    '101':1,
    '104':2,
    '107':4,
    '109':1,
    '113':1,
    '114':1,
    '119':2,
    '127':6,
    '128':13,
    '129':8,
    '130':51,
    '131':23,
    '132':33,
    '133':29,
    '135':1,
    '138':2,
    '140':1,
    '152':4,
    '155':3,
    '165':2,
    '166':3,
    '174':3,
    '180':2,
    '181':1,
    '219':16,
    '227':82,
    '261':13,
    '275':14,
    '284':2,
    '285':16,
    '300':4,
    '327':1,
    '333':1,
    '343':1,
    '344':2,
    '348':2,
    '356':5,
    '362':11,
    '367':8,
    '368':5,
    '369':56,
    '373':5,
    '375':11,
    '376':5,
    '380':4,
    '381':7,
    '382':7,
    '383':4,
    '388':7,
    '389':12,
    '395':34,
    '396':14,
    '404':6,
    '424':3,
    '432':1,
    '435':15,
    '459':2,
    '464':7,
    '470':5,
    '480':3,
    '481':1,
    '489':1,
    '493':6,
    '502':8,
    '506':1,
    '507':4,
    '521':4,
    '524':8,
    '526':4,
    '528':15,
    '533':1,
    '536':10,
    '537':2,
    '558':2,
    '569':16,
    '572':8,
    '577':4,
    '578':16,
    '610':1,
    '612':3,
    '614':2,
    '616':8,
    '621':8,
    '622':24,
    '627':2,
    '682':2,
    '716':11,
    '719':4,
    '723':2,
    '728':6,
    '731':1,
    '736':2,
    '760':1,
    '781':14,
    '793':6,
    '822':1,
    '857':3,
    '894':1,
    '924':7,
    '925':2,
    '929':88,
    '948':7,
    '957':55,
    '966':7,
    '975':160,
    '976':1,
    '978':12,
    '1003':1,
    '1016':2,
    '1021':4,
    '1029':2,
    '1051':3,
    '1061':5,
    '1072':19,
    '1081':2,
    '1088':2,
    '1089':2,
    '1100':4,
    '1106':2,
    '1110':3
}


def test_division_composition_parser(test_runner: object):
    filepath = str(Path(test_runner.full_path_to_mod) / "history" / "states") + "/"

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file
        override = False
        state_id = re.findall(r'	id = (\d*)', text_file)[0]
        if state_id in input_dict.keys():
            coal_value = str(input_dict[state_id])
            if "coal =" in text_file:
                existing_coal_value = re.findall(r'coal = (\d*)', text_file)[0]
                if existing_coal_value != coal_value:
                    override = True
                    text_file_new = text_file_new.replace(f'coal = {existing_coal_value}', f'coal = {coal_value}')

            else:
                if 'resources = {' in text_file:
                    existing_resource_section = re.findall(r'resources = \{.*?\}', text_file, re.MULTILINE | re.DOTALL)[0]
                    override = True
                    text_file_new = text_file_new.replace(existing_resource_section, existing_resource_section[:-1] + f'\tcoal = {coal_value}\n\t' + '}')
                else:
                    existing_provinces_section = re.findall(r'provinces = \{.*?\}', text_file, re.MULTILINE | re.DOTALL)[0]
                    override = True
                    text_file_new = text_file_new.replace(existing_provinces_section, 'resources = {\n\t\tcoal = ' + coal_value + '\n\t}\n\n\t' + existing_provinces_section)

        if override:
            with open(filename, 'w', encoding='utf-8') as text_file_write:
                text_file_write.write(text_file_new)
