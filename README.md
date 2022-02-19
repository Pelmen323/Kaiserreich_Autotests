# Pytest Tests for Kaiserreich

Repo for .py tests for Kaiserreich (can be run for every other HOI4 mod), with possibility to setup Jenkins as runner.
It can be used 'as is' for Kaiserreich user, they only need to pass their system username in which doc folder the project is located and name of mod folder (see screenshots lower). For other HOI4 projects it can be used as well but requires manual verification of each error and adjusting FALSE_POSITIVES iterables respectively

General idea of the project is to automate the scenarios testing that are almost impossible to verify otherwise (they can be checked manually via CWTools in some cases, but my solution benefits from all automation perks - it is never tired and it performs thousands of operation per second). Tests are NOT running the game, instead they parse and analyze the codebase. Tests are mostly created upon finding the issue - to find all affected scenarios and to prevent bugs from reappearing in the future

In-built multithreading support and high performance optimization, current full run time - around 80 seconds.

Requirements - Python installation with pytest and pytest-xdist plugins installed

## Currently included tests:
34 tests:

*Characters tests*
- missing characters test (finds all characters that are checked via 'character =' or 'has_character =' but never defined)
- usage of remove_all_leader_roles effect test (the effect causes CTDs. Test verifies that this effect is not used)
- usage of remove_country_leader_role effect test (the effect causes CTDs. Test verifies that this effect is not used)

*Country flags tests:*
- unused country flags test (finds all country flags that are set but never checked)
- missing country flags test (finds all country flags that are not set but checked)
- cleared country flags test (finds all country flags that are not set but cleared)

*Events tests*
- triggered-only events that are not triggered from outside test (check for events that are not triggered from outside but should)

*Event targets tests*
- unused event targets test (finds all event targets that are set but never checked)
- missing event targets test (finds event targets that are not set but checked)
- cleared event targets test (finds all event targets that are not set but cleared)

*Global flags tests:*
- unused global flags test (finds all global flags that are set but never checked)
- missing global flags test (finds all global flags that are not set but checked)
- cleared global flags test (finds all global flags that are not set but cleared)

*Ideas tests:*
- unused ideas test (finds all ideas that are set but never checked)

*Localization tests*
- localization files typo check (parses loc files and finds commonly misspelled words, as well as prints correct variant)
- localization files syntax violations
- localization files unused loc entries

*OOB files tests:*
- unused OOB files (files with unit templates and/or division/ships spawns that are not used)
- missing OOB files (files with unit templates and/or division/ships spawns that are missing)

*Opinion modifiers tests:*
- unused opinion modifiers test (finds all opinion modifiers that are set but never checked)

*Scripted triggers and effects tests:*
- unused scripted triggers test (finds all scripted triggers that are not used)
- unused scripted effects test (finds all scripted effects that are not used)

*State flags tests:*
- unused state flags test (finds all state flags that are set but never checked)
- missing state flags test (finds all state flags that are not set but checked)
- cleared state flags test (finds all state flags that are not set but cleared)

*Syntax tests:*
- usage of outdated syntax for armor equipment bonuses test (_equipment -> _chassis)
- usage of DLC-locked armor chassis for non NSB owners and vice versa test (owners of NSB have specific armor equipment available; non-DLC players have their own. Checks if these two types of equipment are not mixed)
- usage of outdated syntax for doctrines cost reduction test (tech_bonus -> doctrine_cost_reduction)
- railways file test (verifies the expected and actual number of provinces provided in /map/railways.txt file)
- decisions ai factor test (verifies that decisions and selectable missions have ai factors)
- usage of negative multiplication in ai factors test (negative multiplication is not what you want in 99% of cases)
- usage of 4+ digits after decimal point in ai factors test (HOI4 supports only 3 digits after decimal point)
- admirals and generals stats syntax tests (verifies generals and admirals have correct stats assigned)
- usage of vanilla .dds icons in armour variants test


### Project development timeline on the Jenkins graph:

![Screenshot (2159)](https://user-images.githubusercontent.com/43440389/154126863-2af499b8-cf0b-4935-a214-924163b0e182.png)




## Pytest instructions:
It allows to run test locally, all you need is python installation and installed 'pytest' and 'pytest-xdist' plugins

0. Create venv with pytest installed - 'pip install pytest' or 'pipenv install pytest' if you use pipenv
1. Install pytest-xdist - 'pip install pytest-xdist' or 'pipenv install pytest-xdist' if you use pipenv
2. Clone repo with tests
3. Change directory to repo directory
4. Run:
### pytest -v -s --tb=short "--username=xxx" "--mod_name=xxx" -n 6"
in console, replace **username** with your system username and **mod_name** with mod folder name, -n - number of your CPU cores
![Screenshot (1959)](https://user-images.githubusercontent.com/43440389/151341518-cf21b401-3c90-459d-80ce-02385a0166fe.png)


## Pytest-Jenkins instructions:
It allows to run tests automatically based on specific triggers

0. Create a Python Virtual Environment, install Pytest via 'pip install pytest' or 'pipenv install pytest' if you use pipenv, install 'pytest-xdist' - 'pip install pytest-xdist' or 'pipenv install pytest-xdist' if you use pipenv
1. Install Jenkins https://www.jenkins.io/
2. Install **Python Plugin** and **ShiningPanda Plugin** Jenkins plugins:
![Screenshot (1782)](https://user-images.githubusercontent.com/43440389/148402585-b2eaa6d6-7496-4b11-8643-1b1b17fa87ff.png)

3. Provide Git and Python paths in "Manage Jenkins/Global Tool Configuration/" (For Python - provide path to your virtual environment python.exe file)
![Screenshot (1783)](https://user-images.githubusercontent.com/43440389/148402687-6e20b249-e248-46b8-bca6-39af6920626f.png)

4. Create a new Job (Freestyle project)
5. Configure the job
- git repo - https://github.com/Pelmen323/Kaiserreich_Autotests, branch - main
- Build action - Custom Python Builder, path to your venv (not to exe), nature - Shell, command:
### pytest -v -s --tb=short "--username=xxx" "--mod_name=xxx" -n 6 --junitxml TestResults.xml
(replace **username** with your system username and **mod_name** with mod folder name, -n - number of your CPU cores)
![Screenshot (1961)](https://user-images.githubusercontent.com/43440389/151342210-319f1f31-e817-4283-8462-4279b4aa4e01.png)
- Post-Build Actions - Publish Junit test result report, test report xmls - *.xml
![Screenshot (1962)](https://user-images.githubusercontent.com/43440389/151342304-4a1a4855-e3b0-4ad5-ab7e-d75877be3084.png)

6. Setup the Build Triggers (or you can trigger the job manually)
7. Save the job
