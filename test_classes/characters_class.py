import glob
import re
import os
import logging
from ..test_classes.generic_test_class import FileOpener


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
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
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
    def get_all_advisors(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/characters and return the list with all advisors code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if advisors code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with advisors code and dict with advisors filenames
            else - list: list with advisors code
        """
        filepath_to_characters = f'{test_runner.full_path_to_mod}common\\characters\\'
        advisors = []
        paths = {}

        for filename in glob.iglob(filepath_to_characters + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            pattern_matches = re.findall('((?<=\n)\t\tadvisor = \\{.*\n(.|\n*?)*\n\t\t\\})', text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[0]
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
            filepath_to_traits = f'{test_runner.full_path_to_mod}common\\country_leader\\KR_{trait_type}_traits.txt'
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

        if trait_type == "second_in_command":
            traits.append('second_in_command_trait')
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
            filepath_to_traits = f'{test_runner.full_path_to_mod}common\\country_leader\\KR_{trait_type}_traits.txt'
        else:
            filepath_to_traits = path
        traits = []

        if lowercase:
            text_file = FileOpener.open_text_file(filepath_to_traits)
        else:
            text_file = FileOpener.open_text_file(filepath_to_traits, lowercase=False)

        pattern_matches = re.findall('((?<=\n)\t\w* = \{.*\n(.|\n*?)*\n\t\})', text_file)
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
                if "experience_gain_navy" in i:
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
            logging.error(f"Missing advisor token, {adv}")

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

        # Advisor_level - military
        self.specialist_lvl = adv.count('_1') == 1
        self.expert_lvl = adv.count('_2') == 1
        self.genius_lvl = adv.count('_3') == 1

        # Ledger
        self.has_ledger_slot = adv.count('ledger =') > 0
        if self.has_ledger_slot:
            self.ledger_slot = re.findall('ledger = (\\w+)', adv)[0]
        else:
            self.ledger_slot = None

        # Theorists
        special_theorists_traits = (
            'kr_mobile_warfare_expert',
            'kr_superior_firepower_expert',
            'kr_grand_battle_plan_expert',
            'kr_mass_assault_expert',
            'kr_victory_through_airpower',
            'kr_close_air_support_proponent',
            'kr_assault_aviation',
            'kr_naval_aviation_pioneer',
            'kr_grand_fleet_proponent',
            'kr_submarine_specialist',
            'fra_atomic_pair',
        )

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
        elif self.theorist_role or self.political_role:
            self.cost = 100
        elif self.military_role:
            self.cost = 50
        else:
            self.cost = -1

        # SIC things
        self.sic_has_correct_removal_cost = adv.count('removal_cost = -1') == 1

        # Not already_hired
        self.has_not_already_hired = adv.count('not_already_hired_except_as') > 0
        if self.has_not_already_hired:
            self.not_already_hired_slot = re.findall('not_already_hired_except_as = (\\w+)', adv)[0]

        # Traits
        self.traits = []
        if len(re.findall('traits = \\{\\n', adv)) > 0:
            pass
        else:
            traits_code = re.findall('traits = \\{(.+)\\}', adv)[0].strip()
            if ' ' in traits_code:
                self.traits = [i for i in traits_code.split(" ")]
            else:
                self.traits.append(traits_code)
