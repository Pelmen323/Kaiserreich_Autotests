import logging
from timeit import default_timer as timer
import pytest
from ..core.runner import TestRunner


def pytest_addoption(parser):
    parser.addoption('--username', action='store', default='VADIM',
                     help="Specify your system username in \\documents folder of which the modification is located. Example\
                         C:\\Users\\My_username\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\mod_name\\")

    parser.addoption('--mod_name', action='store', default='Kaiserreich Dev Build',
                     help="Specify your mod folder name. Example\
                         C:\\Users\\My_username\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\mod_name\\")


@pytest.fixture
def test_runner(request):
    """
    This fixture passes class with test data, prints messages as well as times the test execution time and prints to console
    """
    start = timer()
    username = request.config.getoption("--username")
    mod_name = request.config.getoption("--mod_name")
    yield TestRunner(username=username, mod_name=mod_name)
    end = timer()
    logging.debug(f"The test is finished in {round(end-start, 3)} seconds!")
