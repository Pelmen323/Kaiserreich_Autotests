import logging
from timeit import default_timer as timer
import os
import pytest

from ..core.runner import TestRunner


def pytest_addoption(parser):
    parser.addoption('--username', action='store', default='VADIM',
                     help="Specify your system username in \\documents folder of which the modification is located.")
    parser.addoption('--mod_name', action='store', default='Kaiserreich Dev Build',
                     help="Specify your mod folder name.")
    parser.addoption('--repo_path', action='store', default=os.getenv("MOD_REPO_PATH", None),
                     help="Direct path to the mod folder. Use this for CI.")


@pytest.fixture
def test_runner(request):
    """
    This fixture initializes the TestRunner with appropriate paths for local or CI execution.
    """
    start = timer()
    repo_path = request.config.getoption("--repo_path")  # Direct path (for CI)
    username = request.config.getoption("--username")    # Username (for local)
    mod_name = request.config.getoption("--mod_name")    # Mod name (for local)

    # Initialize TestRunner
    if repo_path:
        runner = TestRunner(repo_path=repo_path)
    else:
        runner = TestRunner(username=username, mod_name=mod_name)

    yield runner
    end = timer()
    logging.debug(f"The test finished in {round(end - start, 3)} seconds!")
