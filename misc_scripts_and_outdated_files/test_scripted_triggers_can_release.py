##########################
# Test script to check can_release_X triggers that do not have NOT = { is_claimed_by = ROOT }
# By Pelmen, https://github.com/Pelmen323
##########################
import re
import pytest
from test_classes.scripted_triggers_class import ScriptedTriggers

from test_classes.generic_test_class import ResultsReporter

FALSE_POSITIVES = [
    'can_release_italian_federation',
    'can_release_legation_ports_basic_options',
    'can_release_inner_mongolia_trigger',
    'can_release_tibetan_borderlands_trigger',
    'can_release_chinese_ally'
]


@pytest.mark.smoke
@pytest.mark.kr_specific
def test_check_scripted_triggers_can_release(test_runner: object):
    results = []

    scripted_triggers = ScriptedTriggers.get_all_scripted_triggers(test_runner=test_runner, lowercase=False)

    for trigger in scripted_triggers:
        if trigger.startswith('can_release'):
            if 'NOT = { is_claimed_by = ROOT }' not in trigger:
                trigger_name = re.findall('^(\\S+) = \\{', trigger, flags=re.MULTILINE)[0]
                if trigger_name not in FALSE_POSITIVES:
                    results.append(trigger_name)

    ResultsReporter.report_results(results=results, message="Issues with can_release triggers found - missing 'NOT = { is_claimed_by = ROOT }'")
