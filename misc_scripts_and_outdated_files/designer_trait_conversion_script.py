import glob
import re

from core.runner import TestRunner
from test_classes.generic_test_class import FileOpener
from test_classes.ideas_class import Ideas
from pathlib import Path
import os

air = False
tank = False
navy = False
materiel = False
industrial = True

if air:
    INPUT_DICT = {
        'generic_general_aircraft_organization': 'general_aircraft_manufacturer',
        'generic_light_aircraft_organization': 'light_aircraft_manufacturer',
        'generic_medium_aircraft_organization': 'medium_aircraft_manufacturer',
        'generic_heavy_aircraft_organization': 'heavy_aircraft_manufacturer',
        'generic_cas_aircraft_organization': 'cas_aircraft_manufacturer',
        'generic_naval_aircraft_organization': 'naval_aircraft_manufacturer',
        'generic_multi_role_aircraft_organization':  'multi_role_aircraft_manufacturer',
        'generic_high_agility_fighter_aircraft_organization': 'high_agility_fighter_aircraft_manufacturer',
        'generic_range_focused_aircraft_organization': 'range_focused_aircraft_manufacturer',
    }
    RESEARCH_BONUS = 'air_equipment'

elif tank:
    INPUT_DICT = {
        'generic_tank_organization': 'general_tank_manufacturer',
        'generic_infantry_tank_organization': 'infantry_tank_manufacturer',
        'generic_assault_guns_organization': 'assault_gun_manufacturer',
        'generic_mobile_tank_organization': 'mobile_tank_manufacturer',
        'generic_medium_tank_organization': 'medium_tank_manufacturer',
        'generic_heavy_tank_organization': 'heavy_tank_manufacturer',
        'generic_tank_refurbishment_plant_organization': 'tank_refurbishment_plant',
    }
    RESEARCH_BONUS = 'armor'

elif navy:
    INPUT_DICT = {
        'generic_task_force_ship_organization': 'task_force_ship_manufacturer',
        'generic_battle_line_ship_organization': 'battle_line_ship_manufacturer',
        'generic_escort_ship_organization': 'escort_ship_manufacturer',
        'generic_raider_ship_organization': 'raider_ship_manufacturer',
        'generic_submarine_organization': 'submarine_manufacturer',
        'generic_small_fleet_organization': 'small_fleet_manufacturer',
        'generic_refurbishment_repair_dockyard_organization': 'refurbishment_repair_dockyard',
    }
    RESEARCH_BONUS = 'naval_equipment'


