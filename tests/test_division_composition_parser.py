##########################
# Test script to parse division templates
# By Pelmen, https://github.com/Pelmen323
##########################
import glob
import os
import re

from ..test_classes.generic_test_class import FileOpener, ResultsReporter


class RegimentsSection:
    def __init__(self, text_line: str, is_support_section=False) -> None:
        if is_support_section:
            self.regiments_section = re.findall("^(\\t*?)support = \\{.*?\\n(.*?)\\n^\\1\\}", text_line, flags=re.DOTALL | re.MULTILINE)[0][1].split('\n')
        else:
            self.regiments_section = re.findall("^(\\t*?)regiments = \\{.*?\\n(.*?)\\n^\\1\\}", text_line, flags=re.DOTALL | re.MULTILINE)[0][1].split('\n')
        self.regiments_list = []

        for i in self.regiments_section:
            self.regiments_list.append(Regiment(text_line=i))

        self.regiments_coodrs_list = [(i.x, i.y) for i in self.regiments_list]


class Regiment:
    def __init__(self, text_line: str):
        self.battalion_type = re.findall("\t([^\t]*?) = \\{", text_line)[0]
        self.x = int(re.findall(" x = (.)", text_line)[0])
        self.y = int(re.findall(" y = (.)", text_line)[0])


def test_division_composition_parser(test_runner: object):
    filepath = test_runner.full_path_to_mod
    results = []

    for filename in glob.iglob(filepath + "**/*.txt", recursive=True):
        text_file = FileOpener.open_text_file(filename)

        if "division_template = {" in text_file:
            pattern_matches = re.findall("^(\\t*?)division_template = (\\{.*?^\\1\\})", text_file, flags=re.DOTALL | re.MULTILINE)
            if len(pattern_matches) > 0:
                for match in pattern_matches:
                    match = match[1]
                    division_name = re.findall('name = "(.*)"', match)[0]

                    if "regiments = {" in match:
                        regiments_section = RegimentsSection(text_line=match)

                        # 1. Check the regiments section
                        if x := len([i for i in regiments_section.regiments_coodrs_list if regiments_section.regiments_coodrs_list.count(i) > 1]) > 0:
                            results.append((os.path.basename(filename), f'{division_name} - duplicated regiments'))

                        for i in regiments_section.regiments_coodrs_list:
                            x = i[0]
                            y = i[1]

                            if x == 0 and y == 0:
                                continue

                            # 1.1 Check x axis (column)
                            if x != 0 and y == 0:
                                for i1 in range(0, x):
                                    if (i1, 0) not in regiments_section.regiments_coodrs_list:
                                        results.append((os.path.basename(filename), f'{division_name} - Regiment {i1, 0} is missing'))

                            # 1.2 Check y axis (row)
                            if y != 0:
                                for i2 in range(0, y):
                                    if (x, i2) not in regiments_section.regiments_coodrs_list:
                                        results.append((os.path.basename(filename), f'{division_name} - Regiment {x, i2} is missing'))
                    else:
                        results.append((os.path.basename(filename), f'{division_name} - missing regiments section'))

                    # 2. Check the support section
                    if "support = {" in match:
                        support_section = RegimentsSection(text_line=match, is_support_section=True)

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
