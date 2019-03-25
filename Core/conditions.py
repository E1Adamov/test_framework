from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException
ERRORS = StaleElementReferenceException or NoSuchElementException


class Condition:
    def __init__(self, locator):
        self.locator = locator

    def __call__(self, driver):
        try:
            return self.action(driver)
        except ERRORS:
            return False

    def action(self, driver):
        return False


class PresenceOfAllElementsWithExactTexts(Condition):
    """
    Expected condition for waiting for all elements  with given texts within the given scope
    """

    def __init__(self, locator, expected_element_texts):
        super().__init__(locator)
        self.expected_element_texts = self.texts_sort_lower(expected_element_texts)
        self.actual_element_texts = None

    @staticmethod
    def texts_sort_lower(texts):
        if isinstance(texts, list):
            return sorted([text.lower() for text in texts])
        else:
            return [texts.lower()]

    def action(self, driver):
        print(f'The nasty locator is: {self.locator}')
        elements = driver.find_elements_by_xpath(self.locator[1])
        print(f'Found {len(elements)} elements')
        self.actual_element_texts = sorted([element.text for element in elements])

        if self.actual_element_texts == self.expected_element_texts:
            return elements


class ElementPresent(Condition):
    """
    Expected condition to check if an element is present (search by xpath)
    """
    def action(self, driver):
        element = driver.find_element_by_xpath(self.locator)
        return element


class ElementVisible(Condition):
    """
    Expected condition to check if an element is visible (search by xpath)
    """
    def action(self, driver):
        element = driver.find_element_by_xpath(self.locator)
        if element.is_displayed():
            return element
