import os
import json
from datetime import datetime, timedelta
from task import Task
from utils import pretty_print


class TaskManager:
    def __init__(self, filename="tasks.json"):
        self.filename = filename
        self.tasks = []
        self.collect_tasks()

    def collect_tasks(self) -> None:
        """Сбор задач из Json файла"""
        if os.path.exists(self.filename):
            with open(self.filename, "r", encoding="utf-8") as file:
                data = json.load(file)
                self.tasks = [Task.from_dict(task) for task in data]
                return
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([], file)

    def list_tasks(self):
        data = [
            [
                "ID",
                "Задача",
                "Описание",
                "Категория",
                "Срок выполнения",
                "Приоритет",
                "Статус",
            ]
        ]
        if len(self.tasks) > 0:
            for task in self.tasks:
                data.append(
                    [
                        task.task_id,
                        task.title,
                        task.description,
                        task.category,
                        task.due_date,
                        task.priority,
                        task.status,
                    ]
                )
            pretty_print(data)
        else:
            print([])

    def save_tasks(self) -> None:
        """Сохранение задач в Json файл"""
        with open(self.filename, "w", encoding="utf-8") as file:
            json.dump([task.to_dict() for task in self.tasks], file, indent=4)

    def add_task(
        self,
        title: str,
        description: str | None,
        category: str | None,
        due_date: str | None,
        priority: str | None,
        status: str | None,
    ):
        """Добавление задачи в список задачи класса TaskManager, с последующим сохранением в Json файл

        Args:
            title (str): Название
            description (str | None): Описание
            category (str | None): Категория
            due_date (str | None): Дедлайн
            priority (str | None): Приоритет
            status (str | None): Статус задачи
        """
        task_id = len(self.tasks) + 1
        task = Task(
            task_id=task_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            category=category,
            due_date=datetime.fromisoformat(due_date)
            if due_date
            else datetime.now() + timedelta(days=1),
        )
        self.tasks.append(task)
        self.save_tasks()
        print(f'Задача "{task.title}" успешно создана')

    def delete_task(self, task_id):
        for i, task in enumerate(self.tasks):
            if task.task_id == task_id:
                print(f"Задача {task.title} удалена")
                del self.tasks[i]
                self.save_tasks()
                return
        print(f"Задача с ID {task_id} не найдена")

    def get_task_by_id(self, task_id):
        data = [
            [
                "ID",
                "Задача",
                "Описание",
                "Категория",
                "Срок выполнения",
                "Приоритет",
                "Статус",
            ]
        ]
        for task in self.tasks:
            if task.task_id == task_id:
                data.append(
                    [
                        task.task_id,
                        task.title,
                        task.description,
                        task.category,
                        task.due_date,
                        task.priority,
                        task.status,
                    ]
                )
                pretty_print(data)
                return
        print(f"Задача с ID{task_id} не найдена.")

    def get_tasks_by_category(self, category):
        data = [
            [
                "ID",
                "Задача",
                "Описание",
                "Категория",
                "Срок выполнения",
                "Приоритет",
                "Статус",
            ]
        ]
        for task in self.tasks:
            if task.category == category.lower():
                data.append(
                    [
                        task.task_id,
                        task.title,
                        task.description,
                        task.category,
                        task.due_date,
                        task.priority,
                        task.status,
                    ]
                )
        if len(data) == 0:
            print("Ничего не найдено.")
            return
        pretty_print(data)

    def complete_task_by_id(self, task_id):
        data = [
            [
                "ID",
                "Задача",
                "Описание",
                "Категория",
                "Срок выполнения",
                "Приоритет",
                "Статус",
            ]
        ]

        for task in self.tasks:
            if task.task_id == task_id:
                if task.status == "не выполнено":
                    task.status = "выполнено"
                    self.save_tasks()
                    data.append(
                        [
                            task.task_id,
                            task.title,
                            task.description,
                            task.category,
                            task.due_date,
                            task.priority,
                            task.status,
                        ]
                    )
                    pretty_print(data)
                    return
                print("Задача уже выполнена.")
                return
        if len(data) == 1:
            print(f"Задача с ID {task_id} не найдена.")
