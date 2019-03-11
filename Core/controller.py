from Core.web_elements import *
import Core.xpath as xpath
from contextlib import contextmanager
import Core.filters as filters


@contextmanager
def browse_filters():
    """
    Utility for assertions
    Remembers the current filter page
    Then yields some actions
    And then returns back to the initial filter page
    """
    current_filter = get_current_filter().upper()
    curr_filter_page = f'filters.{current_filter}'
    yield
    set_filter(eval(curr_filter_page))


def go_to_url(url):
    """
    Goes to a url
    :param url: e.g. "http://www.google.com"
    """
    Core.config.driver.get(url)


def s(locator):
    """
    Creates a smart object that explicitly waits for the expected element and returns it
    :param locator: xpath
    :return: a single web element, if it is discovered
    """
    return SmartWebElement(locator)


def ss(locator, texts):
    """
    Creates a smart object that explicitly waits for the expected elements to be found
    and to contain the specified texts (one text per element)
    :param locator: xpath to an element inside which the search will be made
    :param texts: texts of different web elements that are expected to be found
    :return: a texts that were actually discovered in the given scope
    """
    return Tasks(locator, texts)


def get_active(locator, flag=xpath.activate):
    """
    Utility for set_filter()
    Converts xpath of an inactive filter page to the same page but in active state
    :param locator: xpath
    :param flag: string injection to the xpath to make it active
    :return: modifies xpath of the locator
    """
    return flag.join([locator[:-1], locator[-1:]])


def set_filter(locator):
    """
    Switches to a filter page if they are available
    :param locator: xpath
    """
    if len(s(xpath.ACTIVE_FILTER)) != 0:
        s(locator).click()
        active_filter_locator = get_active(locator)
        assert s(active_filter_locator).get_attribute('class') == "selected"


def assert_active(active):
    """
    Asserts active tasks on the current filter page
    :param active: list of tasks that are expected to be active
    """
    active_todos = ss(xpath.ACTIVE_TODO_LIST, active)
    assert sorted(active) == sorted(active_todos)


def assert_completed(completed):
    """
    Asserts completed tasks on the current filter page
    :param completed: list of tasks that are expected to be in completed state
    """
    completed_todos = ss(xpath.COMPLETED_TODO_LIST, completed)
    assert sorted(completed) == sorted(completed_todos)


def get_current_filter():
    """
    Gets the current filter page
    :return: the current filter page in format: 'all', 'active', 'completed'
    """
    return s(xpath.ACTIVE_FILTER).text.lower()


def assert_todos(active, completed):
    """
    Asserts both active and completed tasks on the current filter page
    regardless of their state
    :param active: list of tasks that are expected to be active. Format: 'task1' or ['task1', 'task2']
    :param completed:  list of tasks that are expected to be completed. Format: 'task1' or ['task1', 'task2']
    :return:
    """

    if get_current_filter() == ('all' or 'active'):
        assert_active(active)

    if get_current_filter() == ('all' or 'completed'):
        assert_completed(completed)


def assert_items_left(expected_qty):
    """
    Asserts the 'items left' quantity (active only)
    :param expected_qty: quantity of the active tasks
    """
    actual_qty = int(s(xpath.ITEMS_LEFT).text)
    assert expected_qty == actual_qty
