##########################
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener
from ..test_classes.characters_class import Characters
from ..core.runner import TestRunner
import glob
import os
import shutil


def add_missing_small_portraits(test_runner):
    """Function to:
    1. Check all characters and detect if they are unit leaders
    2. Check if unit leaders have small portraits links
    3. Create small portrait links for those unit leaders
    4. Copy large portraits in specified advisors folders for later conversion to small portraits

    Args:
        test_runner (_type_): test runner obj that contains filepath
    """
    characters, paths = Characters.get_all_characters(test_runner=test_runner, lowercase=False, return_paths=True)
    results = []
    results2 = {}
    backslash_char = "\\"

    for char in characters:
        char_name = None
        unit_leader_role = any([char.count('field_marshal =') > 0, char.count('corps_commander =') > 0, char.count('navy_leader =') > 0])
        try:
            char_name = re.findall('name = (\\w*)', char)[0]
        except Exception:
            results.append((char, paths[char], "Missing char name"))
            continue
        if unit_leader_role:
            pattern_matches = re.findall('portraits = \\{.*army = \\{.*small =.*\\}.*\\}', char.replace("\n", "").replace('\t', ""))
            if len(pattern_matches) < 1:
                try:
                    char_tag = char_name[:3]
                    is_missing_army_portraits_section = False
                    small_path_write = f'"gfx/interface/advisors/{char_tag}/{char_name}.png"'
                    small_path = small_path_write.strip('"')
                    small_path_paste = f"C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\{small_path.replace('/', backslash_char)}"
                    large_portrait_to_copy_raw = re.findall('army = {\n\t\t\t\tlarge = (.*)', char)
                    if large_portrait_to_copy_raw == []:
                        large_portrait_to_copy_raw = re.findall('civilian = {\n\t\t\t\tlarge = (.*)', char)[0]
                        is_missing_army_portraits_section = True
                    else:
                        large_portrait_to_copy_raw = large_portrait_to_copy_raw[0]
                    if "/Generic/" in large_portrait_to_copy_raw:
                        continue
                    large_portrait_to_copy_stripped = large_portrait_to_copy_raw.strip('"')
                    large_portrait_to_copy_path = f"C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\{large_portrait_to_copy_stripped.replace('/', backslash_char)}"

                    source_path_dir = ('C:\\Users\\VADIM\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\gfx\\interface\\advisors\\'+char_tag)
                    if os.path.exists(source_path_dir) is False:
                        os.mkdir(source_path_dir)
                    shutil.copyfile(large_portrait_to_copy_path, small_path_paste)
                    if is_missing_army_portraits_section:
                        str_to_insert = f"portraits = {{\n\t\t\tarmy = {{\n\t\t\t\tsmall = {small_path_write}\n\t\t\t}}\n\t\t\tcivilian = {{\n\t\t\t\tlarge = {large_portrait_to_copy_raw}"
                        string_to_replace = f'portraits = {{\n\t\t\tcivilian = {{\n\t\t\t\tlarge = {large_portrait_to_copy_raw}'
                    else:
                        str_to_insert = f"army = {{\n\t\t\t\tsmall = {small_path_write}\n\t\t\t\tlarge = {large_portrait_to_copy_raw}"
                        string_to_replace = f'army = {{\n\t\t\t\tlarge = {large_portrait_to_copy_raw}'
                    results2[string_to_replace] = str_to_insert
                except Exception as ex:
                    print(ex)
                    print(char)
                    continue

    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    characters = {}
    # Get all existing characters and apply changes
    for filename in glob.iglob(path_to_character_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file_non_lower(filename)
        for key, value in results2.items():
            if key in text_file:
                text_file = text_file.replace(key, value)

        with open(filename, 'w', encoding='utf-8') as text_file_write:
            text_file_write.write(text_file)

if __name__ == '__main__':
    test_runner = TestRunner(username="Vadzim", mod_name="Kaiserreich Dev Build")
    add_missing_small_portraits(test_runner=test_runner)
