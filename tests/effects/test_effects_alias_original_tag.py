##########################
# Test script to check if tag alias is used with original tag. As for 1.12.8, they can't be safely used with "original_tag"
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re

from test_classes.generic_test_class import FileOpener, ResultsReporter


def test_alias_original_tag(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_aliases = f'{test_runner.full_path_to_mod}common\\country_tag_aliases\\tag_aliases.txt'
    results = []

    text_file = FileOpener.open_text_file(filepath_aliases, lowercase=False)
    tag_aliases = re.findall("^(...) = \\{", text_file, flags=re.MULTILINE)

    for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if 'original_tag =' in text_file:
            for i in tag_aliases:
                if f'original_tag = {i}' in text_file:
                    results.append((f'original_tag = {i}', filename.split("Kaiserreich Dev Build\\")[1]))

    ResultsReporter.report_results(results=results, message="Tag alias is used with original tag. Use tag = xxx instead")
