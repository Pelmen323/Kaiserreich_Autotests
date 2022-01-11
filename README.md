# Pytest Tests for Kaiserreich

Repo for .py tests for Kaiserreich (can be run for every other HOI4 mod), with possibility to setup Jenkins as runner.

## Currently included tests:
- railways file test (verifies the expected and actual number of provinces provided in /map/railways.txt file)
- localization files typo check (parses loc files and finds commonly misspelled words, as well as prints correct variant)
- decisions ai factor test (verifies that decisions and selectable missions have ai factors)
- unused global flags test (finds all global flags that are set but never checked)
- unused country flags test (finds all country flags that are set but never checked)


## Pytest-Jenkins instructions:

0. Create a Python Virtual Environment, install Pytest via 'pip install pytest' or 'pipenv install pytest' if you use pipenv
1. Install Jenkins https://www.jenkins.io/
2. Install **Python Plugin** and **ShiningPanda Plugin** Jenkins plugins:
![Screenshot (1782)](https://user-images.githubusercontent.com/43440389/148402585-b2eaa6d6-7496-4b11-8643-1b1b17fa87ff.png)

3. Provide Git and Python paths in "Manage Jenkins/Global Tool Configuration/" (For Python - provide path to your virtual environment python.exe file)
![Screenshot (1783)](https://user-images.githubusercontent.com/43440389/148402687-6e20b249-e248-46b8-bca6-39af6920626f.png)

4. Create a new Job (Freestyle project)
5. Configure the job
- git repo - https://github.com/Pelmen323/Kaiserreich_Jenkins_PyTests, branch - main
- Build action - Custom Python Builder, path to your venv (not to exe), nature - Shell, command - 'pytest -v -s --junitxml TestResults.xml')
- Post-Build Actions - Publish Junit test result report, test report xmls - *.xml
![Screenshot (1786)](https://user-images.githubusercontent.com/43440389/148402821-1feb37ad-90cd-4a47-83dd-c3a34a0d2727.png)

6. Setup the Build Triggers (or you can trigger the job manually)
7. Save the job
