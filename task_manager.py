import argparse
import os
import json
from datetime import datetime, timedelta


class Task:
    def __init__(
        self,
        id: int,
        title: str,
        description: str = "",
        status: str = "не выполнено",
        priority: str = "низкий",
        category: str = "личное",
        due_date: datetime = (datetime.now() + timedelta(days=1)),
    ):
        self.id = id
        self.title = title.lower()
        self.description = description.lower()
        self.status = status.lower()
        self.priority = priority.lower()
        self.category = category.lower()
        self.due_date = due_date.strftime("%Y-%m-%d")

    def to_dict(self) -> dict:
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }


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
                self.tasks = [Task.to_dict(task) for task in data]

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
            id=task_id,
            title=title,
            description=description,
            status=status,
            priority=priority,
            category=category,
            due_date=datetime.fromisoformat(due_date) if due_date else None,
        )
        self.tasks.append(task)
        self.save_tasks()


def main(): ...


if __name__ == "__main__":
    main()
