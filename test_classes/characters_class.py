import glob
import os
import re

from data.advisor_traits import genius_traits, special_theorists_traits
from test_classes.generic_test_class import FileOpener
from pathlib import Path


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
        filepath_to_characters  = str(Path(test_runner.full_path_to_mod) / 'common' / 'characters')
        characters = []
        paths = {}

        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            pattern_matches = re.findall('((?<=\n)\t\\w.* = \\{.*\n(.|\n*?)*\n\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
                    characters.append(match)
                    paths[match] = os.path.basename(filename)

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
        characters_names = []
        characters_names_paths = {}
        for char in characters:
            name = re.findall('^\\t(.+) =', char)[0]
            characters_names.append(name)       # get all char names
            characters_names_paths[name] = paths[char]

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
        advisors = []
        paths = {}

        for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            if "characters" in filename or 'add_advisor_role = {' in text_file:
                pattern_matches = re.findall('^(\\t*?)advisor = \\{(.*?^)\\1\\}', text_file, flags=re.DOTALL | re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[1]
                        advisors.append(match)
                        paths[match] = os.path.basename(filename)

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
        advisors = []
        paths = {}

        for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            if 'add_advisor_role = {' in text_file:
                pattern_matches = re.findall('^(\\t*?)add_advisor_role = \\{(.*?^)\\1\\}', text_file, flags=re.DOTALL | re.MULTILINE)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[1]
                        advisors.append(match)
                        paths[match] = os.path.basename(filename)

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
        if path is None:
            filepath_to_traits = str(Path(test_runner.full_path_to_mod) / 'common' / 'country_leader' / f'KR_{trait_type}_traits.txt')
        else:
            filepath_to_traits = path
        traits = []

        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file(filepath_to_traits, lowercase=False)

        pattern_matches = re.findall('((?<=\n)\t\\w* = \\{)', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                match = match[1:-4]
                traits.append(match)

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
        if path is None:
            filepath_to_traits = str(Path(test_runner.full_path_to_mod) / 'common' / 'country_leader' / f'KR_{trait_type}_traits.txt')
        else:
            filepath_to_traits = path
        traits = []

        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file(filepath_to_traits, lowercase=False)

        pattern_matches = re.findall('((?<=\n)\\t\\w* = \\{.*\n(.|\n*?)*\\n\\t\\})', text_file)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                traits.append(match[0])

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
        list_to_return = []
        if trait_type == "army":
            for i in adv_code:
                if "experience_gain_army" in i:
                    list_to_return.append(re.findall('\t(.*) = \\{', i)[0])

        elif trait_type == "navy":
            for i in adv_code:
                if "experience_gain_navy" in i or 'naval_doctrine_cost_factor' in i:
                    list_to_return.append(re.findall('\t(.*) = \\{', i)[0])

        elif trait_type == "air":
            for i in adv_code:
                if "experience_gain_air" in i:
                    list_to_return.append(re.findall('\t(.*) = \\{', i)[0])

        return list_to_return


class Advisors:
    def __init__(self, adv: str) -> None:
        # Idea_token
        try:
            self.token = re.findall('idea_token = (.+)', adv)[0]
        except IndexError:
            self.token = None

        # Role of the advisor
        self.slot = re.findall('slot = (\\w+)', adv)[0]
        self.military_role = any([adv.count('slot = army_chief') == 1, adv.count('slot = navy_chief') == 1, adv.count('slot = air_chief') == 1, adv.count('slot = high_command') == 1, adv.count('slot = theorist') == 1])
        self.chief_role = any([adv.count('slot = army_chief') == 1, adv.count('slot = navy_chief') == 1, adv.count('slot = air_chief') == 1])
        self.hc_role = adv.count('slot = high_command') == 1
        self.theorist_role = adv.count('slot = theorist') == 1
        self.special_theorist = False
        self.political_role = adv.count('slot = political_advisor') == 1
        self.sic_role = adv.count('slot = second_in_command') == 1
        self.unknown_role = any([self.military_role, self.political_role, self.sic_role]) is False

        # Ledger
        self.has_ledger_slot = adv.count('ledger =') > 0
        if self.has_ledger_slot:
            self.ledger_slot = re.findall('ledger = (\\w+)', adv)[0]
        else:
            self.ledger_slot = None

        # Theorists
        if self.theorist_role:
            for i in special_theorists_traits:
                if i in adv:
                    self.special_theorist = True
                    break

        # Cost
        self.has_defined_cost = len(re.findall('\\bcost =', adv)) > 0
        if self.has_defined_cost:
            try:
                self.cost = int(re.findall('cost = (\\d+)', adv)[0])
            except Exception:
                self.cost = -1
        elif self.theorist_role:
            self.cost = 100
        elif self.political_role:
            self.cost = 150
        elif self.military_role:
            self.cost = 50
        else:
            self.cost = -1

        # SIC things
        self.sic_has_correct_removal_cost = adv.count('can_be_fired = no') == 1

        # Not already_hired
        self.has_not_already_hired = adv.count('not_already_hired_except_as') > 0
        if self.has_not_already_hired:
            self.not_already_hired_slot = re.findall(r'not_already_hired_except_as = (\w+)', adv)

        # Traits
        self.traits = []
        traits_code = re.findall(r'traits = \{(.*?)\}', adv, flags=re.MULTILINE | re.DOTALL)[0]
        traits_code = traits_code.replace('\n', ' ').replace('\t', '').strip().split(' ')
        for trait in traits_code:
            self.traits.append(trait)

        # Advisor_level - military
        self.military_trait_lvl = None
        if len([i for i in self.traits if '_1' in i]) > 0 and self.military_role:
            self.military_trait_lvl = "specialist"
        if len([i for i in self.traits if '_2' in i]) > 0 and self.military_role:
            self.military_trait_lvl = "expert"
        if (len([i for i in self.traits if '_3' in i]) > 0 or len([i for i in self.traits if i in genius_traits]) > 0) and self.military_role:
            self.military_trait_lvl = "genius"
        if self.military_role and self.military_trait_lvl is None:
            self.military_trait_lvl = "specialist"
