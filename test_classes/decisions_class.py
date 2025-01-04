import glob
import os
import re

from pathlib import Path
from test_classes.generic_test_class import FileOpener


def extract_value(obj, s: str, lines: int = 2) -> str:
    if lines == 1:
        return re.findall(p1l(s), obj)[0] if f"\t{s} =" in obj else False
    elif lines > 1:
        return re.findall(pml(s), obj, flags=re.DOTALL | re.MULTILINE)[0][1] if f"\t{s} =" in obj else False


def p1l(s: str) -> str:
    return r"\t+" + s + r" = (\S*)"


def pml(s: str) -> str:
    return r"(\t+)" + s + r" = (\{([^\n]*|.*?^\1)\})"


class Decisions:
    @classmethod
    def get_all_decisions(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse all files in common/decisions and return the list with all decisions code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if decisions code is returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with decisions code and dict with decisions filenames
            else - list: list with decisions code
        """
        filepath_to_decisions = str(Path(test_runner.full_path_to_mod) / "common" / "decisions")
        pattern = re.compile(r"^\t[^\t#]+ = \{.*?^\t\}", flags=re.MULTILINE | re.DOTALL)
        decisions = []
        paths = {}

        for filename in glob.iglob(filepath_to_decisions + "**/*.txt", recursive=True):
            if "categories" in filename:
                continue
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = re.findall(pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    decisions.append(match)
                    paths[match] = os.path.basename(filename)

        assert len(decisions) != 0
        if return_paths:
            return (decisions, paths)
        else:
            return decisions

    @classmethod
    def get_all_decisions_names(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse mod files and and return the list of all decisions names
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True

        Returns:
            list:  all decisions names in mod folder
        """

        decisions, paths = Decisions.get_all_decisions(test_runner=test_runner, lowercase=lowercase, return_paths=True)
        pattern = re.compile(r"^\t(.+) =")
        decisions_names = []
        decisions_names_paths = {}
        for d in decisions:
            name = re.findall(pattern, d)[0]
            decisions_names.append(name)
            decisions_names_paths[name] = paths[d]

        assert len(decisions_names) != 0
        if return_paths:
            return (decisions_names, decisions_names_paths)
        else:
            return decisions_names

    @classmethod
    def get_all_activated_decisions_names(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> list:
        """Parse mod files and and return the list of all activated decisions names
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True

        Returns:
            list:  all activated decisions names in mod folder
        """
        filepath = test_runner.full_path_to_mod
        pattern = re.compile(r"\bdecision = (\S+)")
        decisions = []
        paths = {}

        for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if "decision =" in text_file:
                pattern_matches = re.findall(pattern, text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        match = match[0]
                        decisions.append(match)
                        paths[match] = os.path.basename(filename)

        assert len(decisions) != 0
        if return_paths:
            return (decisions, paths)
        else:
            return decisions

    @classmethod
    def get_all_decisions_categories_with_code(cls, test_runner, lowercase: bool = True, return_only_categories: bool = False) -> dict:
        """Parse mod files and and return the dict of category: code of this category
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True

        Returns:
            dict: all decision categories and their code
        """
        filepath_to_categories = str(Path(test_runner.full_path_to_mod) / "common" / "decisions" / "categories")
        categories = {}
        category_pattern = re.compile(r"^\w* = \{.*?^\}", flags=re.DOTALL | re.MULTILINE)
        category_name_pattern = re.compile(r"^(.*) = \{")

        for filename in glob.iglob(filepath_to_categories + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            pattern_matches = re.findall(category_pattern, text_file)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    category_name = re.findall(category_name_pattern, match)[0]
                    assert category_name not in categories, f"Duplicated decision category {category_name} found"
                    categories[category_name] = match

        assert len(categories) != 0
        if return_only_categories:
            return list(categories.keys())
        return categories

    @classmethod
    def get_all_decisions_categories_with_child_decisions(cls, test_runner, lowercase: bool = True) -> dict:
        """Parse mod files and and return the dict of category: decisions of this category
        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True

        Returns:
            dict: all decision categories and decisions of those categories
        """
        filepath_to_decisions = str(Path(test_runner.full_path_to_mod) / "common" / "decisions")
        decision_categories = Decisions.get_all_decisions_categories_with_code(test_runner=test_runner, lowercase=lowercase, return_only_categories=True)
        categories_w_decisions_dict = {i: [] for i in decision_categories}
        decision_pattern = re.compile(r"^\t(\S+) = \{", flags=re.MULTILINE)

        for filename in glob.iglob(filepath_to_decisions + "**/*.txt", recursive=True):
            if "categories" in filename:
                continue
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            for category in decision_categories:
                if f"{category} = {{" in text_file:
                    pattern = r"^" + category + r" = \{.*?^\}"
                    pattern_matches = re.findall(pattern, text_file, flags=re.DOTALL | re.MULTILINE)
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            decision_name_pattern = re.findall(decision_pattern, match)
                            for i in decision_name_pattern:
                                categories_w_decisions_dict[category].append(i)

        assert len(categories_w_decisions_dict) != 0
        return categories_w_decisions_dict


class DecisionsFactory:
    def __init__(self, dec: str) -> None:
        # Decision properties
        self.token = re.findall(r"^\t*(.+) = \{", dec, flags=re.MULTILINE)[0]
        self.icon = extract_value(dec, "icon", 1)
        self.allowed = extract_value(dec, "allowed")
        self.available = extract_value(dec, "available")
        self.visible = extract_value(dec, "visible")

        self.cancel_effect = extract_value(dec, "cancel_effect")
        self.complete_effect = extract_value(dec, "complete_effect")
        self.remove_effect = extract_value(dec, "remove_effect")

        self.cancel_trigger = extract_value(dec, "cancel_trigger")
        self.cancel_if_not_visible = "cancel_if_not_visible = yes" in dec

        self.target_root_trigger = extract_value(dec, "target_root_trigger")
        self.target_trigger = extract_value(dec, "target_trigger")
        self.targets = extract_value(dec, "targets")
        self.target_array = extract_value(dec, "target_array", 1)

        self.war_with_on_remove = "war_with_on_remove =" in dec
        self.war_with_target_on_remove = "war_with_target_on_remove = yes" in dec
        self.war_with_target_on_complete = "war_with_target_on_complete = yes" in dec

        self.mission_subtype = "\tdays_mission_timeout =" in dec
        self.selectable_mission = "\tdays_mission_timeout =" in dec and "selectable_mission = yes" in dec
        self.ai_factor = extract_value(dec, "ai_will_do")

        self.custom_cost_trigger = extract_value(dec, "custom_cost_trigger")
        self.ai_hint_pp_cost = extract_value(dec, "ai_hint_pp_cost", 1)
        self.cost = extract_value(dec, "cost", 1)

        self.days_remove = extract_value(dec, "days_remove", 1)
        self.reversed = "reversed = yes" in dec
        try:
            self.days_remove = int(self.days_remove)
        except ValueError:
            self.days_remove = False
