import glob
import os
import re

from test_classes.generic_test_class import FileOpener
from pathlib import Path


class Traits:

    @classmethod
    def get_all_traits(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/unit_leaders and return the list with all traits code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if traits code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with traits code and dict with traits filenames
            else - list: list with traits code
        """
        filepath_to_traits = str(Path(test_runner.full_path_to_mod) / "common" / "unit_leader") + "/"
        found_files = False
        traits = []
        paths = {}

        for filename in glob.iglob(filepath_to_traits + "**/*.txt", recursive=True):
            found_files = True
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = re.findall(r"^\t\w.*? = \{.*?^\t\}", text_file, flags=re.MULTILINE | re.DOTALL)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    traits.append(match)
                    paths[match] = os.path.basename(filename)

        assert found_files, f"No .txt files found matching pattern: {filepath_to_traits}"
        assert len(traits) != 0
        if return_paths:
            return (traits, paths)
        else:
            return traits

    @classmethod
    def get_traits_names_from_specified_category(cls, test_runner, category: str = "all", lowercase: bool = True) -> list:
        """Parse all files in common/unit_leaders and return the list with all traits names from specified category

        Args:
            test_runner (_type_): test runner obj
            category (str, optional): specify the category of traits. Defaults to all
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
        Returns:
            list: list with traits code
        """
        traits = Traits.get_all_traits(test_runner=test_runner, lowercase=lowercase)
        traits_list = []
        for trait in traits:
            name = re.findall(r"^\t(.+) =", trait)[0]
            trait_type = re.findall(r"\ttype = (.*)", trait)[0]
            parent_traits = re.findall(r"\tany_parent = \{(.*)\}.*", trait) if "any_parent" in trait else []

            traits_list.append([name, trait_type, parent_traits])

        if category == "all":
            traits_to_return = traits_list
        elif category == "general":
            traits_to_return = [i for i in traits_list if "land" in i[1] or "corps_commander" in i[1]]
        elif category == "field_marshal":
            traits_to_return = [i for i in traits_list if "field_marshal" in i[1]]
        elif category == "all_land":
            traits_to_return = [i for i in traits_list if "land" in i[1] or "corps_commander" in i[1] or "field_marshal" in i[1]]
        elif category == "navy":
            traits_to_return = [i for i in traits_list if "navy" in i[1]]
        elif category == "operative":
            traits_to_return = [i for i in traits_list if "operative_traits" in i[1]]
        else:
            raise ValueError(f"Unsupported category requested - {traits_to_return}")

        assert len(traits_list) != 0
        return traits_to_return
