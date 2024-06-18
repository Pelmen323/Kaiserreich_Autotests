import glob
import os
import re

from test_classes.characters_class import Advisors, Characters
from test_classes.generic_test_class import FileOpener


class Ideas:

    @classmethod
    def get_all_ideas(cls, test_runner, lowercase: bool = True, return_paths: bool = False, include_hidden_ideas: bool = True, include_country_ideas: bool = True, include_manufacturers: bool = True, include_laws: bool = False, include_army_spirits: bool = False) -> tuple[list, dict]:
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
        filepath_to_ideas = f'{test_runner.full_path_to_mod}common\\ideas\\'
        ideas = []
        paths = {}

        for filename in glob.iglob(filepath_to_ideas + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            if include_hidden_ideas:
                hidden_ideas_string = re.findall('\\thidden_ideas = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(hidden_ideas_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', hidden_ideas_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_country_ideas:
                country_ideas_string = re.findall('\\tcountry = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(country_ideas_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', country_ideas_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_manufacturers:
                # Industry
                industry_ideas_string = re.findall('\\tindustrial_concern = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(industry_ideas_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', industry_ideas_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Materiel
                materiel_manufacturer_string = re.findall('\\tmateriel_manufacturer = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(materiel_manufacturer_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', materiel_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Tank
                tank_manufacturer_string = re.findall('\\ttank_manufacturer = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(tank_manufacturer_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', tank_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Naval
                naval_manufacturer_string = re.findall('\\tnaval_manufacturer = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(naval_manufacturer_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', naval_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # Aircraft
                aircraft_manufacturer_string = re.findall('\\taircraft_manufacturer = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(aircraft_manufacturer_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', aircraft_manufacturer_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_laws:
                economy_laws_string = re.findall('\\teconomy = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(economy_laws_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', economy_laws_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                trade_laws_string = re.findall('\\ttrade_laws = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(trade_laws_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', trade_laws_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                mobilization_laws_string = re.findall('\\tmobilization_laws = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(mobilization_laws_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', mobilization_laws_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

            if include_army_spirits:
                # academy_spirit
                academy_spirit_string = re.findall('\\tacademy_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(academy_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', academy_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # army_spirit
                army_spirit_string = re.findall('\\tarmy_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(army_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', army_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # division_command_spirit
                division_command_spirit_string = re.findall('\\tdivision_command_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(division_command_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', division_command_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # naval_academy_spirit
                naval_academy_spirit_string = re.findall('\\tnaval_academy_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(naval_academy_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', naval_academy_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # navy_spirit
                navy_spirit_string = re.findall('\\tnavy_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(navy_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', navy_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # naval_command_spirit
                naval_command_spirit_string = re.findall('\\tnaval_command_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(naval_command_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', naval_command_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # air_force_spirit
                air_force_spirit_string = re.findall('\\tair_force_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(air_force_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', air_force_spirit_string[0][0])
                    if len(pattern_matches) > 0:
                        for match in pattern_matches:
                            match = match[0]
                            ideas.append(match)
                            paths[match] = os.path.basename(filename)

                # air_force_command_spirit
                air_force_command_spirit_string = re.findall('\\tair_force_command_spirit = \\{.*\n((.|\n*?)*)\n\t\\}', text_file)
                if len(air_force_command_spirit_string) > 0:
                    pattern_matches = re.findall('(\t\t\\w.* = \\{.*\n(.|\n*?)*\n\t\t\\})', air_force_command_spirit_string[0][0])
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
    def get_all_used_ideas(cls, test_runner, lowercase: bool = True, return_paths: bool = False) -> tuple[list, dict]:
        """Parse all files in common/ideas and return the list with all used ideas names

        Args:
            test_runner (_type_): test runner obj
            lowercase (bool, optional): defines if returned list contains lowercase str or not. Defaults to True.
            return_paths (bool, optional): defines if ideas names are returned with dict that contains their filenames. Defaults to False.

        Returns:
            if return_paths - tuple[list, dict]: list with ideas names and dict with ideas filenames
            else - list: list with ideas names
        """
        filepath = test_runner.full_path_to_mod
        used_ideas = []
        paths = {}

        for filename in glob.iglob(filepath + '**/*.txt', recursive=True):
            if lowercase:
                text_file = FileOpener.open_text_file(filename)
            else:
                text_file = FileOpener.open_text_file(filename, lowercase=False)

            # No brackets
            if '_ideas =' in text_file:
                pattern_matches = re.findall("add_ideas = ([\\w':-]+)", text_file)
                pattern_matches += re.findall("remove_ideas = ([\\w':-]+)", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        used_ideas.append(match)
                        paths[match] = os.path.basename(filename)

            if '_idea =' in text_file:
                pattern_matches = re.findall("has_idea = ([\\w':-]+)", text_file)
                pattern_matches += re.findall("add_idea = ([\\w':-]+)", text_file)
                pattern_matches += re.findall("remove_idea = ([\\w':-]+)", text_file)
                pattern_matches += re.findall("add_timed_idea = .*idea = ([\\w':-]+).*", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        used_ideas.append(match)
                        paths[match] = os.path.basename(filename)

            # Brackets
            if '_ideas = {' in text_file:
                pattern_matches = re.findall("add_ideas = \\{.*\n((.|\n*?)*)\n\t*\\}", text_file)
                pattern_matches += re.findall("remove_ideas = \\{.*\n((.|\n*?)*)\n\t*\\}", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        ideas_code = match[0].split('\n')
                        for idea in ideas_code:
                            idea = idea.strip('\t')
                            if "#" not in idea and len(idea) > 0:
                                used_ideas.append(idea)
                            paths[idea] = os.path.basename(filename)

            if 'show_ideas_tooltip =' in text_file:
                pattern_matches = re.findall("show_ideas_tooltip = ([\\w':-]+)", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        used_ideas.append(match)
                        paths[match] = os.path.basename(filename)

            # Timed ideas
            if '\tidea =' in text_file:
                pattern_matches = re.findall("\tidea = ([\\w':-]+)", text_file)
                if len(pattern_matches) > 0:
                    for match in pattern_matches:
                        used_ideas.append(match)
                        paths[match] = os.path.basename(filename)

        if return_paths:
            return (used_ideas, paths)
        else:
            return used_ideas

    @classmethod
    def get_all_ideas_names(cls, test_runner, lowercase: bool = True, return_paths: bool = False, include_hidden_ideas: bool = True, include_country_ideas: bool = True, include_manufacturers: bool = True, include_characters_tokens: bool = True, include_laws: bool = False, include_army_spirits: bool = False) -> tuple[list, dict]:
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
        ideas, paths = Ideas.get_all_ideas(test_runner=test_runner, lowercase=lowercase, return_paths=True, include_hidden_ideas=include_hidden_ideas, include_country_ideas=include_country_ideas, include_manufacturers=include_manufacturers, include_laws=include_laws, include_army_spirits=include_army_spirits)

        ideas_names = []
        ideas_names_paths = {}
        for idea in ideas:
            name = re.findall('^\\t\\t(.+) =', idea)[0]
            ideas_names.append(name)       # get all ideas names
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
