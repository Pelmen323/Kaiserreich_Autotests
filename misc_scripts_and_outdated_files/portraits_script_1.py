import glob
import re

from ..test_classes.generic_test_class import FileOpener
from ..test_classes.characters_class import Characters


def test_convert_portraits_lines(test_runner):
    portraits_dict = {}
    pattern_civilian = r'\t\t\tcivilian = \{.*?\}'
    pattern_army = r'\t\t\tarmy = \{.*?\}'

    filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters'
    filepath_to_portraits = f'{test_runner.full_path_to_mod}interface\\kaiserreich\\portraits'

    characters = Characters.get_all_characters(test_runner=test_runner, return_paths=False, lowercase=False)

    # Check every character
    for char in characters:
        # print(char)
        char_name = re.findall('^\\t(.+) =', char)[0]
        char_tag = char_name[:3]
        civ_portraits = re.findall(pattern_civilian, char, flags=re.DOTALL | re.MULTILINE)
        army_portraits = re.findall(pattern_army, char, flags=re.DOTALL | re.MULTILINE)

        # Generate variables and extract portraits path
        for i in [[civ_portraits, "civilian"], [army_portraits, "army"]]:
            portraits_string = i[0]
            portraits_key = i[1]
            if portraits_string != []:
                portraits_string = portraits_string[0]
                if "small" in portraits_string and "GFX" not in portraits_string:
                    small_portrait_path = re.findall('small = (.*)', portraits_string)[0]
                    small_portrait_var_name = f'GFX_portrait_{char_name}_{portraits_key}_small'
                    portraits_dict[small_portrait_var_name] = [char_tag, small_portrait_path]

                if "large" in portraits_string and "GFX" not in portraits_string:
                    large_portrait_path = re.findall('large = (.*)', portraits_string)[0]
                    large_portrait_var_name = f'GFX_portrait_{char_name}_{portraits_key}_large'
                    portraits_dict[large_portrait_var_name] = [char_tag, large_portrait_path]

    # print(portraits_dict.items())
    # Override char files
    for filename in glob.iglob(filepath_to_characters + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        for key, value in portraits_dict.items():
            if value[1] in text_file:
                text_file = FileOpener.open_text_file(filename, lowercase=False)
                text_file_new = text_file.replace(value[1], key)
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)

    # Group dict by tag before creating gfx files
    portraits_dict_grouped_by_tag = {}
    for key, value in portraits_dict.items():
        portraits_dict_grouped_by_tag[value[0]] = []
    for key, value in portraits_dict.items():
        portraits_dict_grouped_by_tag[value[0]].append([key, value[1]])

    # Create GFX files or update them
    for key, value in portraits_dict_grouped_by_tag.items():
        generated_string = ''.join(['\tspriteType = {\n\t\tname = "' + gfx_name + '"\n\t\ttexturefile = ' + gfx_path + '\n\t}\n' for gfx_name, gfx_path in value])
        finalized_generated_string = 'spriteTypes = {\n\n' + generated_string + '\n}\n'

        list_of_gfx_files = [i for i in glob.iglob(filepath_to_portraits + "**/*.gfx", recursive=True)]
        expected_filename = f'{key}_portraits.gfx'
        new_filename = f'{filepath_to_portraits}\\{expected_filename}'
        with open(new_filename, 'w', encoding="utf-8") as new_file:
            new_file.write(finalized_generated_string)
