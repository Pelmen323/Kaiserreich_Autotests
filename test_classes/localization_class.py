import glob
import re
from pathlib import Path

from .generic_test_class import FileOpener


class Localization:

    @classmethod
    def get_all_loc_keys(cls, test_runner, lowercase: bool = True, return_duplicated_keys: bool = False, return_keys_from_specific_file: str = False) -> dict:
        filepath = str(Path(test_runner.full_path_to_mod) / "localisation") + "/"
        results = []
        loc_dict = {}
        duplicated_loc_keys = []

        if not return_keys_from_specific_file:
            for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
                text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

                if "l_english" not in text_file:
                    continue

                lines_raw = text_file.split('\n')                                                                           # 1. Get list of all lines regardless of contents
                lines_raw = [i for i in lines_raw if ":" in i and "l_english:" not in i and i.strip(' ')[0] != "#"]         # 2. Form a list only with valid loc keys
                results += lines_raw
        else:
            text_file = FileOpener.open_text_file(return_keys_from_specific_file, lowercase=lowercase)

            lines_raw = text_file.split('\n')                                                                           # 1. Get list of all lines regardless of contents
            lines_raw = [i for i in lines_raw if ":" in i and "l_english:" not in i and i.strip(' ')[0] != "#" and i[1] != "#"]    # 2. Form a list only with valid loc keys
            results += lines_raw

        for i in results:
            key = i[:i.index(":")].strip()                                                                              # 3. Process the list with all loc and make it a dict
            value = i[i.index(":") + 2:].strip()
            if key in loc_dict.keys():
                duplicated_loc_keys.append(key)
            else:
                loc_dict[key] = value

        if return_duplicated_keys:
            return loc_dict, duplicated_loc_keys
        else:
            return loc_dict

    @classmethod
    def get_all_colors(cls, test_runner) -> list:
        filepath = Path(test_runner.full_path_to_mod) / "interface" / "core.gfx"

        text_file = FileOpener.open_text_file(filepath, lowercase=False)
        textcolors = re.findall(r'\ttextcolors = \{.*?^\t\}', text_file, flags=re.DOTALL | re.MULTILINE)[0]
        colors = re.findall(r'^\t\t(\w) =.*?\n', textcolors, flags=re.DOTALL | re.MULTILINE)

        return colors
