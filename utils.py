from task import Task
from datetime import datetime

def pretty_print(data):
    """Вывод информации в виде таблицы

    Args:
        data (_type_): Список, в котором включены данные для вывода
    """
    longest_cols = [
        (max([len(str(row[i])) for row in data]) + 3) for i in range(len(data[0]))
    ]
    row_format = "".join(
        ["{:>" + str(longest_col) + "}" for longest_col in longest_cols]
    )
    for row in data:
        print(row_format.format(*row))


def answer_user_edit_info(task: Task, user_choice: int):
    if user_choice == 1:  # Название
        task.title = input("Введите новое название: ")
        return task
        
    elif user_choice == 2:  # Описание
        task.description = input("Введите новое описание: ")
        return task
        
    elif user_choice == 3:  # Дедлайн
        due_date = input("Введите новый дедлайн год-месяц-день: ")
        
        try:
            if bool(datetime.strptime(due_date, '%Y-%m-%d')):
                task.due_date = due_date
        except ValueError:
                print('Дата должна быть в формате год-месяц-день.')
                return
            
        return task
    
    elif user_choice == 4:  # Категория
        task.category = input("Введите новую категорию: ")
        return task
    
    elif user_choice == 5:  # Приоритет
        priority = input("Введите новый приоритет (низкий,средний,выскоий): ")
        if priority.lower() not in ["низкий", "средний", "высокий"]:
            print("Сказано же - низкий, средний, высокий.")
            return
        task.priority = priority
        return task

    elif user_choice == 6:  # Статус
        status = input("Введите новый статус (не выполнено/выполнено)")
        if status.lower() not in ["не выполнено", "выполнено"]:
            print("Статус задачи может быть только: не выполнено/выполнено")
            return 
        task.status = status
        return task 

    elif user_choice == 7:  # Вся
        title = input("Введите новое название: ")
        description = input("Введите новое описание: ")
        due_date = input("Введите новый дедлайн год-месяц-день: ")
        
        try:
            if not bool(datetime.strptime(due_date, '%Y-%m-%d')):
                print('Дата должна быть в формате год-месяц-день.')
                return
        except ValueError:
            print('Дата должна быть в формате год-месяц-день.')
            return
        
        category = input("Введите новую категорию: ")
        priority = input("Введите новый приоритет (низкий,средний,выскоий): ")

        if priority.lower() not in ["низкий", "средний", "высокий"]:
            print("Сказано же - низкий, средний, высокий.")
            return

        status = input("Введите новый статус (не выполнено/выполнено): ")

        if status.lower() not in ["не выполнено", "выполнено"]:
            print("Статус задачи может быть только: не выполнено/выполнено")
            return
        task.title, task.description, task.due_date, task.category, task.priority, task.status = title, description, due_date, category, priority, status
        return task
    
    elif user_choice == 8:
        print("Отмена действия.")
        return

    print("Не найдено действий.")
