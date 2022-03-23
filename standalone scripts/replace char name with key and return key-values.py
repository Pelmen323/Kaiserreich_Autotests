##########################
# By Pelmen, https://github.com/Pelmen323
##########################
import re
from ..test_classes.generic_test_class import FileOpener, DataCleaner, ResultsReporter
from ..test_classes.characters_class import Characters
from ..core.runner import TestRunner
import glob


def replace_char_raw_names_with_keys(test_runner: object):
    characters, paths = Characters.get_all_characters_with_paths(test_runner=test_runner, lowercase=False)
    results = []
    results2 = []
    results3 = {}
            
    for char in characters:
        char_name = re.findall('name = (.*)', char)
        char_code = re.findall('^\t(\w.+) = \{', char)
        
        if 'name = "' in char:
            results.append((char_code, char_name, paths[char])) 
            results2.append(f'{"".join(char_code)}: {"".join(char_name)}')
            results3[f'{"".join(char_name)}'] = f'{"".join(char_code)}'
   
    print()
    for result in results2:
        print(result)
        
    path_to_character_files = f'{test_runner.full_path_to_mod}common\\characters\\'
    characters = {}

    for filename in glob.iglob(path_to_character_files + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file_non_lower(filename)
        for key, value in results3.items():
            if key in text_file:
                text_file = text_file.replace(key, value)

        with open(filename, 'w', encoding='utf-8') as text_file_write:
            text_file_write.write(text_file)
     
if __name__ == '__main__':
    test_runner = TestRunner(username="Vadzim", mod_name="Kaiserreich Dev Build")
    replace_char_raw_names_with_keys(test_runner=test_runner)
