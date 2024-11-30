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