def legacy_designer_trait_replacer(username, mod_name):
    results = []
    mio_dict = {}
    ideas_to_override = {}
    test_runner = TestRunner(username, mod_name)
    filepath_to_mio = str(Path(test_runner.full_path_to_mod) / "common" / "military_industrial_organization" / "organizations") + "/"
    filepath_to_ideas = str(Path(test_runner.full_path_to_mod) / "common" / "ideas") + "/"

    # Find all tank/armor mios
    for filename in glob.iglob(filepath_to_mio + "**/*.txt", recursive=True):
        if "generic" in filename:
            continue
        text_file = FileOpener.open_text_file(filename)

        pattern_matches = re.findall(r"^[^\t#]+ = \{.*?^\}", text_file, flags=re.MULTILINE | re.DOTALL)
        if len(pattern_matches) > 0:
            for match in pattern_matches:
                for k in INPUT_DICT.keys():
                    if k in match:
                        mio_name = re.findall(r'^\tname = (.*)', match, flags=re.MULTILINE)[0]

                        # if mio_name in mio_dict.keys():
                        #     results.append(f'2 or more MIO with the same name encountered {mio_name} - make sure they have matching traits! This affects script results')

                        for i in mio_dict.keys():
                            if mio_name in i:
                                results.append(f'MIO duplication - {mio_name} and {i} - make sure they have matching traits!')
                            elif i in mio_name:
                                results.append(f'MIO duplication - {mio_name} and {i} - make sure they have matching traits!')

                        mio_trait = re.findall(r'include = (.*)', match)[0]
                        mio_dict[mio_name] = mio_trait

    assert len(mio_dict) > 0

    ideas = Ideas.get_all_ideas(test_runner, lowercase=False, include_country_ideas=False, include_hidden_ideas=False, include_manufacturers=False, include_tank_manufacturers=tank, include_naval_manufacturers=navy, include_air_manufacturers=air)
    for i in ideas:
        idea_name = re.findall(r'^\t+(.*) = \{', i)[0]
        idea_name_arg = re.findall(r'\tname = (.*)', i)[0].lower() if 'name =' in i else False
        matching_mio_trait = False
        # 1. mio name == idea token

        if idea_name.lower() not in mio_dict.keys():
            partial_match = False

            # 2. mio name is in idea token
            for m in mio_dict.keys():
                if m in idea_name.lower():
                    partial_match = True
                    matching_mio_trait = mio_dict[m]
                    break
                elif idea_name_arg:
                    # 3. idea name is in mio name
                    if idea_name_arg in m:
                        partial_match = True
                        matching_mio_trait = mio_dict[m]
                        break
                    # 4. mio name is in idea name
                    elif m in idea_name_arg:
                        partial_match = True
                        matching_mio_trait = mio_dict[m]
                        break

            if not partial_match:
                results.append(f'Idea `{idea_name}` is not present in MIOs or MIO has a custom name/trait')
        else:
            matching_mio_trait = mio_dict[idea_name.lower()]

        if matching_mio_trait:
            idea_trait_code = re.findall(r'traits = \{.*?\}', i, flags=re.MULTILINE | re.DOTALL)[0]
            idea_trait = re.findall(r'traits = \{(.*?)\}', i, flags=re.MULTILINE | re.DOTALL)[0].strip(' ').strip('\t').strip('\n').strip('\t')
            custom_idea_trait = False
            if matching_mio_trait == "custom_mio":
                results.append(f'MIO `{idea_name}` is a custom MIO with no inherited generic mios please veify that idea trait `{idea_trait}` is matching')

            elif matching_mio_trait not in INPUT_DICT.keys():
                results.append(f'MIO `{idea_name}` has a custom trait `{matching_mio_trait}` that is not supported')

            else:
                if '_0' in idea_trait:
                    new_idea_trait_code = idea_trait_code.replace(idea_trait, INPUT_DICT[matching_mio_trait] + '_0')
                elif '_1' in idea_trait:
                    new_idea_trait_code = idea_trait_code.replace(idea_trait, INPUT_DICT[matching_mio_trait] + '_1')
                elif '_2' in idea_trait:
                    new_idea_trait_code = idea_trait_code.replace(idea_trait, INPUT_DICT[matching_mio_trait] + '_2')
                else:
                    custom_idea_trait = True

                if not custom_idea_trait:
                    ideas_to_override[i] = i.replace(idea_trait_code, new_idea_trait_code)

                else:
                    results.append(f'Idea `{idea_name}` has a custom trait `{idea_trait}` - verify manually')

    for filename in glob.iglob(filepath_to_ideas + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file
        override = False
        for i in ideas_to_override.keys():
            if i in text_file:
                text_file_new = text_file_new.replace(i, ideas_to_override[i])
                override = True

        if override:
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file_new)

    if len(results) < 1:
        print("No issues found!")
    else:
        for i in sorted(set(results)):
            print('- [ ] ' + i)


