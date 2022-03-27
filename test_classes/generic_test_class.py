import logging
import re
import os
import glob


class FileOpener:
    '''
    Test class that hosts common file functions like opening text files
    '''
    @classmethod
    def open_text_file(cls, filename: str, lowercase: bool = True) -> str:
        """Opens and returns text file in utf-8-sig encoding

        Args:
            filename (str): text file to open
            lowercase (bool): defines if returned str is converted to lovercase or not. Default - True

        Raises:
            FileNotFoundError: if file is not found

        Returns:
            str: contents of the text file converted to lowercase
        """
        try:
            with open(filename, 'r', encoding='utf-8-sig') as text_file:      # 'utf-8-sig' is mandatory for UTF-8 w/BOM
                if lowercase:
                    return text_file.read().lower()
                else:
                    return text_file.read()
        except Exception as ex:
            logging.error(f"Skipping the file {filename}, {ex}")
            raise FileNotFoundError(f"Can't open the file {filename}")

    @classmethod
    def replace_all_keys_in_file_with_values(cls, path_to_files: str, dict_with_strings_to_replace: dict, lowercase: bool = True) -> None:
        """Parse all files in passed dictionary and replaces encountered keys with values from passed dict

        Args:
            path_to_files (str): path to folder with files to open
            dict_with_strings_to_replace (dict): dict with keys that represent the string to replace, and values to replace keys with
            lowercase (bool, optional): if opened files should be in lowercase. Defaults to True.
        """
        for filename in glob.iglob(path_to_files + '**/*.txt', recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)
            for key, value in dict_with_strings_to_replace.items():
                if key in text_file:
                    text_file = text_file.replace(key, value)

            with open(filename, 'w', encoding='utf-8') as text_file_write:
                text_file_write.write(text_file)


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
    def clear_false_positives(cls, input_iter: dict, false_positives: tuple = ()) -> dict:
        """Removes items from iterable

        Args:
            input_iter (dict): dict/list to remove items from
            false_positives (tuple, optional): iterable with items to remove. Defaults to ().

        Returns:
            dict: cleaned list/disc
        """
        if isinstance(input_iter, dict):
            if len(false_positives) > 0:
                for key in false_positives:
                    try:
                        input_iter.pop(key)
                    except KeyError:
                        continue
                return input_iter

        elif isinstance(input_iter, list):
            if len(false_positives) > 0:
                return [i for i in input_iter if i not in false_positives]

    @classmethod
    def skip_files(cls, files_to_skip: list, filename: str) -> bool:
        """Skip files in the list

        Args:
            files_to_skip (list): list with filenames
            filename (str): list with filenames

        Returns:
            bool: True if file should be skipped
        """
        for file in files_to_skip:
            if file in filename:
                return True


class ResultsReporter:
    @classmethod
    def report_results(cls, results: list, message: str, paths: dict = {}) -> None:
        """Report results and print them

        Args:
            results (list): iterable with results. If not empty - thr items are printed and error raised
            message (str): what to print as error message
            paths (dict, optional): dict with paths for tests that need filepaths printing. Defaults to {}.

        Raises:
            AssertionError: Raised if passed iterable is not empty
        """

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
