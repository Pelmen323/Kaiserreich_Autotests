import glob
import re
import os

from ..test_classes.generic_test_class import FileOpener
from ..test_classes.characters_class import Characters


def test_convert_portraits_lines(test_runner):
    portraits_dict = {}
    gfx_override_dict = {}
    pattern_civilian = r'\t\t\tcivilian = \{.*?\}'
    pattern_army = r'\t\t\tarmy = \{.*?\}'

    filepath_to_gfx = f'{test_runner.full_path_to_mod}interface\\kaiserreich\\portraits'
    filepath_to_portraits = f'{test_runner.full_path_to_mod}gfx\\leaders\\'

    # characters = Characters.get_all_characters(test_runner=test_runner, return_paths=False, lowercase=False)

    # # Check every character
    # for char in characters:
    #     char_name = re.findall('^\\t(.+) =', char)[0]
    #     char_tag = char_name[:3]
    #     civ_portraits = re.findall(pattern_civilian, char, flags=re.DOTALL | re.MULTILINE)
    #     army_portraits = re.findall(pattern_army, char, flags=re.DOTALL | re.MULTILINE)

    #     # Generate variables and extract portraits path
    #     for i in [[civ_portraits, "civilian"], [army_portraits, "army"]]:
    #         portraits_string = i[0]
    #         portraits_key = i[1]
    #         if portraits_string != []:
    #             portraits_string = portraits_string[0]
    #             if "small" in portraits_string and "GFX" not in portraits_string:
    #                 small_portrait_path = re.findall('small = (.*)', portraits_string)[0]
    #                 small_portrait_var_name = f'GFX_portrait_{char_name}_{portraits_key}_small'
    #                 portraits_dict[small_portrait_var_name] = [char_tag, small_portrait_path]

    #             if "large" in portraits_string and "GFX" not in portraits_string:
    #                 large_portrait_path = re.findall('large = (.*)', portraits_string)[0]
    #                 large_portrait_var_name = f'GFX_portrait_{char_name}_{portraits_key}_large'
    #                 portraits_dict[large_portrait_var_name] = [char_tag, large_portrait_path]

    # Extract old and new portrait values
    for filename in glob.iglob(filepath_to_gfx + "**/*.gfx", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        sprites_list = re.findall(r'^\tspriteType = \{.*?^\t}', text_file, flags=re.DOTALL | re.MULTILINE)
        for sprite in sprites_list:
            name = re.findall(r'name = "GFX_portrait_(.*?)"', sprite)[0]
            if "_large" in name and "Generic" not in sprite:
                tag = name[:3]
                portrait_type = [i for i in ["civilian", "army", "navy"] if i in name][0]
                char_name = name[4:].replace("_civilian", "").replace("_army", "").replace("_navy", "").replace("_large", "")
                texturefile = re.findall(r'texturefile = (.*)', sprite)[0]
                if len([i for i in sprites_list if char_name in i and "_large" in i and texturefile not in re.findall(r'texturefile = (.*)', i)[0]]) > 0:
                    print(char_name)
                    new_filename = tag + '_' + char_name.lower() + '_' + portrait_type + '.png"'
                else:
                    new_filename = tag + '_' + char_name.lower() + '.png"'  
                texturefile_path, old_filename = re.findall(r'(.*/)([^/]*)"', texturefile)[0]
                new_path = texturefile_path + new_filename
                portraits_dict[old_filename] = new_filename[:-1]
                gfx_override_dict[texturefile] = new_path

    # Override gfx files
    for filename in glob.iglob(filepath_to_gfx + "**/*.gfx", recursive=True):
        override = False
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file
        for key, value in gfx_override_dict.items():
            if key in text_file:
                override = True
                text_file_new = text_file_new.replace(key, value)

        if override:
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file_new)

    for filename in glob.iglob(filepath_to_portraits + '**/*.png', recursive=True):
        # print(filename)
        # print(os.path.basename(filename))
        for key, value in portraits_dict.items():
            if key in os.path.basename(filename):
                os.rename(filename, filename.replace(os.path.basename(filename), value))
        # os.rename(filename, f'{filename[:-4]}_alt.png')
                    
        
        # for key, value in portraits_dict.items():
        #     if value[1] in text_file:
        #         text_file = FileOpener.open_text_file(filename, lowercase=False)
        #         text_file_new = text_file.replace(value[1], key)
        #         with open(filename, 'w', encoding="utf-8") as text_file_write:
        #             text_file_write.write(text_file_new)

    # Group dict by tag before creating gfx files
    # portraits_dict_grouped_by_tag = {}
    # for key, value in portraits_dict.items():
    #     portraits_dict_grouped_by_tag[value[0]] = []
    # for key, value in portraits_dict.items():
    #     portraits_dict_grouped_by_tag[value[0]].append([key, value[1]])

    # # Create GFX files or update them
    # for key, value in portraits_dict_grouped_by_tag.items():
    #     generated_string = ''.join(['\tspriteType = {\n\t\tname = "' + gfx_name + '"\n\t\ttexturefile = ' + gfx_path + '\n\t}\n' for gfx_name, gfx_path in value])
    #     finalized_generated_string = 'spriteTypes = {\n\n' + generated_string + '\n}\n'

    #     list_of_gfx_files = [i for i in glob.iglob(filepath_to_portraits + "**/*.gfx", recursive=True)]
    #     expected_filename = f'{key}_portraits.gfx'
    #     if [i for i in list_of_gfx_files if expected_filename in i] == []:
    #         new_filename = f'{filepath_to_portraits}\\{expected_filename}'
    #         with open(new_filename, 'w', encoding="utf-8") as new_file:
    #             new_file.write(finalized_generated_string)
    #     else:
    #         with open(expected_filename, 'w', encoding="utf-8") as new_file:
    #             new_file.write(finalized_generated_string)
