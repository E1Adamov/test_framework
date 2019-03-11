from Core.url import *
from Tests.base_test import BaseTest, setup
from Core.tools import *


class TestTodoMVC(BaseTest):

    def test_tasks_life_cycle(self):

        go_to(BASE_URL)

        add("a")
        assert_all_todos(active='a')

        add('b')
        assert_all_todos(active=['a', 'b'])

        edit('a', 'edited a')
        assert_all_todos(active=['edited a', 'b'])

        toggle('b')
        assert_all_todos(active=['edited a'], completed='b')

        toggle('b')
        assert_all_todos(active=['edited a', 'b'])

        delete('edited a')
        assert_all_todos(active='b')

        add('c')
        assert_all_todos(active=['b', 'c'])

        toggle('c')
        assert_all_todos(active='b', completed='c')

        clear_completed()
        assert_all_todos(active='b')
