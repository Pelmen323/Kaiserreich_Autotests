# Pytest Tests for Kaiserreich

Repo for .py tests for Kaiserreich, can be run via Jenkins:

Pytest-Jenkins instructions:

0. Create a Python Virtual Environment, install Pytest via 'pip install pytest' or 'pipenv install pytest' if you use pipenv
1. Install Jenkins https://www.jenkins.io/
2. Install **Python Plugin** and **ShiningPanda Plugin** Jenkins plugins:
3. Provide Git and Python paths in "Manage Jenkins/Global Tool Configuration/" (For Python - provide path to your virtual environment python.exe file)
4. Create a new Job
5. Configure the job
- git repo - https://github.com/Pelmen323/Kaiserreich_Jenkins_PyTests, branch - main
- Build action - Custom Python Builder, path to your venv (not to exe), nature - Shell, command - 'pytest -v -s --junitxml TestResults.xml')
- Post-Build Actions - Publish Junit test result report, test report xmls - *.xml
6. Setup the Build Triggers
7. Save the job


Currently included tests:
- railways file test (verifies the expected and actual number of provinces provided in /map/railways.txt file)
- localization files typo check (parses loc files and finds commonly misspelled words, as well as prints correct variant)