def legacy_designer_research_replacer(username, mod_name):
    results = []
    ideas_to_override = {}
    test_runner = TestRunner(username, mod_name)
    filepath_to_ideas = str(Path(test_runner.full_path_to_mod) / "common" / "ideas") + "/"

    ideas = Ideas.get_all_ideas(test_runner, lowercase=False, include_country_ideas=False, include_hidden_ideas=False, include_manufacturers=False, include_tank_manufacturers=tank, include_naval_manufacturers=navy, include_air_manufacturers=air, include_materiel_manufacturers=materiel)
    for i in ideas:
        idea_name = re.findall(r'^\t+(.*) = \{', i)[0]
        research_bonus_code = re.findall(r'research_bonus = \{.*?\}', i, flags=re.MULTILINE | re.DOTALL)[0] if 'research_bonus = {' in i else False
        idea_trait_code = re.findall(r'traits = \{.*?\}', i, flags=re.MULTILINE | re.DOTALL)[0]
        idea_trait = re.findall(r'traits = \{(.*?)\}', i, flags=re.MULTILINE | re.DOTALL)[0].strip(' ').strip('\t').strip('\n').strip('\t')

        if any([air, tank, navy]):
            research_bonus = RESEARCH_BONUS
            if research_bonus_code:
                ideas_to_override[i] = i.replace(research_bonus_code, f'research_bonus = {{\n\t\t\t\t{research_bonus} = 0.15\n\t\t\t}}')
            else:
                ideas_to_override[i] = i.replace(idea_trait_code, idea_trait_code + f'\n\t\t\tresearch_bonus = {{\n\t\t\t\t{research_bonus} = 0.15\n\t\t\t}}')

        elif materiel:
            research_bonus = ''
            if 'support_equipment_manufacturer' in idea_trait:
                research_bonus = 'support_tech'
            elif 'motorised_equipment_manufacturer' in idea_trait:
                research_bonus = 'motorized_equipment'
            elif 'armored_car_manufacturer' in idea_trait:
                research_bonus = 'armor'

            elif 'infantry_equipment_manufacturer' in idea_trait:
                research_bonus = 'infantry_weapons'
            elif 'artillery_equipment_manufacturer' in idea_trait:
                research_bonus = 'artillery'
            elif 'mechanised_equipment_manufacturer' in idea_trait:
                research_bonus = 'motorized_equipment'

            if research_bonus == '':
                results.append(f'Idea `{idea_name}` - unknown trait {idea_trait}, fix research bonus manually')
                continue

            if research_bonus_code:
                ideas_to_override[i] = i.replace(research_bonus_code, f'research_bonus = {{\n\t\t\t\t{research_bonus} = 0.15\n\t\t\t}}')
            else:
                ideas_to_override[i] = i.replace(idea_trait_code, idea_trait_code + f'\n\t\t\tresearch_bonus = {{\n\t\t\t\t{research_bonus} = 0.15\n\t\t\t}}')

            if 'armored_car_manufacturer' in idea_trait:
                if 'has_dlc_lar = yes' not in i:
                    results.append(f'Idea `{idea_name}` should have LAR check')

    for filename in glob.iglob(filepath_to_ideas + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        text_file_new = text_file
        override = False
        for i in ideas_to_override.keys():
            if i in text_file:
                text_file_new = text_file_new.replace(i, ideas_to_override[i])
                override = True

        if override:
            with open(filename, 'w', encoding="utf-8") as text_file_write:
                text_file_write.write(text_file_new)

    if len(results) < 1:
        print("No issues found!")
    else:
        for i in sorted(set(results)):
            print('- [ ] ' + i)


def list_ideas(username, mod_name):
    results = []
    test_runner = TestRunner(username, mod_name)

    idea_names = []

    ideas = Ideas.get_all_ideas(test_runner, lowercase=False, include_country_ideas=False, include_hidden_ideas=False, include_manufacturers=False, include_tank_manufacturers=tank, include_naval_manufacturers=navy, include_air_manufacturers=air, include_materiel_manufacturers=materiel, include_industrial_manufacturers=industrial)
    for i in ideas:
        idea_name = re.findall(r'^\t+(.*) = \{', i)[0]
        idea_names.append(idea_name)

    for filename in glob.iglob(test_runner.full_path_to_mod + '**/*.txt', recursive=True):
        text_file = FileOpener.open_text_file(filename, lowercase=False)
        if 'add_ideas' in text_file:
            for i in idea_names:
                if f'add_ideas = {i}' in text_file:
                    results.append(f'{i} - {os.path.basename(filename)}')

    if len(results) < 1:
        print("No issues found!")
    else:
        for i in sorted(set(results)):
            print('- [ ] ' + i)


list_ideas(username="VADIM", mod_name="Kaiserreich Dev Build")
