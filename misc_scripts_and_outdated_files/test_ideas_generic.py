##########################
# Test script to check if there are generic ideas used together with custom ideas
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from test_classes.generic_test_class import (
    ResultsReporter,
)
from test_classes.ideas_class import Ideas

FILES_TO_SKIP = ["00 Generic ideas.txt", '01 Army Spirits.txt', '01 Air Spirits.txt', '01 Navy Spirits.txt']
GENERIC_TAGS = ['ADA', 'AFG', 'ALG', 'AMA', 'ANG', 'ANT', 'ASY', 'AZR', 'BAH', 'BAS', 'BAY', 'BHU', 'BOT', 'BRD', 'BRI', 'BRM', 'BRT', 'BUK', 'CAM', 'CAR', 'CAT', 'CEN', 'CEY', 'CHA', 'CMR', 'COG', 'COS', 'CYP', 'DAH', 'PRE', 'EPR', 'DOM', 'ECU', 'ELS', 'EQG', 'ERI', 'ETS', 'EMI', 'FRP', 'LIL', 'GAB', 'GHA', 'GLC', 'GNA', 'GNB', 'GOY', 'GRP', 'GRU', 'GUA', 'GYA', 'HAI', 'HAU', 'HEJ', 'HON', 'ICE', 'IKH', 'INR', 'IRQ', 'IVO', 'JAM', 'JBS', 'KAC', 'KAZ', 'KBR', 'KDR', 'KEN', 'KHI', 'KIV', 'KOR', 'KUM', 'KUR', 'LAO', 'LBA', 'LEB', 'LIB', 'MAD', 'MAL', 'MAN', 'MLI', 'MLT', 'MLW', 'MNT', 'MON', 'MOR', 'MRT', 'MZB', 'NEP', 'NGA', 'NGF', 'NGR', 'NIC', 'NMB', 'NZL', 'OMA', 'PAL', 'PAN', 'PHI', 'PIR', 'PNG', 'QUE', 'RHI', 'VCR', 'RWA', 'SAR', 'SAU', 'SCO', 'SEN', 'SHA', 'SIE', 'SIK', 'SLO', 'SLV', 'SPO', 'SUD', 'SUR', 'SYR', 'TAI', 'TIB', 'TKE', 'TOG', 'TRI', 'TRK', 'TRP', 'TRS', 'TRU', 'TUN', 'TUS', 'TZN', 'UGA', 'VIN', 'VOL', 'WLS', 'YEM', 'YUC', 'ZAM', 'ZAN']


def test_check_ideas_generic(test_runner: object):
    results = []
    # 1. Get the dict of all ideas
    for i in [
        [True, False, False, False, False, "tank"],
        [False, True, False, False, False, "naval"],
        [False, False, True, False, False, "air"],
        [False, False, False, True, False, "industrial"],
        [False, False, False, False, True, "materiel"],
    ]:
        ideas = Ideas.get_all_ideas(
            test_runner=test_runner,
            lowercase=False,
            return_paths=False,
            include_hidden_ideas=False,
            include_country_ideas=False,
            include_manufacturers=False,
            include_tank_manufacturers=i[0],
            include_naval_manufacturers=i[1],
            include_air_manufacturers=i[2],
            include_industrial_manufacturers=i[3],
            include_materiel_manufacturers=i[4]
        )
        generic_ideas = {}
        for x in ideas:
            idea_token = re.findall(r'^\t\t(.+) =', x)[0]
            if 'generic' in idea_token:
                tag_definitions = re.findall(r'tag = (.+)', x)
                if tag_definitions != []:
                    for d in tag_definitions:
                        if d in GENERIC_TAGS:
                            results.append(f'{idea_token} - idea is added to tag {d} multiple times')
                    generic_ideas[idea_token] = tag_definitions + GENERIC_TAGS

        for x in ideas:
            idea_token = re.findall(r'^\t\t(.+) =', x)[0]
            if 'generic' not in idea_token:
                tag_definitions = re.findall(r'tag = (.+)', x)
                for gi in generic_ideas.keys():
                    for tag in tag_definitions:
                        if tag in generic_ideas[gi]:
                            results.append(f'{tag} - idea {idea_token} is available together with generic idea {gi} in the same category `{i[5]}`')

    ResultsReporter.report_results(results=results, message="A mix of generic and custom manufacturer ideas is encountered.")
