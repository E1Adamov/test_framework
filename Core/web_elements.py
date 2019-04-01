from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys

import Core.config
from Core.conditions import *


def actions():
    """
    :return: a shortcut to action chains
    """
    return ActionChains(Core.config.driver)


class SmartWaitingWebElement:
    """
    Waiting element. Waits for the expected element to be present, and then can
    apply it's own or selenium's methods
    """

    def __init__(self, locator):
        self.locator = locator
        self.wd_wait = WebDriverWait(Core.config.driver, Core.config.TIMEOUT)
        self.default_conditions = ElementVisible
        self.web_element = self.find(self.locator)

    def __len__(self):
        return 1 if self.web_element is not None else 0

    def __eq__(self, other):
        return False is other if not self.web_element else True is other

    def __getattr__(self, item):
        if self.web_element:
            return getattr(self.web_element, item)

    def __str__(self):
        return self.locator

    def __repr__(self):
        return self.web_element

    def wait(self, *conditions):
        try:
            for condition in conditions:
                self.wd_wait.until(condition(self.locator), condition)
        except TimeoutException:
            pass

    def find(self, locator):
        try:
            self.wait(self.default_conditions)
            element = Core.config.driver.find_element_by_xpath(locator)
            return element
        except NoSuchElementException:
            return None

    def double_click(self):
        actions().double_click(self).perform()
        return self

    def set_value(self, value):
        self.web_element.send_keys(Keys.CONTROL + 'a')
        self.web_element.send_keys(value)
        return self

    def press_enter(self):
        self.web_element.send_keys(Keys.ENTER)

    def hover(self):
        actions().move_to_element(self).perform()
        return self


class SmartWaitingWebElementsList:
    """
    Searches for elements that can be found by the given locator and waits for
    presence of all elements with texts. Stores the actual texts and returns the
    list of actually found web elements with given texts
    """
    def __init__(self, locator, texts):
        self.locator = locator
        self.expected_texts = texts
        self.wd_wait = WebDriverWait(Core.config.driver, Core.config.TIMEOUT)
        self.default_conditions = PresenceOfAllElementsWithExactTexts
        self.web_elements = self.find(self.locator)
    
    def __getattr__(self, item):
        return [getattr(element, item) for element in self.web_elements]

    def __iter__(self):
        return iter(self.web_elements)

    def __repr__(self):
        return self.web_elements

    def __str__(self):
        return str(self.texts)

    def __getitem__(self, item):
        return self.web_elements[item]

    def __len__(self):
        return len(self.web_elements)

    def __eq__(self, other):
        return self.texts == other

    def find(self, locator):
        self.wait(self.default_conditions, self.expected_texts)
        elements = Core.config.driver.find_elements_by_xpath(locator)
        return elements

    def wait(self, *conditions, condition_args):
        try:
            for condition in conditions:
                self.wd_wait.until(condition(self.locator), condition)
        except TimeoutException:
            pass

    def get_attrs(self, attr):
        return [element.get_attribute(attr) for element in self.web_elements]

    @property
    def texts(self):
        if self.web_elements:
            return [element.text for element in self.web_elements]
        return None
