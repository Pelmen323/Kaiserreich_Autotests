##########################
# Test script to check for advisors having invalid ledger line
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..test_classes.generic_test_class import ResultsReporter
from ..test_classes.localization_class import Localization
from ..test_classes.national_focus_class import (National_focus,
                                                 NationalFocusFactory)

FALSE_POSITIVES = ['nee_country_select_screen', 'nee_blank']
FOCUSES_NO_DESC = ['wls_', 'sco_', 'yun_', 'mnt_', 'imro_', 'kdr_', 'bat_', 'kor_']


def test_check_national_focus_contents(test_runner: object):
    """Test national focuses contents
    Args:
        test_runner (object): test object generated by conftest file
    """
    national_focuses, paths = National_focus.get_all_national_focuses(test_runner=test_runner, return_paths=True)
    loc_keys = Localization.get_all_loc_keys(test_runner=test_runner)
    results = []
    print(len(national_focuses))

    for foc_code in national_focuses:
        focus = NationalFocusFactory(focus=foc_code)
        # Skips
        if focus.id in FALSE_POSITIVES:
            continue

        # 1. Missing focus ID
        if not focus.id:
            results.append((foc_code.replace('\t', '').replace('\n', '  '), paths[foc_code], "Missing focus id"))
            continue

        # 2. Focus GFX
        if not focus.icon:
            results.append((focus.id, paths[foc_code], "Missing focus gfx path"))

        # 3. Focus position
        if 'x =' not in foc_code:
            results.append((focus.id, paths[foc_code], "Missing focus x axis"))
        if 'y =' not in foc_code:
            results.append((focus.id, paths[foc_code], "Missing focus y axis"))

        # 4. Costs
        if not focus.cost:
            results.append((focus.id, paths[foc_code], "Missing cost"))
        else:
            if int(focus.cost) > 100:
                results.append((focus.id, paths[foc_code], "Encountered focus duration > 700 days"))
            elif int(focus.cost) < 0:
                results.append((focus.id, paths[foc_code], "Encountered focus duration < 0 days"))

        # 5. Reward
        if not focus.completion_reward:
            results.append((focus.id, paths[foc_code], "Missing completion reward"))
        else:
            # Logging
            try:
                focus_logging = re.findall('log = ".*"', focus.completion_reward)[0]
            except IndexError:
                results.append((focus.id, paths[foc_code], "Missing logging - completion reward"))
                continue
            if f'focus {focus.id}' not in focus_logging:
                results.append((focus.id, focus_logging, paths[foc_code], "Completion - Logging line doesn't contain focus id"))

        if focus.select_effect:
            # Logging
            try:
                focus_logging = re.findall('log = ".*"', focus.select_effect)[0]
            except IndexError:
                results.append((focus.id, paths[foc_code], "Missing logging - select effect"))
                continue
            if f'select focus {focus.id}' not in focus_logging:
                results.append((focus.id, focus_logging, paths[foc_code], "Select effect - logging line doesn't contain focus id"))

        # 6. Check for dynamic loc in focus name loc
        if focus.id in loc_keys.keys():
            if "[" in loc_keys[focus.id]:       # Either scripted loc or variable
                if not focus.dynamic:
                    results.append((focus.id, paths[foc_code], "Missing `dynamic = yes` - scripted loc/variable in focus name"))

        # 7. Focus name check
        if focus.id not in loc_keys.keys():
            if focus.text is False:
                results.append((focus.id, paths[foc_code], "Both focus id and text are not present in loc keys"))
            elif focus.text not in loc_keys.keys():
                results.append((focus.id, paths[foc_code], "Both focus id and text are not present in loc keys"))
            elif loc_keys[focus.text] == "":
                results.append((focus.id, paths[foc_code], "Both focus id and text are not present in loc keys"))
        elif loc_keys[focus.id] == "":
            results.append((focus.id, paths[foc_code], "Both focus id and text are not present in loc keys"))

        # 8. Focus desc
        if len([i for i in FOCUSES_NO_DESC if i in focus.id]) == 0 and not focus.puppet_only_focus:             # Skipping specific focuses - they are puppet-only
            if f'{focus.id}_desc' not in loc_keys.keys():
                if focus.text is False:
                    results.append((focus.id, paths[foc_code], "Focus desc is not present in loc keys"))
                elif f'{focus.text}_desc' not in loc_keys.keys():
                    results.append((focus.id, paths[foc_code], "Focus desc is not present in loc keys"))
                elif loc_keys[f'{focus.text}_desc'] == "":
                    results.append((focus.id, paths[foc_code], "Focus desc is not present in loc keys"))
            elif len(loc_keys[f'{focus.id}_desc']) < 6:
                results.append((focus.id, paths[foc_code], "Focus desc is not present in loc keys"))

        # 9. War declaration - will_lead_to_war_with
        if 'create_wargoal' in foc_code or 'declare_war_on = {' in foc_code:
            if not focus.will_lead_to_war_with:
                results.append((focus.id, paths[foc_code], "The focus is starting war/generating wargoal but doesn't have 'will_lead_to_war_with'"))

    ResultsReporter.report_results(results=results, message="Issues during focuses parsing were encountered. Check console output")
