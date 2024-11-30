from datetime import datetime


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
        """Вывод задачи в виде словаря для сохранения в json виде

        Returns:
            dict: Представление задачи в виде словаря
        """
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
        """Создание класса из словаря

        Args:
            data (_type_): Преобразование json информации в класс Task

        Returns:
            Task: Возвращает задачу
        """
        return cls(
            task_id=data["task_id"],
            title=data["title"],
            description=data["description"],
            category=data["category"],
            due_date=data["due_date"],
            priority=data["priority"],
            status=data["status"],
        )
