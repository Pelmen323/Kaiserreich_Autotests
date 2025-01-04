##########################
# Test script to check if events that are fired only once are having fire_only_once = yes flag
# By Pelmen, https://github.com/Pelmen323
##########################
import re

from ..test_classes.national_focus_class import National_focus, NationalFocusFactory
from ..test_classes.events_class import Events
from ..test_classes.decisions_class import Decisions, DecisionsFactory
from ..test_classes.characters_class import Characters
from ..test_classes.scripted_effects_class import ScriptedEffects
from ..test_classes.generic_test_class import ResultsReporter


def test_events_double_scoping(test_runner: object):
    all_events = Events.get_all_events(test_runner=test_runner, lowercase=True)
    all_characters = Characters.get_all_characters_names(test_runner=test_runner, return_paths=False, lowercase=True)
    results = []

    for event in all_events:
        event_id = re.findall('^\\tid = (\\S+)', event, flags=re.MULTILINE)[0]
        options = re.findall('^\\toption = \\{.*?^\\t\\}', event, flags=re.MULTILINE | re.DOTALL)
        if len(options) > 0:
            for option in options:
                option_name = re.findall('^\\t\\tname = (\\S+)', option, flags=re.MULTILINE)[0] if "\\t\\tname =" in option else event_id
                for character in all_characters:
                    if character in option:
                        if option.count(character + " = {") > 1:
                            results.append((option_name, character, option.count(character + " = {")))

    ResultsReporter.report_results(results=results, message="Those characters are scoped to multiple times in the same event option.")


def test_focuses_double_scoping(test_runner: object):
    all_focuses = National_focus.get_all_national_focuses(test_runner=test_runner, return_paths=False, lowercase=True)
    all_characters = Characters.get_all_characters_names(test_runner=test_runner, return_paths=False, lowercase=True)
    results = []

    for i in all_focuses:
        focus = NationalFocusFactory(focus=i)
        for character in all_characters:
            if focus.select_effect and character in focus.select_effect:
                if focus.select_effect.count(character + " = {") > 1:
                    results.append((f'{focus.id} - select effect', character, focus.select_effect.count(character + " = {")))
            if focus.completion_reward and character in focus.completion_reward:
                if focus.completion_reward.count(character + " = {") > 1:
                    results.append((f'{focus.id} - completion reward', character, focus.completion_reward.count(character + " = {")))

    ResultsReporter.report_results(results=results, message="Those characters are scoped to multiple times in the same focus.")


def test_decisions_double_scoping(test_runner: object):
    all_decisions = Decisions.get_all_decisions(test_runner=test_runner, return_paths=False, lowercase=True)
    all_characters = Characters.get_all_characters_names(test_runner=test_runner, return_paths=False, lowercase=True)
    results = []

    for i in all_decisions:
        decision = DecisionsFactory(dec=i)
        for character in all_characters:
            if decision.cancel_effect and character in decision.cancel_effect:
                if decision.cancel_effect.count(character + " = {") > 1:
                    results.append((f'{decision.token} - cancel effect', character, decision.cancel_effect.count(character + " = {")))
            if decision.complete_effect and character in decision.complete_effect:
                if decision.complete_effect.count(character + " = {") > 1:
                    results.append((f'{decision.token} - complete effect', character, decision.complete_effect.count(character + " = {")))
            if decision.remove_effect and character in decision.remove_effect:
                if decision.remove_effect.count(character + " = {") > 1:
                    results.append((f'{decision.token} - remove effect', character, decision.remove_effect.count(character + " = {")))

    ResultsReporter.report_results(results=results, message="Those characters are scoped to multiple times in the same decision.")


def test_effects_double_scoping(test_runner: object):
    all_effects = ScriptedEffects.get_all_scripted_effects(test_runner=test_runner, return_paths=False, lowercase=True)
    all_characters = Characters.get_all_characters_names(test_runner=test_runner, return_paths=False, lowercase=True)
    results = []

    for effect in all_effects:
        effect_token = re.findall('^(\\S+) = \\{', effect, flags=re.MULTILINE)[0]
        for character in all_characters:
            if character in effect:
                if effect.count(character + " = {") > 1:
                    results.append((effect_token, character, effect.count(character + " = {")))

    ResultsReporter.report_results(results=results, message="Those characters are scoped to multiple times in the same scripted effect.")
