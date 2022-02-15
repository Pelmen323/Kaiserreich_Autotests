import logging
import re
import os


class TestClass:
    '''
    Basic test class that hosts widely-used functions - work with text files, regex, clearing false-positives
    '''
    def open_text_file(self, filename: str) -> str:
        '''
        Opens and returns text file in utf-8-sig encoding
        '''
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
                return text_file.read()
        except Exception as ex:
            logging.error(f"Skipping the file {filename}, {ex}")
            raise FileNotFoundError(f"Can't open the file {filename}")

    def extract_matches(self, source_file: str, regex_pattern: str, output_dict: dict, iter_with_filepath: str, len_to_cut: int = 0):
        '''
        Function for simple extract and cut regex
        '''
        pattern_matches = re.findall(regex_pattern, source_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[len_to_cut:].strip()
                output_dict[match] = 0
                iter_with_filepath[match] = os.path.basename(source_file)

    def clear_false_positives_dict(self, input_dict: dict, false_positives: tuple = ()) -> dict:
        '''
        Function to clear and return dict\n
        Input - dict to clean and iterable with the items to exclude\n
        Output - cleaned dict
        '''
        if len(false_positives) > 0:
            for key in false_positives:
                try:
                    input_dict.pop(key)
                except KeyError:
                    continue
            return input_dict

    def skip_files(self, files_to_skip: list, filename: str) -> bool:
        '''
        Function to skip the file during iteration\n
        Input - str with filename, iterable with the items to skip\n
        Output - bool (True if the file should be skipped)
        '''
        for file in files_to_skip:
            if file in filename:
                return True
