# Pytest Tests for Kaiserreich

Repository for .py tests for [Kaiserreich](https://steamcommunity.com/workshop/filedetails/?id=1521695605) with the possibility to set up Jenkins as a runner.
It can be used 'as is' for Kaiserreich users, they only need to pass their system username in which doc folder the project is located and the name of the mod folder (see screenshots lower). For other HOI4 projects, it can be used as well but no support is provided.

The general idea of the project is to automate the scenarios testing that is almost impossible to verify otherwise (they can be checked manually via CWTools in some cases, but my solution benefits from all automation perks - it is never tired, fast and provides almost instant feedback).
Tests are NOT running the game, instead, they parse and analyze the codebase.
Repository is constantly updated - tests are mostly created upon finding bugs.

In-built multithreading support and high-performance optimization, current full runtime - around 3 minutes with 6 cores utilised.

Requirements - Python installation with pytest and pytest-xdist plugins.

## Currently included tests
90+ tests, including:

*Advisors tests*
- usage of non-unique advisor tokens test (it causes bugs all over the place. Advisors should have unique tokens)
- usage of missing idea tokens in advisors activation
- invalid advisors costs test
- invalid advisors ledger lines test
- invalid advisors `not_already_hired_except_as` lines values
- advisors with invalid traits tests (all advisors slots)

*Characters tests*
- missing characters test (finds all characters that are checked via 'character =' or 'has_character =' but never defined)
- missing gfx portraits files test
- unused characters test (characters that exist but never recruited)
- duplicated characters test
- characters without loc keys in their names test
- characters with several advisor roles and missing `not_already_hired_except_as` lines
- characters (unit leaders) with missing small portrait links
- unit leaders with traits of unsupported type

*Cosmetic tags tests:*
- unused cosmetic tags test (finds all cosmetic tags that are set but never checked)
- unused cosmetic tags test - colors (finds all cosmetic tags colors that are never used)
- missing cosmetic tags test (finds all cosmetic tags that are not set but checked)

*Character flags tests:*
- unused character flags test (finds all character flags that are set but never checked)
- missing character flags test (finds all character flags that are not set but checked)
- cleared character flags test (finds all character flags that are not set but cleared)

*Country flags tests:*
- unused country flags test (finds all country flags that are set but never checked)
- missing country flags test (finds all country flags that are not set but checked)
- cleared country flags test (finds all country flags that are not set but cleared)

*Decisions tests:*
- decisions ai factor test (verifies that decisions and selectable missions have ai factors)
- unused decisions categories test
- duplicated decisions categories test
- duplicated decisions test
- war declaration decisions AI code test (checks if decisions have required AI code so AI performs better)

*Events tests*
- triggered-only events that are not triggered from outside test (check for events that are not triggered from outside but should)
- missing triggered events test
- events with no pictures

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
- Scripted loc brackets usage (finds oddities with vanilla scripted loc functions usage, such as missing brackets or unexpected following characters)
- Unused scripted loc test
- Usage of inline loc in scripted localisation files

*OOB files tests:*
- unused OOB files (files with unit templates and/or division/ships spawns that are not used)
- missing OOB files (files with unit templates and/or division/ships spawns that are missing)

*Opinion modifiers tests:*
- unused opinion modifiers test (finds all opinion modifiers that are set but never checked)

*Performance tests*
- a lot of tests related to unoptimized triggers usage
- focuses/decisions/events that can be optimized by using ideology flags tests

*Scripted triggers and effects tests:*
- unused scripted triggers test (finds all scripted triggers that are not used)
- unused scripted effects test (finds all scripted effects that are not used)

*State flags tests:*
- unused state flags test (finds all state flags that are set but never checked)
- missing state flags test (finds all state flags that are not set but checked)
- cleared state flags test (finds all state flags that are not set but cleared)

*Syntax tests:*
- missing 'limit' expression in if/elif conditions test
- usage of outdated syntax for armor equipment bonuses test (equipment -> chassis)
- usage of DLC-locked armor chassis for non NSB owners and vice versa test (owners of NSB have specific armor equipment available; non-DLC players have their own. Checks if these two types of equipment are not mixed)
- usage of outdated syntax for doctrines cost reduction test (tech_bonus -> doctrine_cost_reduction)
- railways file test (verifies the expected and actual number of provinces provided in /map/railways.txt file)
- usage of negative multiplication in ai factors test (negative multiplication is not what you want in 99% of cases)
- usage of 4+ digits after decimal point in ai factors test (HOI4 supports only 3 digits after decimal point)
- admirals and generals stats syntax tests (verifies generals and admirals have correct stats assigned)
- usage of vanilla .dds icons in armour variants test
- usage of incorrect equipment type in modifiers


### Project development timeline on the Jenkins graph

![Screenshot (2159)](https://user-images.githubusercontent.com/43440389/154126863-2af499b8-cf0b-4935-a214-924163b0e182.png)




## Pytest instructions
It allows to run test locally, all you need is python installation and installed 'pytest' and 'pytest-xdist' plugins

0. Create venv with pytest installed - 'pip install pytest' or 'pipenv install pytest' if you use pipenv
1. Install pytest-xdist - 'pip install pytest-xdist' or 'pipenv install pytest-xdist' if you use pipenv
2. Clone repository with tests
3. Change directory to repository directory
4. Run:
### pytest -v -s --tb=short "--username=xxx" "--mod_name=xxx" -n 6"
in console, replace **username** with your system username and **mod_name** with mod folder name, -n - number of your CPU cores
![Screenshot (1959)](https://user-images.githubusercontent.com/43440389/151341518-cf21b401-3c90-459d-80ce-02385a0166fe.png)


## Pytest-Jenkins instructions
It allows to run tests automatically based on specific triggers

0. Create a Python Virtual Environment, install Pytest via 'pip install pytest' or 'pipenv install pytest' if you use pipenv, install 'pytest-xdist' - 'pip install pytest-xdist' or 'pipenv install pytest-xdist' if you use pipenv
1. Install [Jenkins](https://www.jenkins.io/)
2. Install **Python Plugin** and **ShiningPanda Plugin** Jenkins plugins:
![Screenshot (1782)](https://user-images.githubusercontent.com/43440389/148402585-b2eaa6d6-7496-4b11-8643-1b1b17fa87ff.png)

3. Provide Git and Python paths in "Manage Jenkins/Global Tool Configuration/" (For Python - provide path to your virtual environment python.exe file)
![Screenshot (1783)](https://user-images.githubusercontent.com/43440389/148402687-6e20b249-e248-46b8-bca6-39af6920626f.png)

4. Create a new Job (Freestyle project)
5. Configure the job
- [GitHub repository](https://github.com/Pelmen323/Kaiserreich_Autotests), branch - main
- Build action - Custom Python Builder, path to your venv (not to exe), nature - Shell, command:
### pytest -v -s --tb=short "--username=xxx" "--mod_name=xxx" -n 6 --junitxml TestResults.xml
(replace **username** with your system username and **mod_name** with mod folder name, -n - number of your CPU cores)
![Screenshot (1961)](https://user-images.githubusercontent.com/43440389/151342210-319f1f31-e817-4283-8462-4279b4aa4e01.png)
- Post-Build Actions - Publish Junit test result report, test report xmls - *.xml
![Screenshot (1962)](https://user-images.githubusercontent.com/43440389/151342304-4a1a4855-e3b0-4ad5-ab7e-d75877be3084.png)

6. Setup the Build Triggers (or you can trigger the job manually)
7. Save the job

![Diagram](tests_coverage.svg)

