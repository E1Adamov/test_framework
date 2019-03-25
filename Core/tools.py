from Core.controller import *
from Core.filters import *


def go_to(url):
    """
    :param url: e.g. "http://www.google.com"
    """
    Core.config.driver.get(url)


def add(todo_text):
    """
    Adds a new task
    :param todo_text: the text that you want to put in the task
    """
    s(xpath.NEW_TODO).send_keys(todo_text + Keys.ENTER)


def edit(old_text, new_text):
    """
    Finds a task with the given text and replaces the text with the new one.
    Note that if you're on a filtered page, then some tasks may be temporary
    invisible. Therefore it may be impossible to edit them from the current
    filter page and you need to switch to another filter page
    :param old_text: task text to search for
    :param new_text: the new text of the found task
    :return:
    """
    s(xpath.EXISTING_TODO.format(old_text)).double_click()
    s(xpath.EDIT_TODO.format(old_text)).set_value(new_text).press_enter()


def assert_all_todos(active=(), completed=()):
    """
    Asserts all tasks on all filter pages regardless of their state.
    Also, verifies the 'items left' number on each page of the filter.
    :param active: list of tasks that are expected to be active. Format: ['task1'] or ['task1', 'task2']
    :param completed:  list of tasks that are expected to be completed. Format: ['task1'] or ['task1', 'task2']
    """
    with browse_filters():
        for page in FILTERS:
            set_filter(page)
            assert_todos(active=active, completed=completed)
            assert_items_left(len(active))


def goto_filter(page):
    """
    Goes to a filter page
    :param page: from module filters.py: ALL, ACTIVE, COMPLETED
    :return:
    """
    return set_filter(page)


def toggle(todo_text):
    """
    Toggles a task's state to the opposite one (active/completed)
    :param todo_text: the task's text for the search
    """
    s(xpath.TOGGLE.format(todo_text)).click()


def delete(todo_text):
    """
    Permanently deletes a task
    :param todo_text: the task's text for the search
    """
    s(xpath.TOGGLE.format(todo_text)).hover()
    s(xpath.DELETE.format(todo_text)).click()


def clear_completed():
    """
    Clicks the 'clear completed' button
    """
    s(xpath.CLEAR_COMPLETED).click()


def assert_clear_completed(status):
    """
    This method was not included into the bundled assertion "assert_all_todos",
    because when the 'clear completed' button is not visible, waiting every
    time takes too long. So, it should be used explicitly.
    Verifies the presence of button "clear completed" that has to be visible only
    when completed tasks are available
    :param status: bool. True if it's expected to be visible
    """
    assert s(xpath.CLEAR_COMPLETED) == status


def toggle_all():
    """
    clicks the "toggle all" buttton
    """
    s(xpath.TOGGLE_ALL).click()
