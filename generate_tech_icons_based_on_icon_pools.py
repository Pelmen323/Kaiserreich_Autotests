import re
import os

INPUT_FILE_PATH_TAG = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\kaiserreich\\technology_icons_tanks.gfx'
INPUT_FILE_PATH_TAG2 = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\kaiserreich\\technology_icons_tank_designer.gfx'
INPUT_FILE_PATH_EE = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\interface\\kaiserreich\\technology_icons_tanks.gfx'
PATH_TO_ICON_POOL = 'C:\\Users\\' + os.getlogin() + '\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\Kaiserreich Dev Build\\gfx\\interface\\equipmentdesigner\\graphic_db\\00_Russia_tank_icons.txt'
INPUT_LIST = [
    ['gwtank_medium', 'light_tank_chassis_0'],
    ['basic_light_tank_medium', 'light_tank_chassis_1'],
    ['basic_light_td_medium', 'light_tank_destroyer_chassis_1'],
    ['basic_light_art_medium', 'light_tank_artillery_chassis_1'],
    ['basic_light_spaa_medium', 'light_tank_aa_chassis_1'],
    ['improved_light_tank_medium', 'light_tank_chassis_2'],
    ['improved_light_td_medium', 'light_tank_destroyer_chassis_2'],
    ['improved_light_art_medium', 'light_tank_artillery_chassis_2'],
    ['improved_light_spaa_medium', 'light_tank_aa_chassis_2'],
    ['advanced_light_tank_medium', 'light_tank_chassis_3'],
    ['advanced_light_td_medium', 'light_tank_destroyer_chassis_3'],
    ['advanced_light_art_medium', 'light_tank_artillery_chassis_3'],
    ['advanced_light_spaa_medium', 'light_tank_aa_chassis_3'],
    ['early_medium_tank_medium', 'medium_tank_chassis_0'],
    ['early_medium_td_medium', 'medium_tank_destroyer_chassis_0'],
    ['early_medium_art_medium', 'medium_tank_artillery_chassis_0'],
    ['early_medium_spaa_medium', 'medium_tank_aa_chassis_0'],
    ['basic_medium_tank_medium', 'medium_tank_chassis_1'],
    ['basic_medium_td_medium', 'medium_tank_destroyer_chassis_1'],
    ['basic_medium_art_medium', 'medium_tank_artillery_chassis_1'],
    ['basic_medium_spaa_medium', 'medium_tank_aa_chassis_1'],
    ['improved_medium_tank_medium', 'medium_tank_chassis_2'],
    ['improved_medium_td_medium', 'medium_tank_destroyer_chassis_2'],
    ['improved_medium_art_medium', 'medium_tank_artillery_chassis_2'],
    ['improved_medium_spaa_medium', 'medium_tank_aa_chassis_2'],
    ['advanced_medium_tank_medium', 'medium_tank_chassis_3'],
    ['advanced_medium_td_medium', 'medium_tank_destroyer_chassis_3'],
    ['advanced_medium_art_medium', 'medium_tank_artillery_chassis_3'],
    ['advanced_medium_spaa_medium', 'medium_tank_aa_chassis_3'],
    ['early_heavy_tank_medium', 'heavy_tank_chassis_0'],
    ['early_heavy_td_medium', 'heavy_tank_destroyer_chassis_0'],
    ['early_heavy_art_medium', 'heavy_tank_artillery_chassis_0'],
    ['early_heavy_spaa_medium', 'heavy_tank_aa_chassis_0'],
    ['basic_heavy_tank_medium', 'heavy_tank_chassis_1'],
    ['basic_heavy_td_medium', 'heavy_tank_destroyer_chassis_1'],
    ['basic_heavy_art_medium', 'heavy_tank_artillery_chassis_1'],
    ['basic_heavy_spaa_medium', 'heavy_tank_aa_chassis_1'],
    ['improved_heavy_tank_medium', 'heavy_tank_chassis_2'],
    ['improved_heavy_td_medium', 'heavy_tank_destroyer_chassis_2'],
    ['improved_heavy_art_medium', 'heavy_tank_artillery_chassis_2'],
    ['improved_heavy_spaa_medium', 'heavy_tank_aa_chassis_2'],
    ['advanced_heavy_tank_medium', 'heavy_tank_chassis_3'],
    ['advanced_heavy_td_medium', 'heavy_tank_destroyer_chassis_3'],
    ['advanced_heavy_art_medium', 'heavy_tank_artillery_chassis_3'],
    ['advanced_heavy_spaa_medium', 'heavy_tank_aa_chassis_3'],
    ['super_heavy_tank_medium', 'super_heavy_tank_chassis_1'],
    ['super_heavy_td_medium', 'super_heavy_tank_destroyer_chassis_1'],
    ['super_heavy_art_medium', 'super_heavy_tank_artillery_chassis_1'],
    ['super_heavy_spaa_medium', 'super_heavy_tank_aa_chassis_1'],
    ['land_cruiser_armor_medium', 'land_cruiser_chassis_1'],
    ['main_battle_tank_medium', 'modern_tank_chassis_1'],
    ['modern_td_medium', 'modern_tank_destroyer_chassis_1'],
    ['modern_art_medium', 'modern_tank_artillery_chassis_1'],
    ['modern_spaa_medium', 'modern_tank_aa_chassis_1'],
    ['amphibious_tank_medium', 'amphibious_tank_chassis_1']
]
TAGS = ['FER']


