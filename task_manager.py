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
        data = [
            ['ID', 'Задача', 'Описание',  'Категория',  'Срок выполнения', 'Приоритет', 'Статус']
        ]
        if len(self.tasks) > 0:
            for task in self.tasks:
                data.append([task.task_id,task.title,task.description,task.category,task.due_date,task.priority,task.status])
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
                print(f'Задача {task.title} удалена')
                del self.tasks[i]
                self.save_tasks()
                return
        print(f'Задача с ID {task_id} не найдена')
        
    def get_task_by_id(self, task_id):
        data = [
            ['ID', 'Задача', 'Описание',  'Категория',  'Срок выполнения', 'Приоритет', 'Статус']
        ]
        for task in self.tasks:
            if task.task_id == task_id:

                data.append([task.task_id,task.title,task.description,task.category,task.due_date,task.priority,task.status])
                pretty_print(data)
                return
        print(f'Задача с ID{task_id} не найдена.')
    
    def get_tasks_by_category(self, category):
        data = [
            ['ID', 'Задача', 'Описание',  'Категория',  'Срок выполнения', 'Приоритет', 'Статус']
        ]
        for task in self.tasks:
            if task.category == category.lower():
                data.append([task.task_id,task.title,task.description,task.category,task.due_date,task.priority,task.status])
        if len(data) == 0:
            print('Ничего не найдено.')
            return
        pretty_print(data)
        
        
                
        
def pretty_print(data):
    longest_cols = [
        (max([len(str(row[i])) for row in data]) + 3)
        for i in range(len(data[0]))
    ]
    row_format = "".join(["{:>" + str(longest_col) + "}" for longest_col in longest_cols])
    for row in data:
        print(row_format.format(*row))

                    

def main(command_line=None):
    parser = argparse.ArgumentParser(
        prog="Список задач", description="Управление вашим списком задач"
    )
    parser.add_argument("--debug", action="store_true", help="Print debug info")
    subparser = parser.add_subparsers(dest="command")

    # Вывод данных
    list_parser = subparser.add_parser("list", help="Вывод всех задач")
    list_parser.add_argument('-id', type=int, help='Вывод по айдишнику', default=None)
    list_parser.add_argument('--category','-c', type=str, help='Вывод по категориям', default=None)

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
        if args.id:
            # manager.get_task_by_id(args.id)
            manager.get_task_by_id(args.id)
        elif args.category:
            manager.get_tasks_by_category(args.category)
        else:
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
