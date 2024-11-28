import argparse
import os
import json
from datetime import datetime, timedelta


class Task:
    def __init__(
        self,
        task_id: int,
        title: str,
        description: str = "",
        status: str = "не выполнено",
        priority: str = "низкий",
        category: str = "личное",
        due_date: datetime | str = None,
    ):
        self.task_id = task_id
        self.title = title.lower()
        self.description = description.lower()
        self.status = status.lower()
        self.priority = priority.lower()
        self.category = category.lower()
        self.due_date = (
            due_date.strftime("%Y-%m-%d")
            if isinstance(due_date, datetime)
            else due_date
        )

    def to_dict(self) -> dict:
        return {
            "task_id": self.task_id,
            "title": self.title,
            "description": self.description,
            "category": self.category,
            "due_date": self.due_date,
            "priority": self.priority,
            "status": self.status,
        }

    @classmethod
    def from_dict(cls, data):
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )


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
        if len(self.tasks) > 0:
            print("\tСписок задач")
            print(
                """ID Задача \t Описание \t Категория \t Срок выполнения Приоритет \t Статус"""
            )
            for task in self.tasks:
                print(
                    f"{task.task_id}. {task.title}\t{task.description} \t {task.category} \t {task.due_date} \t {task.priority} \t {task.status}"
                )
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


def main(command_line=None):
    parser = argparse.ArgumentParser(
        prog="Список задач", description="Управление вашим списком задач"
    )
    parser.add_argument("--debug", action="store_true", help="Print debug info")
    subparser = parser.add_subparsers(dest="command")

    # Вывод данных
    list_parser = subparser.add_parser("list", help="Вывод всех задач")

    # Ввод данных
    add_parser = subparser.add_parser("add", help="Добавление задачи в список задач")
    add_parser.add_argument(
        "--title", "-t", help="Заголовок задачи. Необходимо заполнить"
    )
    add_parser.add_argument(
        "--description",
        "-d",
        help="Описание задачи. По умолчанию - пустая строка",
        default="",
    )
    add_parser.add_argument(
        "--status",
        "-s",
        help="Статус задачи. По умолчанию - не выполнено",
        choices=["не выполнено", "в процессе", "выполнено"],
        default="не выполнено",
    )
    add_parser.add_argument(
        "--priority",
        "-p",
        help="Приоритет задачи. По умолчанию - низкий",
        choices=["низкий", "средний", "высокий"],
        default="низкий",
    )
    add_parser.add_argument(
        "--category",
        "-c",
        help="Категория задачи. По умолчанию - личное",
        choices=["обучение", "личное", "работа", "дом"],
        default="личное",
    )
    add_parser.add_argument(
        "--deadline",
        "-dl",
        help="Дедлайн задачи. По умолчанию будет значение - сегодня + 1 день",
        default=None,
    )

    manager = TaskManager()

    args = parser.parse_args(command_line)

    if args.debug:
        print("debug" + str(args))

    if args.command == "list":
        manager.list_tasks()
    if args.command == "add":
        manager.add_task(
            title=args.title,
            description=args.description,
            category=args.category,
            due_date=args.deadline,
            priority=args.priority,
            status=args.status,
        )

if __name__ == "__main__":
    main()
