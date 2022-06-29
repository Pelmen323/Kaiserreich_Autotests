import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener


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
        filepath_to_traits = f'{test_runner.full_path_to_mod}common\\unit_leader\\'
        traits = []
        paths = {}

        for filename in glob.iglob(filepath_to_traits + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            pattern_matches = re.findall('((?<=\n)\t\\w.* = \\{.*\n(.|\n*?)*\n\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    traits.append(match)
                    paths[match] = os.path.basename(filename)

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
        all_traits = []
        land_traits = []
        corps_commander_traits = []
        field_marshal_traits = []
        navy_traits = []
        operative_traits = []
        for trait in traits:
            name = re.findall('^\\t(.+) =', trait)[0]
            traits_line = re.findall('\\ttype =.*', trait)[0]

            if "all" in traits_line:
                all_traits.append(name)
            if "land" in traits_line:
                land_traits.append(name)
            if "corps_commander" in traits_line:
                corps_commander_traits.append(name)
            if "field_marshal" in traits_line:
                field_marshal_traits.append(name)
            if "navy" in traits_line:
                navy_traits.append(name)
            if "operative_traits" in traits_line:
                operative_traits.append(name)

        if category == "all":
            traits_to_return = all_traits + land_traits + corps_commander_traits + field_marshal_traits + navy_traits + operative_traits
        elif category == "general":
            traits_to_return = land_traits + corps_commander_traits
        elif category == "field_marshal":
            traits_to_return = field_marshal_traits
        elif category == "all_land":
            traits_to_return = land_traits + corps_commander_traits + field_marshal_traits
        elif category == "navy":
            traits_to_return = navy_traits
        elif category == "operative":
            traits_to_return = operative_traits
        else:
            raise ValueError(f"Unsupported category requested - {traits_to_return}")

        return traits_to_return
