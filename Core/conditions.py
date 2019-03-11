from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException, NoSuchElementException, TimeoutException


class PresenceOfAllElementsWithExactTexts:
    """
    Expected condition for waiting for all elements  with given texts within the given scope
    """

    def __init__(self, scope, expected_element_texts):
        self.locator = scope  # xpath
        self.expected_element_texts = self.texts_sort_lower(expected_element_texts)
        self.actual_element_texts = None

    @staticmethod
    def texts_sort_lower(texts):
        if isinstance(texts, list):
            return sorted([text.lower() for text in texts])
        else:
            return [texts.lower()]

    def __call__(self, driver):
        try:
            elements = EC._find_elements(driver, self.locator)
            self.actual_element_texts = sorted([todo.text for todo in elements])

            if self.actual_element_texts == self.expected_element_texts:
                return elements

        except StaleElementReferenceException or NoSuchElementException or TimeoutException:
            print('Expected:', self.expected_element_texts)
            print('Actual:', self.actual_element_texts)
            return False


class PresenceOfElement:
    """
    Expected condition for waiting for a given element
    """

    def __init__(self, locator):
        self.locator = locator  # xpath

    def __call__(self, driver):
        try:
            element = EC._find_element(driver, self.locator)
            return element if element else False
        except StaleElementReferenceException or NoSuchElementException or TimeoutException:
            return False
