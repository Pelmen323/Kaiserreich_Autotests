import glob
import os
import re

from test_classes.generic_test_class import FileOpener


class Variables:
    @classmethod
    def get_all_used_flags(cls, test_runner, lowercase: bool = True, flag_type: str = "country", return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all flags
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with flags and dict with filenames
            else - list: list with vars code
        """
        filepath = test_runner.full_path_to_mod
        flags = []
        paths = {}
        if flag_type not in ["country", "state", "global"]:
            raise ValueError("Unsupported flag value passed. Expected country, state, global")

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if f"has_{flag_type}_flag =" in text_file or f"modify_{flag_type}_flag =" in text_file:
                pattern_matches = re.findall(r"has_" + flag_type + r"_flag = ([^ \t\n]*)", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        flags.append(match)
                        paths[match] = os.path.basename(filename)

                pattern_matches = re.findall(r"[y|s]_" + flag_type + r"_flag = \{.*?flag = ([^ \t\n\}]*).*?\}", text_file, flags=re.MULTILINE | re.DOTALL)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        flags.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (flags, paths)
        else:
            return flags

    @classmethod
    def get_all_set_flags(cls, test_runner, lowercase: bool = True, flag_type: str = "country", return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all flags
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with flags and dict with filenames
            else - list: list with vars code
        """
        filepath = test_runner.full_path_to_mod
        flags = []
        paths = {}
        if flag_type not in ["country", "state", "global"]:
            raise ValueError("Unsupported flag value passed. Expected country, state, global")

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if f"set_{flag_type}_flag =" in text_file:
                pattern_matches = re.findall(r"set_" + flag_type + r"_flag = ([^ \t\n]*)", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        flags.append(match)
                        paths[match] = os.path.basename(filename)

                pattern_matches = re.findall(r"set_" + flag_type + r"_flag = \{.*?flag = ([^ \t\n\}]*).*?\}", text_file, flags=re.MULTILINE | re.DOTALL)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        flags.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (flags, paths)
        else:
            return flags

    @classmethod
    def get_all_cleared_flags(cls, test_runner, lowercase: bool = True, flag_type: str = "country", return_paths: bool = False) -> list[str]:
        """Parse all files return the list with all flags
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if vars code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with flags and dict with filenames
            else - list: list with vars code
        """
        filepath = test_runner.full_path_to_mod
        flags = []
        paths = {}
        if flag_type not in ["country", "state", "global"]:
            raise ValueError("Unsupported flag value passed. Expected country, state, global")

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if f"clr_{flag_type}_flag =" in text_file:
                pattern_matches = re.findall(r"clr_" + flag_type + r"_flag = ([^ \t\n]*)", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        flags.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (flags, paths)
        else:
            return flags
