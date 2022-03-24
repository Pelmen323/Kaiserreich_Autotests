##########################
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener
from ..test_classes.characters_class import Characters
from ..core.runner import TestRunner
import glob


def replace_char_raw_names_with_keys(test_runner: object):
    """Function to:
    1. Check all characters and detect if their names are raw str
    2. Replace raw str with leys
    3. Print key: str pairs that should be added to loc files

    Args:
        test_runner (_type_): test runner obj that contains filepath
    """
    characters, paths = Characters.get_all_characters(test_runner=test_runner, lowercase=False, return_paths=True)
    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    results = []
    key_value_pairs_to_print = []
    lines_to_replace = {}

    # Generate lines to insert and to print
    for char in characters:
        char_name = re.findall('name = (.*)', char)
        char_code = re.findall('^\t(\\w.+) = \\{', char)

        if 'name = "' in char:
            results.append((char_code, char_name, paths[char]))
            key_value_pairs_to_print.append(f'{"".join(char_code)}: {"".join(char_name)}')
            lines_to_replace[f'{"".join(char_name)}'] = f'{"".join(char_code)}'

    # Print keys: values to manually insert into loc files
    print()
    for result in key_value_pairs_to_print:
        print(result)

    # Replace name lines with newly generated ones
    for filename in glob.iglob(path_to_character_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file_non_lower(filename)
        for key, value in lines_to_replace.items():
            if key in text_file:
                text_file = text_file.replace(key, value)

        with open(filename, 'w', encoding='utf-8') as text_file_write:
            text_file_write.write(text_file)


if __name__ == '__main__':
    test_runner = TestRunner(username="Vadzim", mod_name="Kaiserreich Dev Build")
    replace_char_raw_names_with_keys(test_runner=test_runner)
