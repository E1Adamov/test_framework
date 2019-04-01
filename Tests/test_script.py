from Core.url import *
from Tests.base_test import *
from Core.tools import *


class TestTodoMVC(BaseTest):

    def test_tasks_life_cycle(self):

        go_to(BASE_URL)
        assert_all_todos()

        add('task 1')
        assert_all_todos(active=['task 1'])

        add('task 2')
        assert_all_todos(active=['task 1', 'task 2'])
        assert_clear_completed(False)

        toggle('task 1')
        assert_all_todos(active=['task 2'], completed=['task 1'])

        edit('task 1', 'task edited 1')
        assert_all_todos(active=['task 2'], completed=['task edited 1'])

        edit('task 2', 'task edited 2')
        assert_all_todos(active=['task edited 2'], completed=['task edited 1'])
        assert_clear_completed(True)

        add('task 3')
        assert_all_todos(active=['task edited 2', 'task 3'], completed=['task edited 1'])
        assert_clear_completed(True)

        toggle_all()
        assert_all_todos(completed=['task edited 2', 'task 3', 'task edited 1'])

        clear_completed()
        assert_all_todos()

    def test_load(self):  # TODO
        pass
