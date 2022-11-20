import glob
import re

from core.runner import TestRunner
from test_classes.generic_test_class import DataCleaner, FileOpener

FILES_TO_SKIP = ['localisation', 'interface', 'gfx', 'map', 'common\\units', 'names', 'states', '00_construction_scripted_effects']


def replace_string(filename, pattern, replace_with, encoding="utf-8", flag=None):
    text_file = FileOpener.open_text_file(filename, lowercase=False)
    if flag is None:
        text_file_fixed = re.sub(pattern=pattern, repl=replace_with, string=text_file)
    else:
        text_file_fixed = re.sub(pattern=pattern, repl=replace_with, string=text_file, flags=flag)

    with open(filename, 'w', encoding=encoding) as text_file_write:
        text_file_write.write(text_file_fixed)


def apply_formatting(filename, encoding="utf-8"):
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=\\{\\}])  (?=[\\w_\\"=\\{\\}])', replace_with=' ', encoding=encoding)  # Remove any doublespaces
    replace_string(filename=filename, pattern='=\\b', replace_with='= ', encoding=encoding)                     # Add spaces between symbol and =
    replace_string(filename=filename, pattern='\\b=', replace_with=' =', encoding=encoding)                     # Add spaces between symbol and =
    replace_string(filename=filename, pattern='=\\{', replace_with='= {', encoding=encoding)                    # Add spaces between symbol and =
    replace_string(filename=filename, pattern='[ \\t]{1,}\\n', replace_with='\\n', encoding=encoding)           # Remove trailing whitespaces
    replace_string(filename=filename, pattern='\\{(?=[\\w_\\"=])', replace_with='{ ', encoding=encoding)        # Add spaces between symbol and {
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=])\\}', replace_with=' }', encoding=encoding)       # Add spaces between symbol and }
    replace_string(filename=filename, pattern='(?<=[^\\n])\\Z', replace_with='\\n', encoding=encoding)          # Add last line if file is missing
    replace_string(filename=filename, pattern='(?<=^)    ', replace_with='\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)        ', replace_with='\\t\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)        ', replace_with='\\t\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)    ', replace_with='\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='(?<=\\t)    ', replace_with='\\t', encoding=encoding, flag=re.MULTILINE)  # Fix cases of using spaces
    replace_string(filename=filename, pattern='^$\\n{2,}', replace_with='\\n', encoding=encoding, flag=re.MULTILINE)          # Add last line if file is missing
    replace_string(filename=filename, pattern='limit = \\{\\n\\t+(has_template = .*?)\\n\\t+\\}', replace_with='limit = { \\1 }', encoding=encoding)
    replace_string(filename=filename, pattern='set_technology = \\{\\n\\t+(.+?)\\n\\t+\\}', replace_with='set_technology = { \\1 }', encoding=encoding)
    replace_string(filename=filename, pattern='delete_unit_template_and_units = \\{[^}]*?\\n\\t+(division_template = \".*?\").*\\n\\t+(disband = \\w+).*\\n\\t+\\}', replace_with='delete_unit_template_and_units = { \\1 \\2 }', encoding=encoding)
    replace_string(filename=filename, pattern='delete_unit_template_and_units = \\{[^}]*?\\n\\t+(division_template = \".*?\").*\\n\\t+\\}', replace_with='delete_unit_template_and_units = { \\1 }', encoding=encoding)
    replace_string(filename=filename, pattern='target_array = allies', replace_with='target_array = faction_members', encoding=encoding)
    replace_string(filename=filename, pattern='activate_targeted_decision = \\{\\n\\t+(target = .*?)\\n\\t+(decision = .*?)\\n\\t+\\}', replace_with='activate_targeted_decision = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='activate_targeted_decision = \\{\\n\\t+(decision = .*?)\\n\\t+(target = .*?)\\n\\t+\\}', replace_with='activate_targeted_decision = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='activate_targeted_decision = \\{ (decision = .*?) (target = .*?) }', replace_with='activate_targeted_decision = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='remove_targeted_decision = \\{\\n\\t+(target = .*?)\\n\\t+(decision = .*?)\\n\\t+\\}', replace_with='remove_targeted_decision = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='remove_targeted_decision = \\{\\n\\t+(decision = .*?)\\n\\t+(target = .*?)\\n\\t+\\}', replace_with='remove_targeted_decision = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='remove_targeted_decision = \\{ (decision = .*?) (target = .*?) }', replace_with='remove_targeted_decision = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='has_game_rule = \\{\\n\\t+(rule = .*?)\\n\\t+(option = .*?)\\n\\t+\\}', replace_with='has_game_rule = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    replace_string(filename=filename, pattern='has_game_rule = \\{\\n\\t+(option = .*?)\\n\\t+(rule = .*?)\\n\\t+\\}', replace_with='has_game_rule = { \\2 \\1 }', encoding=encoding, flag=re.MULTILINE)

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+id = ([^ #]*?)\\n\\t+\\}', replace_with='country_event = \\1', encoding=encoding, flag=re.MULTILINE)                                                                  # base
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+id = ([^ #]*?)\\n\\t+\\}', replace_with='country_event = \\2 \\1', encoding=encoding, flag=re.MULTILINE)                                                     # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+id = ([^ #]*?)[ \\t]*?(#.*?)\\n\\t+\\}', replace_with='country_event = \\1 \\2', encoding=encoding, flag=re.MULTILINE)                                                # With comments

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                   # base
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(months = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                 # months
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 \\3 }', encoding=encoding, flag=re.MULTILINE)  # with random_days
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\2 }', encoding=encoding, flag=re.MULTILINE)  # with random_days
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                  # with hours
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 \\3 }', encoding=encoding, flag=re.MULTILINE) # with hours and random_hours
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\2 }', encoding=encoding, flag=re.MULTILINE) # with hours and random_hours
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\2 }', encoding=encoding, flag=re.MULTILINE) # with days and random_hours

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)                      # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)               # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)                     # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 } \\1', encoding=encoding, flag=re.MULTILINE)              # With comments
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{.*?(#.*?)\\n\\t+(id = [^ #]*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\2 \\3 \\4 } \\1', encoding=encoding, flag=re.MULTILINE)                      # With comments

    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 } \\2', encoding=encoding, flag=re.MULTILINE)                                                  # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(days = [^ #]*?)\\n\\t+(random_days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\4 } \\2', encoding=encoding, flag=re.MULTILINE)                 # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 } \\2', encoding=encoding, flag=re.MULTILINE)                                                 # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) .*?(#.*?)\\n\\t+(hours = [^ #]*?)\\n\\t+(random_hours = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\3 \\4 } \\2', encoding=encoding, flag=re.MULTILINE)                 # With comments on id line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) (days = [^ #]*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)                                         # id and days on the same line
    replace_string(filename=filename, pattern='(?<!^)country_event = \\{\\n\\t+(id = [^ #]*?) (days = [^ #]*?) .*?(#.*?)\\n\\t+\\}', replace_with='country_event = { \\1 \\2 } \\3', encoding=encoding, flag=re.MULTILINE)                           # id and days and comments on the same line

    replace_string(filename=filename,
                   pattern='random_owned_controlled_state = \\{\\n(\\t+)limit = \\{\\n(\\1.*\\n)*?\\1\\}\\n(\\1.*\\n)*?\\t+add_building_construction = \\{\\n\\t+type = industrial_complex\\n\\t+level = 1(\\n\\1.*\\n)*?\\t+\\}\\n\\t+\\}',
                   replace_with='add_one_random_civilian_factory = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format
    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n(\t+)(\\1.*\n)*?\t+\n\t+add_building_construction = \\{\n\t+type = industrial_complex\n\t+level = 1\n\t+(\\1.*\n)*?\t+\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_civilian_factory = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format

    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n(\t+)limit = \\{\n(\\1.*\n)*?\\1\\}\n\t+add_building_construction = \\{\n\t+type = arms_factory\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_military_factory = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format
    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n\t+add_extra_state_shared_building_slots = 1\n\t+add_building_construction = \\{\n\t+type = arms_factory\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_military_factory = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format

    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n(\t+)limit = \\{\n(\\1.*\n)*?\\1\\}\n\t+add_building_construction = \\{\n\t+type = dockyard\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_dockyard = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format
    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n\t+add_extra_state_shared_building_slots = 1\n\t+add_building_construction = \\{\n\t+type = dockyard\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_dockyard = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format

    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n(\t+)limit = \\{\n(\\1.*\n)*?\\1\\}\n\t+add_extra_state_shared_building_slots = 1\n\t+add_building_construction = \\{\n\t+type = synthetic_refinery\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_synthetic_refinery = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format
    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n\t+add_extra_state_shared_building_slots = 1\n\t+add_building_construction = \\{\n\t+type = synthetic_refinery\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_synthetic_refinery = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format

    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n(\t+)limit = \\{\n(\\1.*\n)*?\\1\\}\n\t+add_extra_state_shared_building_slots = 1\n\t+add_building_construction = \\{\n\t+type = fuel_silo\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_fuel_silo = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format
    # replace_string(filename=filename,
    #                pattern='random_owned_controlled_state = \\{\n\t+add_extra_state_shared_building_slots = 1\n\t+add_building_construction = \\{\n\t+type = fuel_silo\n\t+level = 1\n\t+instant_build = yes\n\t+\\}\n\t+\\}',
    #                replace_with='add_one_random_fuel_silo = yes', encoding=encoding, flag=re.MULTILINE)                           # Factory format

    # replace_string(filename=filename, pattern='ai_will_do = \\{\\n\\t+(factor = [^ \\t]*?)\\n\\t+\\}', replace_with='ai_will_do = { \\1 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='ai_will_do = \\{\\n\\t+(base = [^ \\t]*?)\\n\\t+\\}', replace_with='ai_will_do = { \\1 }', encoding=encoding, flag=re.MULTILINE)

    # replace_string(filename=filename, pattern='set_variable = \\{\\n\\t+(var = .*?)\\n\\t+(value = .*?)\\n\\t+\\}', replace_with='set_variable = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='set_variable = \\{\\n\\t+(.*?) = (.*?)\\n\\t+\\}', replace_with='set_variable = { \\1 = \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='set_variable = \\{ var = (.*?) value = (.*?) \\}', replace_with='set_variable = { \\1 = \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='add_to_variable = \\{\\n\\t+(var = .*?)\\n\\t+(value = .*?)\\n\\t+\\}', replace_with='add_to_variable = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='add_to_variable = \\{\\n\\t+(.*?) = (.*?)\\n\\t+\\}', replace_with='add_to_variable = { \\1 = \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='add_to_variable = \\{ var = (.*?) value = (.*?) \\}', replace_with='add_to_variable = { \\1 = \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='subtract_from_variable = \\{\\n\\t+(var = .*?)\\n\\t+(value = .*?)\\n\\t+\\}', replace_with='subtract_from_variable = { \\1 \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='subtract_from_variable = \\{\\n\\t+(.*?) = (.*?)\\n\\t+\\}', replace_with='subtract_from_variable = { \\1 = \\2 }', encoding=encoding, flag=re.MULTILINE)
    # replace_string(filename=filename, pattern='subtract_from_variable = \\{ var = (.*?) value = (.*?) \\}', replace_with='subtract_from_variable = { \\1 = \\2 }', encoding=encoding, flag=re.MULTILINE)


def apply_formatting_loc(filename, encoding="utf-8-sig"):
    replace_string(filename=filename, pattern='[ \\t]{1,}\\n', replace_with='\\n', encoding=encoding)           # Remove trailing whitespaces
    replace_string(filename=filename, pattern='\\{(?=[\\w_\\"=])', replace_with='{ ', encoding=encoding)        # Add spaces between symbol and {
    replace_string(filename=filename, pattern='(?<=[\\w_\\"=])\\}', replace_with=' }', encoding=encoding)       # Add spaces between symbol and }
    replace_string(filename=filename, pattern='(?<=[^\\n])\\Z', replace_with='\\n', encoding=encoding)          # Add last line if file is missing
    replace_string(filename=filename, pattern=':[0-9] ', replace_with=': ', encoding=encoding)                      # Purge version control
    replace_string(filename=filename, pattern='^$\\n{2,}', replace_with='\\n', encoding=encoding, flag=re.MULTILINE)          # Add last line if file is missing
    replace_string(filename=filename, pattern='^([^ #\\n]+?:) ', replace_with=' \\1 ', encoding=encoding, flag=re.MULTILINE)  # Add whitespace if the line doesn't start with


def apply_formatting_characters(filename, encoding="utf-8"):
    replace_string(filename=filename, pattern='\\t*ai_will_do = \\{ factor = 1 \\}.*\n', replace_with='', encoding=encoding)                  # Delete ai factors from characters files
    replace_string(filename=filename, pattern='\\t*ai_will_do = \\{.*\\n\\t*factor = 1.*\\n\\t*\\}.*\n', replace_with='', encoding=encoding)  # Delete ai factors from characters files


def format_kaiserreich(username, mod_name):
    runner = TestRunner(username, mod_name)
    filepath_common = f'{runner.full_path_to_mod}common\\'
    filepath_history = f'{runner.full_path_to_mod}history\\'
    filepath_events = f'{runner.full_path_to_mod}events\\'
    filepath_loc = f'{runner.full_path_to_mod}localisation\\'
    filepath_characters = f'{runner.full_path_to_mod}common\\characters\\'
    filepath_unit_names_divisions = f'{runner.full_path_to_mod}common\\units\\names_divisions\\'
    filepath_unit_names_ships = f'{runner.full_path_to_mod}common\\units\\names_ships\\'
    print(filepath_common)
    for filename in glob.iglob(filepath_common + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        apply_formatting(filename=filename)

    for filename in glob.iglob(filepath_history + '**/*.txt', recursive=True):
        if DataCleaner.skip_files(files_to_skip=FILES_TO_SKIP, filename=filename):
            continue
        apply_formatting(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_events + '**/*.txt', recursive=True):
        apply_formatting(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_unit_names_divisions + '**/*.txt', recursive=True):
        apply_formatting(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_unit_names_ships + '**/*.txt', recursive=True):
        apply_formatting(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_loc + '**/*.yml', recursive=True):
        apply_formatting_loc(filename=filename, encoding="utf-8-sig")

    for filename in glob.iglob(filepath_characters + '**/*.txt', recursive=True):
        apply_formatting_characters(filename=filename)


if __name__ == '__main__':
    format_kaiserreich(username="VADIM", mod_name="Kaiserreich Dev Build")
