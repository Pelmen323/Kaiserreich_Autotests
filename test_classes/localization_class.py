import glob

from .generic_test_class import FileOpener


class Localization:

    @classmethod
    def get_all_loc_keys(cls, test_runner, lowercase: bool = True) -> dict:
        filepath = f'{test_runner.full_path_to_mod}localisation\\'
        results = []
        loc_dict = {}

        for filename in glob.iglob(filepath + '**/*.yml', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            lines_raw = text_file.split('\n')                                           # 1. Get list of all lines regardless of contents
            lines_raw = [i for i in lines_raw if ":" in i and "l_english:" not in i]    # 2. Form a list only with valid loc keys
            results += lines_raw

        for i in results:
            key = i[:i.index(":")].strip()                                                      # 3. Process the list with all loc and make it a dict
            value = i[i.index(":") + 2:].strip()
            loc_dict[key] = value

        return loc_dict
