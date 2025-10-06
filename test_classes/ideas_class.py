import glob
import os
import re
from pathlib import Path

from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import FileOpener


class Ideas:

    @classmethod
    def get_all_ideas(
        cls,
        test_runner,
        lowercase: bool = True,
        return_paths: bool = False,
        include_hidden_ideas: bool = True,
        include_country_ideas: bool = True,
        include_manufacturers: bool = True,
        include_laws: bool = False,
        include_army_spirits: bool = False,
        include_tank_manufacturers: bool = False,
        include_naval_manufacturers: bool = False,
        include_air_manufacturers: bool = False,
        include_materiel_manufacturers: bool = False,
        include_industrial_manufacturers: bool = False,
    ) -> tuple[list, dict]:
        """Parse all files in common/ideas and return the list with all ideas code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if ideas code is returned with dict that contains their filenames. Defaults to False.
            include_country_ideas (bool, optional): defines if ideas code includes country ideas. Defaults to True.
            include_manufacturers (bool, optional): defines if ideas code includes manufacturers ideas. Defaults to True.
            include_laws (bool, optional): defines if ideas code includes laws ideas. Defaults to False.
            include_army_spirits (bool, optional): defines if ideas code includes army spirits ideas. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with ideas code and dict with ideas filenames
            else - list: list with ideas code
        """
        filepath_to_ideas = str(Path(test_runner.full_path_to_mod) / "common" / "ideas") + "/"
        ideas = []
        paths = {}

        p1 = r" = \{.*\n((.|\n*?)*)\n\t\}"
        match_pattern = re.compile(r"(\t\t\w.* = \{.*\n(.|\n*?)*\n\t\t\})")
        for filename in glob.iglob(filepath_to_ideas + "**/*.txt", recursive=True):
            text_file = FileOpener.open_text_file(filename, lowercase=lowercase)

            if include_hidden_ideas:
                hidden_ideas_string = re.findall(r"\thidden_ideas" + p1, text_file)
                if len(hidden_ideas_string) > 0:
                    pattern_matches = re.findall(match_pattern, hidden_ideas_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_country_ideas:
                country_ideas_string = re.findall(r"\tcountry" + p1, text_file)
                if len(country_ideas_string) > 0:
                    pattern_matches = re.findall(match_pattern, country_ideas_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_manufacturers or include_industrial_manufacturers:
                # Industry
                industry_ideas_string = re.findall(r"\tindustrial_concern" + p1, text_file)
                if len(industry_ideas_string) > 0:
                    pattern_matches = re.findall(match_pattern, industry_ideas_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Materiel
            if include_manufacturers or include_materiel_manufacturers:
                materiel_manufacturer_string = re.findall(r"\tmateriel_manufacturer" + p1, text_file)
                if len(materiel_manufacturer_string) > 0:
                    pattern_matches = re.findall(match_pattern, materiel_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Tank
            if include_manufacturers or include_tank_manufacturers:
                tank_manufacturer_string = re.findall(r"\ttank_manufacturer" + p1, text_file)
                if len(tank_manufacturer_string) > 0:
                    pattern_matches = re.findall(match_pattern, tank_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Naval
            if include_manufacturers or include_naval_manufacturers:
                naval_manufacturer_string = re.findall(r"\tnaval_manufacturer" + p1, text_file)
                if len(naval_manufacturer_string) > 0:
                    pattern_matches = re.findall(match_pattern, naval_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Aircraft
            if include_manufacturers or include_air_manufacturers:
                aircraft_manufacturer_string = re.findall(r"\taircraft_manufacturer" + p1, text_file)
                if len(aircraft_manufacturer_string) > 0:
                    pattern_matches = re.findall(match_pattern, aircraft_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_laws:
                for i in ["economy", "trade_laws", "mobilization_laws"]:
                    laws_string = re.findall(r"\t" + i + p1, text_file)
                    if len(laws_string) > 0:
                        pattern_matches = re.findall(match_pattern, laws_string[0][0])
                        if len(pattern_matches) > 0:
                            for match in pattern_matches:
                                match = match[0]
                                ideas.append(match)
                                paths[match] = os.path.basename(filename)

            if include_army_spirits:
                for i in ["academy_spirit", "army_spirit", "division_command_spirit", "naval_academy_spirit", "navy_spirit", "naval_command_spirit", "air_force_spirit", "air_force_command_spirit"]:
                    spirit_string = re.findall(r"\t" + i + p1, text_file)
                    if len(spirit_string) > 0:
                        pattern_matches = re.findall(match_pattern, spirit_string[0][0])
                        if len(pattern_matches) > 0:
                            for match in pattern_matches:
                                match = match[0]
                                ideas.append(match)
                                paths[match] = os.path.basename(filename)

        if return_paths:
            return (ideas, paths)
        else:
            return ideas

    @classmethod
    def get_all_ideas_names(
        cls,
        test_runner,
        lowercase: bool = True,
        return_paths: bool = False,
        include_hidden_ideas: bool = True,
        include_country_ideas: bool = True,
        include_manufacturers: bool = True,
        include_characters_tokens: bool = True,
        include_laws: bool = False,
        include_army_spirits: bool = False,
    ) -> tuple[list, dict]:
        """Parse all files in common/ideas and return the list with all ideas code

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if ideas code is returned with dict that contains their filenames. Defaults to False.
            include_country_ideas (bool, optional): defines if ideas code includes country ideas. Defaults to True.
            include_manufacturers (bool, optional): defines if ideas code includes manufacturers ideas. Defaults to True.
            include_characters_tokens (bool, optional): defines if ideas code includes characters ideas. Defaults to True.
            include_laws (bool, optional): defines if ideas code includes laws ideas. Defaults to False.
            include_army_spirits (bool, optional): defines if ideas code includes army spirits ideas. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with ideas code and dict with ideas filenames
            else - list: list with ideas code
        """
        ideas, paths = Ideas.get_all_ideas(
            test_runner=test_runner,
            lowercase=lowercase,
            return_paths=True,
            include_hidden_ideas=include_hidden_ideas,
            include_country_ideas=include_country_ideas,
            include_manufacturers=include_manufacturers,
            include_laws=include_laws,
            include_army_spirits=include_army_spirits,
        )

        ideas_names = []
        ideas_names_paths = {}
        for idea in ideas:
            name = re.findall(r"^\t\t(.+) =", idea)[0]
            ideas_names.append(name)  # get all ideas names
            ideas_names_paths[name] = paths[idea]

        if include_characters_tokens:
            advisors, paths_characters = Characters.get_all_advisors(test_runner=test_runner, return_paths=True)
            for advisor_code in advisors:
                adv = Advisors(adv=advisor_code)
                ideas_names.append(adv.token)
                paths[adv.token] = paths_characters[advisor_code]

        if return_paths:
            return (ideas_names, ideas_names_paths)
        else:
            return ideas_names
