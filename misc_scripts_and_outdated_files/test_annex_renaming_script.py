import glob
import re

from test_classes.generic_test_class import FileOpener


def test_main(test_runner):
    path_to_triggers = f'{test_runner.full_path_to_mod}common\\scripted_triggers\\'
    storage_dict = {}
    pattern = r'#.*annexation_(.*?)\ncan_release_(\d+)'

    for filename in glob.iglob(path_to_triggers + "**/*.txt", recursive=True):
        if "Annexation triggers" in filename:
            text_file = FileOpener.open_text_file(filename, lowercase=False)
            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    storage_dict[match[0]] = match[1]

    for filename in glob.iglob(test_runner.full_path_to_mod + "**/*.txt", recursive=True):
        if "Annexation triggers" not in filename:
            text_file = FileOpener.open_text_file(filename, lowercase=False)
            text_file_new = text_file
            OVERRIDE = False
            for i in storage_dict.keys():
                pattern = r'annexation_' + i + r'\b(?![\$\w_])'
                match = re.findall(pattern, text_file)
                if len(match) > 0:
                    OVERRIDE = True
                    text_file_new = re.sub(pattern, f'annexation_{storage_dict[i]}', text_file_new)

            if OVERRIDE:
                with open(filename, 'w', encoding="utf-8") as text_file_write:
                    text_file_write.write(text_file_new)

    for filename in glob.iglob(test_runner.full_path_to_mod + "**/*.yml", recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file
        OVERRIDE = False
        for i in storage_dict.keys():
            pattern = r'annexation_' + i + r'\b(?![\$\w_])'
            match = re.findall(pattern, text_file)
            if len(match) > 0:
                OVERRIDE = True
                text_file_new = re.sub(pattern, f'annexation_{storage_dict[i]}', text_file_new)

        if OVERRIDE:
            with open(filename, 'w', encoding="utf-8-sig") as text_file_write:
                text_file_write.write(text_file_new)
