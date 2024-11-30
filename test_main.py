import os 
import pytest
import json
from task_manager import TaskManager
from task import Task
from unittest.mock import patch

@pytest.fixture
def task_manager(tmpdir):
    temp_file = tmpdir.join('tasks.json')
    manager = TaskManager(filename=str(temp_file))
    return manager

def test_add_task(task_manager):
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    assert len(task_manager.tasks) == 1
    assert task_manager.tasks[0].title == 'заголовок'
    assert task_manager.tasks[0].description == 'описание'
    
@patch('builtins.input', side_effect = [1,'Новый заголовок'])
def test_edit_task_title(mock_input, task_manager):
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    task_manager.edit_task(1)
    TaskManager.input = lambda: '1'
    TaskManager.input = lambda: 'Новый заголовок'
    assert task_manager.tasks[0].title == 'Новый заголовок'
    
def test_del_task(task_manager):
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    assert len(task_manager.tasks) == 1
    task_manager.delete_task(1)
    assert len(task_manager.tasks) == 0

def test_list_tasks(capfd, task_manager):
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    task_manager.list_tasks()
    captured = capfd.readouterr()
    assert '2   заголовок   описание   категория        2020-11-21      низкий   не выполнено' in captured.out
    
def test_list_tasks_by_id(capfd, task_manager):
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    task_manager.add_task('Заголовок','Описание', 'Категория', '2020-11-21','Низкий', 'не выполнено')
    task_manager.get_task_by_id(2)
    captured = capfd.readouterr()
    assert '2   заголовок   описание   категория        2020-11-21      низкий   не выполнено' in captured.out
    
    