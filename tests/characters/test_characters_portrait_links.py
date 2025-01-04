##########################
# Test script to check if characters have required portrait links
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.characters_class import Characters
from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = (
    "hnn_tang_hualong",
    "hnn_ren_bishi",
    "hnn_cai_hesen",
    "hnn_huang_yanpei",
    "hnn_tan_yankai",
    "hnn_zhou_shizhao",
    "lep_rong_zongjing",
    "lep_li_baozhang",
    "lep_li_linsi",
)


def test_characters_portrait_links(test_runner: object):
    characters, paths = Characters.get_all_characters(test_runner=test_runner, return_paths=True)
    results = []
    pattern_army = re.compile(r"\t\t\tarmy = \{.*?\}", flags=re.DOTALL | re.MULTILINE)
    pattern_navy = re.compile(r"\t\t\tnavy = \{.*?\}", flags=re.DOTALL | re.MULTILINE)
    pattern_civ = re.compile(r"\t\t\tcivilian = \{.*?\}", flags=re.DOTALL | re.MULTILINE)

    for char in characters:
        unit_leader_role = any([char.count("field_marshal =") > 0, char.count("corps_commander =") > 0])
        advisor_role = char.count("\tadvisor = {") > 0
        country_leader_role = char.count("\tcountry_leader = {") > 0
        char_name = re.findall(r"^\t(.+) =", char)[0]
        army_portraits = re.findall(pattern_army, char)
        navy_portraits = re.findall(pattern_navy, char)
        civ_portraits = re.findall(pattern_civ, char)

        if any([army_portraits != [], navy_portraits != [], civ_portraits != []]):
            small_line = None
            large_line = None
            for i in [army_portraits, navy_portraits, civ_portraits]:
                if i != []:
                    portraits_line = i[0]
                    if "small = " in portraits_line:
                        small_line = re.findall(r"small = \S*", portraits_line)[0]
                        if "_large" in small_line:
                            results.append(f"{char_name} - {paths[char]} - small portrait link is potentially invalid - {small_line}")
                    if "large = " in portraits_line:
                        large_line = re.findall(r"large = \S*", portraits_line)[0]
                        if "_small" in large_line:
                            results.append(f"{char_name} - {paths[char]} - large portrait link is potentially invalid - {small_line}")

            if unit_leader_role:
                if small_line is None:
                    results.append(f"{char_name} - {paths[char]} - Character (unit leader) is missing small portrait link")
                if large_line is None:
                    results.append(f"{char_name} - {paths[char]} - Character (unit leader) is missing large portrait link")

            if advisor_role:
                if small_line is None:
                    results.append(f"{char_name} - {paths[char]} - Character (advisor) is missing small portrait link")

            if country_leader_role:
                if large_line is None:
                    results.append(f"{char_name} - {paths[char]} - Character (country leader) is missing large portrait link")

    ResultsReporter.report_results(results=results, message="Missing character portrait links were encountered.")
