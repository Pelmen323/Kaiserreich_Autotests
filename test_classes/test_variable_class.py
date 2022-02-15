import logging
import re
import os


class TestClass:
    def open_text_file(self, filename: str) -> str:
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
                return text_file.read()
        except Exception as ex:
            logging.error(f"Skipping the file {filename}, {ex}")
            raise FileNotFoundError(f"Can't open the file {filename}")

    def extract_matches(self, source_file: str, regex_pattern: str, output_dict: dict, iter_with_filepath: str, len_to_cut: int = 0):
        pattern_matches = re.findall(regex_pattern, source_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[len_to_cut:].strip()
                output_dict[match] = 0
                iter_with_filepath[match] = os.path.basename(source_file)

    def clear_false_positives_dict(self, input_dict: dict, false_positives: tuple = ()):
        if len(false_positives) > 0:
            for key in false_positives:
                try:
                    input_dict.pop(key)
                except KeyError:
                    continue

    def skip_files(self, files_to_skip, filename):
        for file in files_to_skip:
            if file in filename:
                return True
