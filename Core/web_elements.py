import Core.config
from Core.conditions import *


from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys


def actions():
    """
    :return: a shortcut to action chains
    """
    return ActionChains(Core.config.driver)


class SmartWebElement:
    """
    Waiting element. Waits for the expected element to be present, and then can
    apply it's own or selenium's methods
    """

    def __init__(self, locator):
        self.locator = locator
        self.wait = WebDriverWait(Core.config.driver, Core.config.TIMEOUT)
        self.web_element = self.finder()

    def __len__(self):
        return 1 if self.web_element is not None else 0

    def finder(self):
        try:
            return self.wait.until(PresenceOfElement((By.XPATH, self.locator)))
        except TimeoutException as e:
            print(f'Element not found: {self.locator}')
            raise e

    def __getattr__(self, item):
        return getattr(self.web_element, item)

    def double_click(self):
        actions().double_click(self.web_element).perform()
        return self

    def set_value(self, value):
        self.web_element.send_keys(Keys.CONTROL + 'a')
        self.web_element.send_keys(value)
        return self

    def press_enter(self):
        self.web_element.send_keys(Keys.ENTER)


class Tasks:
    """
    Searches for elements that can be found by the given locator and waits for
    presence of all elements with texts. Returns the actual list of found texts
    for further assertion
    """
    def __init__(self, locator, texts):
        self.locator = locator
        self.todo_texts = texts
        self.wait = WebDriverWait(Core.config.driver, Core.config.TIMEOUT)
        self.web_elements = None
        self.texts = self.finder()

    def __iter__(self):
        return iter(self.texts)

    def __repr__(self):
        return self.texts

    def __str__(self):
        return str(self.texts)

    def __getitem__(self, item):
        return self.texts[item]

    def __len__(self):
        return len(self.texts)

    def __eq__(self, other):
        return self.texts == other

    def finder(self):

        if self.todo_texts:
            try:
                todos = self.wait.until(PresenceOfAllElementsWithExactTexts((By.XPATH, self.locator), self.todo_texts))
                return [i.text for i in todos]
            except TimeoutException as e:
                raise e

        self.web_elements = Core.config.driver.find_elements_by_xpath(self.locator)
        return tuple(i.text for i in self.web_elements)

    def get_attrs(self, attr):
        return [element.get_attribute(attr) for element in self.web_elements]
