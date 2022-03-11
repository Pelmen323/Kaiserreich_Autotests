import logging
import re
import os


class FileOpener:
    '''
    Test class that hosts file functions - like opening text files
    '''
    @classmethod
    def open_text_file(cls, filename: str) -> str:
        '''
        Opens and returns text file in utf-8-sig encoding
        '''
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
                return text_file.read().lower()
        except Exception as ex:
            logging.error(f"Skipping the file {filename}, {ex}")
            raise FileNotFoundError(f"Can't open the file {filename}")

    @classmethod        
    def open_text_file_non_lower(cls, filename: str) -> str:
        '''
        Opens and returns text file in utf-8-sig encoding
        '''
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
                return text_file.read()
        except Exception as ex:
            logging.error(f"Skipping the file {filename}, {ex}")
            raise FileNotFoundError(f"Can't open the file {filename}")

class IterableParser:
    @classmethod
    def extract_matches(cls, source_file: str, regex_pattern: str, output_dict: dict, iter_with_filepath: str, len_to_cut: int = 0):
        '''
        Function for simple extract and cut regex
        '''
        pattern_matches = re.findall(regex_pattern, source_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[len_to_cut:].strip()
                output_dict[match] = 0
                iter_with_filepath[match] = os.path.basename(source_file)
                
class DataCleaner:
    @classmethod
    def clear_false_positives_dict(cls, input_dict: dict, false_positives: tuple = ()) -> dict:
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

    @classmethod
    def skip_files(cls, files_to_skip: list, filename: str) -> bool:
        '''
        Function to skip the file during iteration\n
        Input - str with filename, iterable with the items to skip\n
        Output - bool (True if the file should be skipped)
        '''
        for file in files_to_skip:
            if file in filename:
                return True


class ResultsReporter:
    @classmethod
    def report_results(cls, results: list, message: str, paths: dict = {}) -> None:
        '''
        Method to report results and print them
        Input - list with results, dict with paths (optional), error message
        Output - None
        '''
        
        if len(results) > 0:
            logging.warning("Following issues were encountered during test execution:")

            if isinstance(results, list):
                if paths == {}:
                    for i in results:
                        logging.error(f"- [ ] {i}")
                else:
                    for i in results:
                        logging.error(f"- [ ] {i}, - '{paths[i]}'")

            elif isinstance(results, dict):
                if paths == {}:
                    for i in results.items():
                        logging.error(f"- [ ] {i}")
                else:
                    for i in results.items():
                        logging.error(f"- [ ] {i}, - '{paths[i]}'")

            logging.warning(f"{len(results)} issues found")
            logging.warning(f"{message}")
            raise AssertionError(message)
