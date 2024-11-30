import argparse
from task_manager import TaskManager
from datetime import datetime


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

    # Завершить задачу
    complete_parser = subparser.add_parser('complete', help='Завершить задачу')
    complete_parser.add_argument('-id', help='Айди задачи, которую нужно завершить', type=int)
    
    # Редактироваение данных 
    edit_parser = subparser.add_parser('edit', help='Изменение задачи')
    edit_parser.add_argument('-id', type=int, help='Айди задачи, которую нужно изменить')
    
    # Удаление задачи
    delete_parser = subparser.add_parser('del', help='Удалить задачу')
    delete_parser.add_argument('-id', type=int, help='Айди задачи, которую нужно удалить ')
    
    manager = TaskManager()

    args = parser.parse_args(command_line)

    if args.debug:
        print("debug" + str(args))

    if args.command == "list":
        if args.id:
            manager.get_task_by_id(args.id)
        elif args.category:
            manager.get_tasks_by_category(args.category)
        else:
            manager.list_tasks()
        
    if args.command == "add":
        try:
            if bool(datetime.strptime(args.deadline, '%Y-%m-%d')):
                
                if args.title:
                    manager.add_task(
                        title=args.title,
                        description=args.description,
                        category=args.category,
                        due_date=args.deadline,
                        priority=args.priority,
                        status=args.status,
                    )
                else:
                    print('Для создания задачи небходимо указать "--title"')
        except ValueError:
            print('Дату необходимо указывать в формате год-месяц-день')
        
        
            
    if args.command == 'edit':
        if args.id:
            manager.edit_task(args.id)
        
    if args.command == 'del':
        if args.id:
            manager.delete_task(args.id)
        
    if args.command == 'complete':
        if args.id:
            manager.complete_task_by_id(args.id)
        else:
            print('Необходимо указать ID задачи, которую нужно завершить.')

if __name__ == "__main__":
    main()
