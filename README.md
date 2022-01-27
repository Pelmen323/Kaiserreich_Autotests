# Pytest Tests for Kaiserreich

Repo for .py tests for Kaiserreich (can be run for every other HOI4 mod), with possibility to setup Jenkins as runner.
It can be used 'as is' for Kaiserreich user, they only need to pass their system username in which doc folder the project is located and name of mod folder (see screenshots lower). For other HOI4 projects it can be used as well but requires manual verification of each error and adjusting FALSE_POSITIVES iterables respectively

General idea of the project is to automate the scenarios testing that are almost impossible to verify otherwise (they can be checked manually via CWTools in some cases, but my solution benefits from all automation perks - it is never tired and it performs thousands of operation per second). Tests are NOT running the game, instead they parse and analyze the codebase

Current full run time - around 4 minutes

## Currently included tests:

- usage of remove_all_leader_roles effect test (the effect causes CTDs. Test verifies that this effect is not used)
- usage of remove_country_leader_role effect test (the effect causes CTDs. Test verifies that this effect is not used)
- usage of retire_character outside of tooltip (retire_character does not remove the character from HoS slot if he is a current country leader. It should be replaced with retire = yes which removes char from all ideology slots)
- railways file test (verifies the expected and actual number of provinces provided in /map/railways.txt file)
- localization files typo check (parses loc files and finds commonly misspelled words, as well as prints correct variant)
- decisions ai factor test (verifies that decisions and selectable missions have ai factors)
- unused global flags test (finds all global flags that are set but never checked)
- unused country flags test (finds all country flags that are set but never checked)
- unused state flags test (finds all state flags that are set but never checked)
- missing global flags test (finds all global flags that are not set but checked)
- missing country flags test (finds all country flags that are not set but checked)
- missing state flags test (finds all state flags that are not set but checked)
- cleared global flags test (finds all global flags that are not set but cleared)
- cleared country flags test (finds all country flags that are not set but cleared)
- cleared state flags test (finds all state flags that are not set but cleared)


## Pytest instructions:
It allows to run test locally, all you need is python installation and installed 'pytest' plugin
0. Create venv with pytest installed - 'pip install pytest' or 'pipenv install pytest' if you use pipenv
1. Clone repo with tests
2. Change directory to repo directory
3. Run:
### pytest -v -s "--username=VADIM" "--mod_name=Kaiserreich Dev Build"**
in console, replace **username** with your system username and **mod_name** with mod folder name
![Screenshot (1959)](https://user-images.githubusercontent.com/43440389/151341518-cf21b401-3c90-459d-80ce-02385a0166fe.png)


## Pytest-Jenkins instructions:
It allows to run tests automatically based on specific triggers
0. Create a Python Virtual Environment, install Pytest via 'pip install pytest' or 'pipenv install pytest' if you use pipenv
1. Install Jenkins https://www.jenkins.io/
2. Install **Python Plugin** and **ShiningPanda Plugin** Jenkins plugins:
![Screenshot (1782)](https://user-images.githubusercontent.com/43440389/148402585-b2eaa6d6-7496-4b11-8643-1b1b17fa87ff.png)

3. Provide Git and Python paths in "Manage Jenkins/Global Tool Configuration/" (For Python - provide path to your virtual environment python.exe file)
![Screenshot (1783)](https://user-images.githubusercontent.com/43440389/148402687-6e20b249-e248-46b8-bca6-39af6920626f.png)

4. Create a new Job (Freestyle project)
5. Configure the job
- git repo - https://github.com/Pelmen323/Kaiserreich_Jenkins_PyTests, branch - main
- Build action - Custom Python Builder, path to your venv (not to exe), nature - Shell, command:
### pytest -v -s "--username=VADIM" "--mod_name=Kaiserreich Dev Build" --junitxml TestResults.xml
(replace **username** with your system username and **mod_name** with mod folder name)
![Screenshot (1961)](https://user-images.githubusercontent.com/43440389/151342210-319f1f31-e817-4283-8462-4279b4aa4e01.png)
- Post-Build Actions - Publish Junit test result report, test report xmls - *.xml
![Screenshot (1962)](https://user-images.githubusercontent.com/43440389/151342304-4a1a4855-e3b0-4ad5-ab7e-d75877be3084.png)

6. Setup the Build Triggers (or you can trigger the job manually)
7. Save the job
