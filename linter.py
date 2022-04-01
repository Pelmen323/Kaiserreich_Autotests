import glob
import re
from test_classes.generic_test_class import FileOpener, DataCleaner
from core.runner import TestRunner
FILES_TO_SKIP = ['localisation', 'interface', 'gfx', 'map', 'common\\units', 'names']


def replace_string(filename, pattern, replace_with):
    text_file = FileOpener.open_text_file(filename, lowercase=False)
    text_file_fixed = re.sub(pattern=pattern, repl=replace_with, string=text_file)

    with open(filename, 'w', encoding='utf-8') as text_file_write:
        text_file_write.write(text_file_fixed)


def lint_kaiserreich(username, mod_name):
    runner = TestRunner(username, mod_name)
    filepath_common = f'{runner.full_path_to_mod}common\\'
    print(filepath_common)
    for filename in glob.iglob(filepath_common + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        replace_string(filename=filename, pattern='(?<=[\\w_"={}])  (?=[\\w_"={}])', replace_with=' ')
        replace_string(filename=filename, pattern='=\\b', replace_with='= ')
        replace_string(filename=filename, pattern='\\b=', replace_with=' =')
        replace_string(filename=filename, pattern='(?<=[\\w_"={}])  (?=[\\w_"={}])', replace_with=' ')
        replace_string(filename=filename, pattern=' \\n', replace_with='\\n')


if __name__ == '__main__':
    lint_kaiserreich(username="VADIM", mod_name="Kaiserreich Dev Build")
