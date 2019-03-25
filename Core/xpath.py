NEW_TODO = "//input[@class='new-todo']"
EXISTING_TODO = "//label[@can-dblclick='edit' and text()='{}']"
EDIT_TODO = "//li[div/label[text()='{}']]/input[@class='edit']"

TODO_LIST = "//input[@class='edit' and @can-enter = 'updateTodo']"
ACTIVE_TODO_LIST = "//ul[@class='todo-list']/li[@class='todo']//label"
COMPLETED_TODO_LIST = "//ul[@class='todo-list']/li[@class='todo completed']//label"

TOGGLE = "//li[div/label[text()='{}']]/div/input[@class='toggle']"
TOGGLE_ALL = "//label[@for='toggle-all']"

DELETE = "//li[div/label[text()='{}']]/div/button[@class='destroy']"
CLEAR_COMPLETED = "//button[@class='clear-completed  ']"
ITEMS_LEFT = "//span[@class='todo-count']/strong"

filter_ = "//ul[@class='filters']//a[@href='#!{}']"
activate = " and @class='selected'"
ACTIVE_FILTER = "//ul[@class='filters']//a[@class='selected']"
