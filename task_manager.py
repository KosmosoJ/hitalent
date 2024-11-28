import argparse
from datetime import datetime, timedelta


class Task:
    def __init__(
        self,
        id:int,
        title:str,
        description:str="",
        status:str="не выполнено",
        priority:str="низкий",
        category:str="личное",
        due_date:datetime=(datetime.now() + timedelta(days=1)),
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
            'id':self.id,
            'title':self.title,
            'description':self.description,
            'category':self.category,
            'due_date':self.due_date,
            'priority':self.priority,
            'status':self.status
        }
        
def main(): ...


if __name__ == "__main__":
    main()
