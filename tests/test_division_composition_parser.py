##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


class RegimentsSection:
    def __init__(self, text_line: str, filepath: str, filepath_to_vanilla: str, is_support_section=False) -> None:
        try:
            if is_support_section:
                self.regiments_section = re.findall("^(\\t*?)support = \\{.*?\\n(.*?)\\n^\\1\\}", text_line, flags=re.DOTALL | re.MULTILINE)[0][1].split('\n')
            else:
                self.regiments_section = re.findall("^(\\t*?)regiments = \\{.*?\\n(.*?)\\n^\\1\\}", text_line, flags=re.DOTALL | re.MULTILINE)[0][1].split('\n')
            self.regiments_list = []

            for i in self.regiments_section:
                if len(i) > 4:
                    self.regiments_list.append(Regiment(i, filepath, filepath_to_vanilla))

            self.regiments_coodrs_list = [(i.x, i.y) for i in self.regiments_list]
        except Exception:
            print(text_line)
            raise


class Regiment:
    def __init__(self, text_line: str, filepath: str, filepath_to_vanilla: str):
        self.battalion_type = re.findall("\t([^\t]*?) = \\{", text_line)[0]
        self.x = int(re.findall(" x = (.)", text_line)[0])
        self.y = int(re.findall(" y = (.)", text_line)[0])
        for i in [filepath_to_vanilla, filepath]:
            for filename in glob.iglob(f'{i}\\common\\units' + '**/*.txt', recursive=True):
                text_file = FileOpener.open_text_file(filename)
                if f'	{self.battalion_type} = ' + '{' in text_file:
                    self.group = re.findall('^\\t' + self.battalion_type + ' = \\{.*?group = (.*?)\\n.*?^\\t\\}', text_file, flags=re.DOTALL | re.MULTILINE)[0]


def test_division_composition_parser(test_runner: object):
    filepath = test_runner.full_path_to_mod
    filepath_to_vanilla = "C:\\SteamLibrary\\steamapps\\common\\Hearts of Iron IV"
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "division_template = {" in text_file:
            pattern_matches = re.findall("^(\\t*?)division_template = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[1]
                    division_name = re.findall('name = "(.*)"', match)[0]

                    # 1. Check the regiments section
                    if "regiments = {" in match:
                        regiments_section = RegimentsSection(match, filepath, filepath_to_vanilla)

                        # 1.1 Regiments occupying the same coordinates
                        if x := len([i for i in regiments_section.regiments_coodrs_list if regiments_section.regiments_coodrs_list.count(i) > 1]) > 0:
                            results.append((os.path.basename(filename), f'{division_name} - duplicated regiments'))

                        # 1.2 Columns with mixed unit groups
                        try:
                            for i in range(0, max([i.x for i in regiments_section.regiments_list]) + 1):
                                regiments_from_the_same_column = sorted([r for r in regiments_section.regiments_list if r.x == i], key=lambda x: x.y)
                                column_group = regiments_from_the_same_column[0].group
                                for reg in regiments_from_the_same_column:
                                    if reg.group != column_group:
                                        results.append((os.path.basename(filename), f'{division_name} - regiment {reg.battalion_type} on coords {reg.x} {reg.y} does not belong to the group {column_group}'))
                        except Exception:
                            print(match)
                            raise

                        # 1.3 Missing regiments
                        for i in regiments_section.regiments_coodrs_list:
                            x = i[0]
                            y = i[1]

                            if x == 0 and y == 0:
                                continue

                            # Check x axis (column)
                            if x != 0 and y == 0:
                                for i1 in range(0, x):
                                    if (i1, 0) not in regiments_section.regiments_coodrs_list:
                                        results.append((os.path.basename(filename), f'{division_name} - Regiment {i1, 0} is missing'))

                            # Check y axis (row)
                            if y != 0:
                                for i2 in range(0, y):
                                    if (x, i2) not in regiments_section.regiments_coodrs_list:
                                        results.append((os.path.basename(filename), f'{division_name} - Regiment {x, i2} is missing'))

                            # 1.4 Regiments that should be locked
                            if y == 4:
                                results.append((os.path.basename(filename), f'{division_name} - Regiment {x, y} should be locked by doctrine'))

                    else:
                        results.append((os.path.basename(filename), f'{division_name} - missing regiments section'))

                    # 2. Check the support section
                    if "support = {" in match:
                        support_section = RegimentsSection(match, filepath, filepath_to_vanilla, is_support_section=True)

                        if x := len([i for i in support_section.regiments_coodrs_list if support_section.regiments_coodrs_list.count(i) > 1]) > 0:
                            results.append((os.path.basename(filename), f'{division_name} - duplicated support company coords'))

                        for i in support_section.regiments_coodrs_list:
                            x = i[0]
                            y = i[1]

                            # 2.1 Check if company is defined not in the 1st column
                            if x != 0:
                                results.append((os.path.basename(filename), f'{division_name} - Invalid support company coordinates {x, y}'))

                            # 2.2 Check y axis (row)
                            elif y != 0:
                                for i2 in range(0, y):
                                    if (x, i2) not in support_section.regiments_coodrs_list:
                                        results.append((os.path.basename(filename), f'{division_name} - Support company {x, i2} is missing'))

    ResultsReporter.report_results(results=results, message="Division templates with violations were encountered. Check console output")
