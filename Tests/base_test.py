import pytest
from time import sleep
from selenium.webdriver import Firefox, Chrome
import Core.config


@pytest.fixture(scope='class', params=[Chrome()])
def setup(request):
    """
    Sets up Pytest within a class scope with different browsers as parameters
    """
    Core.config.driver = request.param
    Core.config.driver.maximize_window()

    def teardown():
        """
        Closes the browsers after the tests are finished
        """
        sleep(2)
        Core.config.driver.quit()

    request.addfinalizer(teardown)


@pytest.mark.usefixtures('setup')
class BaseTest:
    """
    The class that inherits setup and passes further to its subclasses
    """
    pass
