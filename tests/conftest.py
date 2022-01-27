import pytest
from timeit import default_timer as timer


class TestRunner:
    '''
    Test class that contains full filepath to mod folder
    Initialized via fixture, accepts 2 args, both passed via pytest console:
    -username: pass via --username=my_username, it is system user name in which docs mod is located
    -mod_name: pass via --mod_name=my_modname

    Example: C:\\Users\\username\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\mod_name\\
    '''
    def __init__(self, username: str, mod_name: str) -> None:
        self.username = username
        self.mod_name = mod_name
        self.full_path_to_mod = f"C:\\Users\\{username}\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\{mod_name}\\"


def pytest_addoption(parser):
    parser.addoption('--username', action='store', default='VADIM',
                     help="Specify your system username in \\documents folder of which the modification is located. Example\
                         C:\\Users\\My_username\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\mod_name")

    parser.addoption('--mod_name', action='store', default='Kaiserreich Dev Build',
                     help="Specify your mod folder name. Example\
                         C:\\Users\\My_username\\Documents\\Paradox Interactive\\Hearts of Iron IV\\mod\\mod_name")


@pytest.fixture
def test_runner(request):
    """
    This fixture passes class with test data, prints messages as well as times the test execution time and prints to console
    """
    print("    The test is started. Please wait...")
    start = timer()
    username = request.config.getoption("--username")
    mod_name = request.config.getoption("--mod_name")
    yield TestRunner(username=username, mod_name=mod_name)
    end = timer()
    print(f"    The test is finished in {round(end-start, 3)} seconds!")