def main(input_list: list[str, str]):
    '''
    This script autogenerates tech icons based on the first icon in icon pool
    Useful if you have created icon pool but need to update non-NSB icon techs
    Input - List
    Input[0] - tank icon
    Input[1] - chassis icon
    TAGS - list with tags to process
    INPUT_FILE_PATH_TAG - file with tank techs gfx
    INPUT_FILE_PATH_EE - file with tank techs gfx (ee)
    PATH_TO_ICON_POOL - file with tank techs icon pool
    '''

    for tag in TAGS:
        with open(PATH_TO_ICON_POOL, 'r', encoding='utf-8') as text_file:
            input_file = text_file.read()

        models_pool = re.findall(tag + ' = {.*?\n}', input_file, flags=re.DOTALL | re.MULTILINE)[0]
        for item in input_list:
            tech_icon = item[0]
            chassis = item[1]

            try:
                chassis_subpool = re.findall('\t' + chassis + r' = \{.*?icons = \{([^}]+).*?\n\t\}', models_pool, flags=re.DOTALL | re.MULTILINE)[0]
            ## No chassis icon
            except IndexError:
                continue
            ### Clean up chassis subpool
            chassis_subpool = chassis_subpool.strip('\t')
            if '\n' in chassis_subpool:
                chassis_subpool = chassis_subpool.split('\n')
                chassis_subpool = [i for i in chassis_subpool if i.strip('\t') != '']
                first_icon_to_show = chassis_subpool[-1].strip('\t')
            else:
                first_icon_to_show = chassis_subpool.strip(' ')

            ### Now compare filepaths for first icon in pull and tech icon for that tier
            with open(INPUT_FILE_PATH_TAG, 'r', encoding='utf-8') as text_file_tech_ee:
                tech_EE_input_file = text_file_tech_ee.read()
                try:
                    ee_tank_icon_path = re.findall(first_icon_to_show + '.*?\n.*?texturefile.*?=.*?"(.*?)"', tech_EE_input_file)[0]
                except Exception:
                    with open(INPUT_FILE_PATH_TAG2, 'r', encoding='utf-8') as text_file_tech_ee:
                        tech_EE_input_file = text_file_tech_ee.read()
                        ee_tank_icon_path = re.findall(first_icon_to_show + '.*?\n.*?texturefile.*?=.*?"(.*?)"', tech_EE_input_file)[0]

            try:
                with open(INPUT_FILE_PATH_TAG, 'r', encoding='utf-8') as text_file_tech_tag:
                    tech_TAG_input_file = text_file_tech_tag.read()
                    tag_tank_icon_path = re.findall('GFX_' + tag + '_' + tech_icon + '.*?\n.*?texturefile.*?=.*?"(.*?)"', tech_TAG_input_file)[0]
            except IndexError:
                ### Tech icon doesn't exist - need to create
                tag_tank_icon_path = ""

            if ee_tank_icon_path != tag_tank_icon_path:
                # if "Poland" not in tag_tank_icon_path and "Ukraine" not in tag_tank_icon_path:
                print(f'{ee_tank_icon_path} - {tag_tank_icon_path}')
                if tag_tank_icon_path != "":
                    ## Replace invalid path
                    with open(INPUT_FILE_PATH_TAG, 'w', encoding='utf-8') as text_file_write:
                        what_to_replace = re.findall('GFX_' + tag + '_' + tech_icon + '.*?\n.*?texturefile.*?=.*?".*?"', tech_TAG_input_file)[0]
                        replace_with = 'GFX_' + tag + '_' + tech_icon + '"\n\t\ttexturefile = "' + ee_tank_icon_path + '"'
                        output_file = tech_TAG_input_file.replace(what_to_replace, replace_with)
                        text_file_write.write(output_file)
                else:
                    ## Add new entry
                    with open(INPUT_FILE_PATH_TAG, 'w', encoding='utf-8') as text_file_write:
                        previous_tech_in_list = input_list[input_list.index(item)-1][0]
                        what_to_replace = re.findall('GFX_' + tag + '_' + previous_tech_in_list + '.*? = \{.*?\n\t\}', tech_TAG_input_file, flags=re.DOTALL | re.MULTILINE)[0]
                        replace_with = '\n\tSpriteType = {\n\t\tname = "GFX_' + tag + '_' + tech_icon + '"\n\t\ttexturefile = "' + ee_tank_icon_path + '"\n\t}'
                        output_file = tech_TAG_input_file.replace(what_to_replace, what_to_replace + replace_with)
                        text_file_write.write(output_file)


if __name__ == '__main__':
    main(INPUT_LIST)
