import glob
import os
import re

from test_classes.generic_test_class import FileOpener
from pathlib import Path


def extract_value(obj, s: str, tab: str, lines: int = 2) -> str:
    if lines == 1:
        return re.findall(p1l(s), obj)[0] if f"\n{tab}{s} =" in obj else False
    elif lines > 1:
        return re.findall(pml(s), obj, flags=re.DOTALL | re.MULTILINE)[0][1] if f"\\n{tab}{s} =" in obj else False


def p1l(s: str):
    return r"\t+" + s + r" = (\S*)"


def pml(s: str):
    return r"(\t+)" + s + r" = (\{([^\n]*|.*?^\1)\})"


class Characters:

    @classmethod
    def get_all_characters(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/characters and return the list with all characters code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if characters code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with characters code and dict with characters filenames
            else - list: list with characters code
        """
        filepath_to_characters = Path(test_runner.full_path_to_mod) / "common" / "characters"
        path_pattern = str(filepath_to_characters / "**/*.txt")
        pattern = re.compile(r"((?<=\n)\t\w.* = \{.*\n(.|\n*?)*\n\t\})")
        found_files = False
        characters = []
        paths = {}

        for filename in glob.iglob(path_pattern, recursive=True):
            found_files = True
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    assert "name =" in match, f'character should always have "name" argument - {match}'
                    characters.append(match)
                    paths[match] = os.path.basename(filename)

        assert found_files, f"No .txt files found matching pattern: {path_pattern}"
        assert len(characters) != 0

        if return_paths:
            return (characters, paths)
        else:
            return characters

    @classmethod
    def get_all_characters_names(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/characters and return the list with all characters names

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if characters names are returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with characters names and dict with characters filenames
            else - list: list with characters names
        """
        characters, paths = Characters.get_all_characters(test_runner=test_runner, lowercase=lowercase, return_paths=True)
        pattern = re.compile(r"^\t(.+) =")
        characters_names = []
        characters_names_paths = {}
        for char in characters:
            name = re.findall(pattern, char)[0]
            characters_names.append(name)  # get all char names
            characters_names_paths[name] = paths[char]

        assert len(characters_names) != 0

        if return_paths:
            return (characters_names, characters_names_paths)
        else:
            return characters_names

    @classmethod
    def get_all_advisors(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in common/characters and return the list with all advisors code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if advisors code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with advisors code and dict with advisors filenames
            else - list: list with advisors code
        """
        filepath = test_runner.full_path_to_mod
        pattern = re.compile(r"^(\t*?)advisor = \{(.*?^)\1\}", flags=re.DOTALL | re.MULTILINE)
        found_files = False
        advisors = []
        paths = {}

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            found_files = True
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if "characters" in filename or "add_advisor_role = {" in text_file:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[1]
                        advisors.append(match)
                        paths[match] = os.path.basename(filename)

        assert found_files, f"No .txt files found matching pattern: {filepath}"
        assert len(advisors) != 0

        if return_paths:
            return (advisors, paths)
        else:
            return advisors

    @classmethod
    def get_all_add_advisor_effects(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list[str]:
        """Parse all files in common/characters and return the list with all advisors code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if advisors code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with advisors code and dict with advisors filenames
            else - list: list with advisors code
        """
        filepath = test_runner.full_path_to_mod
        pattern = re.compile(r"^(\t*?)add_advisor_role = \{(.*?^)\1\}", flags=re.DOTALL | re.MULTILINE)
        found_files = False
        advisors = []
        paths = {}

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            found_files = True
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if "add_advisor_role = {" in text_file:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[1]
                        advisors.append(match)
                        paths[match] = os.path.basename(filename)

        assert found_files, f"No .txt files found matching pattern: {filepath}"
        assert len(advisors) != 0

        if return_paths:
            return (advisors, paths)
        else:
            return advisors

    @classmethod
    def get_advisors_traits(cls, test_runner, trait_type: str = None, lowercase: bool = True, path: str = None) -> list[str]:
        """Parse common\\country_leader\\xxx.txt and return the list with all advisor traits

        Args:
            test_runner (_type_): Contains filepaths
            trait_type (str): Str - any of (second_in_command, political_advisor, high_command, theorist, air_chief, army_chief, navy_chief)
            lowercase (bool): if returned str is lowercase or not
            path(str): optional path to file with traits

        Returns:
            list[str]: all traits from a file (only traits names)
        """
        filepath_to_traits = str(Path(test_runner.full_path_to_mod) / "common" / "country_leader" / f"KR_{trait_type}_traits.txt") if path is None else path
        traits = []

        text_file = FileOpener.open_text_file(filepath_to_traits, lowercase=lowercase)
        pattern_matches = re.findall(r"((?<=\n)\t\w*? = \{)", text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[1:-4]
                traits.append(match)

        assert len(traits) != 0
        return traits

    @classmethod
    def get_advisors_traits_code(cls, test_runner, trait_type: str = None, lowercase: bool = True, path: str = None) -> list[str]:
        """Parse common\\country_leader\\xxx.txt and return the list with all advisor traits code

        Args:
            test_runner (_type_): Contains filepaths
            trait_type (str): Str - any of (second_in_command, political_advisor, high_command, theorist, air_chief, army_chief, navy_chief)
            lowercase (bool): if returned str is lowercase or not
            path(str): optional path to file with traits

        Returns:
            list[str]: all traits code from a file
        """
        filepath_to_traits = str(Path(test_runner.full_path_to_mod) / "common" / "country_leader" / f"KR_{trait_type}_traits.txt") if path is None else path
        traits = []

        text_file = FileOpener.open_text_file(filepath_to_traits, lowercase=lowercase)
        pattern_matches = re.findall(r"((?<=\n)\t\w* = \{.*\n(.|\n*?)*\n\t\})", text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                traits.append(match[0])

        assert len(traits) != 0
        return traits

    @classmethod
    def get_hc_specified_advisor_traits(cls, test_runner, trait_type: str = None, lowercase: bool = True, path: str = None) -> list[str]:
        """Parse common\\country_leader\\xxx.txt and return the list with all advisor traits

        Args:
            test_runner (_type_): Contains filepaths
            trait_type (str): Str - any of (army, navy, air)
            lowercase (bool): if returned str is lowercase or not
            path(str): optional path to file with traits

        Returns:
            list[str]: all traits from a file (only traits names)
        """
        adv_code = Characters.get_advisors_traits_code(test_runner=test_runner, trait_type="high_command")
        pattern = re.compile(r"\t(.*) = \{")
        list_to_return = []
        if trait_type == "army":
            for i in adv_code:
                if "experience_gain_army" in i:
                    list_to_return.append(re.findall(pattern, i)[0])

        elif trait_type == "navy":
            for i in adv_code:
                if "experience_gain_navy" in i or "naval_doctrine_cost_factor" in i:
                    list_to_return.append(re.findall(pattern, i)[0])

        elif trait_type == "air":
            for i in adv_code:
                if "experience_gain_air" in i:
                    list_to_return.append(re.findall(pattern, i)[0])

        assert len(list_to_return) != 0
        return list_to_return


class Advisors:
    def __init__(self, adv: str) -> None:
        # Tabulation used
        self.tab = t = re.findall(r"\n(\t*?)slot =", adv)[0]
        # Advisor properties
        self.slot = extract_value(adv, "slot", t, 1)
        self.token = extract_value(adv, "idea_token", t, 1)
        self.name = extract_value(adv, "name", t, 1)
        self.desc = extract_value(adv, "desc", t, 1)
        self.ledger_slot = extract_value(adv, "ledger", t, 1)
        self.traits_line = extract_value(adv, "traits", t)
        self.modifier = extract_value(adv, "modifier", t)
        self.research_bonus = extract_value(adv, "research_bonus", t)
        self.allowed = extract_value(adv, "allowed", t)
        self.available = extract_value(adv, "available", t)
        self.visible = extract_value(adv, "visible", t)
        self.cost = extract_value(adv, "cost", t, 1)
        self.can_be_fired = extract_value(adv, "can_be_fired", t, 1)
        self.on_add = extract_value(adv, "on_add", t)
        self.on_remove = extract_value(adv, "on_remove", t)
        self.ai_will_do = extract_value(adv, "ai_will_do", t)

        # Custom advisor properties
        military_chief_slots = ["army_chief", "navy_chief", "air_chief"]
        military_role_slots = military_chief_slots + ["high_command", "theorist"]
        self.military_role = any([adv.count(f"slot = {i}") == 1 for i in military_role_slots])
        self.chief_role = any([adv.count(f"slot = {i}") == 1 for i in military_chief_slots])
        self.sic_role = adv.count("slot = second_in_command") == 1
        self.hc_role = adv.count("slot = high_command") == 1
        self.not_already_hired = extract_value(adv, "not_already_hired_except_as", t, 1)

        # Traits
        self.traits = []
        traits_code = re.findall(r"traits = \{(.*?)\}", adv, flags=re.MULTILINE | re.DOTALL)[0]
        traits_code = traits_code.replace("\n", " ").replace("\t", "").strip().split(" ")
        for trait in traits_code:
            self.traits.append(trait)
