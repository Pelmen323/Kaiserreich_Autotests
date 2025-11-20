##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import re
import os
from pathlib import Path
from charset_normalizer import detect

from test_classes.generic_test_class import FileOpener


def detect_encoding(filename):
    with open(filename, "rb") as f:
        raw_data = f.read()
        return detect(raw_data)["encoding"]


def test_division_composition_parser(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_names = str(Path(test_runner.full_path_to_mod) / "common" / "units" / "names_divisions") + "/"
    filepath_loc = str(Path(test_runner.full_path_to_mod) / "localisation" / "english" / "KR_common" / "division namelists l_english.yml")
    dict_names = {}

    for filename in glob.iglob(filepath_names + "**/*.txt", recursive=True):
        # if any([i for i in lst if i in filename]) is True:
        #     continue
        text_file = FileOpener.open_text_file(filename, lowercase=False)

        if '\tname = "' in text_file:
            tag = os.path.basename(filename)[:3]
            text_file_new = text_file
            pattern_matches = re.findall(r'^(\tname = \"(.*?)\")', text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                file_encoding = detect_encoding(filename)
                for match in pattern_matches:
                    whole_match = match[0]
                    print(whole_match)
                    name = match[1]
                    print(name)
                    replacement_key = 'div_' + tag + '_' + name.replace('(', '').replace(')', '').replace(' ', '_').replace('-', '_').replace("'", '').replace(".", '_').lower()
                    dict_names[replacement_key] = name

                    text_file_new = text_file_new.replace(f'"{name}"', replacement_key)
                    with open(filename, "w", encoding=file_encoding) as text_file_write:
                        text_file_write.write(text_file_new)

    with open(filepath_loc, "a", encoding="utf-8-sig") as text_file_write:
        for key, value in dict_names.items():
            text_file_write.write(f'\n {key}: "{value}"')
