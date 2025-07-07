import argparse
import csv
from tabulate import tabulate
from typing import List, Dict, Union, Optional

def read_csv_file(file_path: str) -> List[Dict[str, str]]:
    """Чтение CSV файла с автоматическим определением заголовков"""
    with open(file_path, mode='r', encoding='utf-8') as file:
        return list(csv.DictReader(file))

def parse_condition(condition: str) -> tuple[str, str, str]:
    """Парсинг условий фильтрации с поддержкой операторов >, <, =, >=, <="""
    operators = ['>=', '<=', '>', '<', '=']
    for op in operators:
        if op in condition:
            parts = condition.split(op, 1)
            if len(parts) == 2:
                return parts[0], op, parts[1]
    raise ValueError(f"Некорректное условие. Используйте: {', '.join(operators)}")

def apply_filter(data: List[Dict[str, str]], condition: str) -> List[Dict[str, str]]:
    """Фильтрация данных с поддержкой числовых и строковых сравнений"""
    if not condition:
        return data
    
    try:
        column, operator, value = parse_condition(condition)
    except ValueError as e:
        raise ValueError(f"Ошибка в условии фильтрации: {e}")

    ops = {
        '>': lambda a, b: a > b,
        '<': lambda a, b: a < b,
        '=': lambda a, b: a == b,
        '>=': lambda a, b: a >= b,
        '<=': lambda a, b: a <= b
    }

    filtered = []
    for row in data:
        try:
            row_val = float(row[column])
            filter_val = float(value)
            if ops[operator](row_val, filter_val):
                filtered.append(row)
        except ValueError:
            if ops[operator](row[column], value):
                filtered.append(row)
    
    return filtered

def apply_aggregation(data: List[Dict[str, str]], aggregation: str) -> Dict[str, Union[float, int]]:
    """Агрегация данных с поддержкой count для любых колонок"""
    if not data:
        return {'Ошибка!': 'Нет данных для агрегации'}
    
    try:
        column, func = aggregation.split('=', 1)
    except ValueError:
        raise ValueError("Формат агрегации: 'колонка=функция'")

    if func == 'count':
        return {'count': len(data)}

    try:
        values = [float(row[column]) for row in data]
    except (ValueError, KeyError):
        raise ValueError(f"Колонка '{column}' не существует или содержит нечисловые значения")

    aggregations = {
        'avg': lambda x: round(sum(x)/len(x), 2),
        'min': min,
        'max': max,
        'sum': sum
    }

    if func not in aggregations:
        raise ValueError(f"Недопустимая функция. Доступно: {', '.join(aggregations.keys())}, count")
    
    return {func: aggregations[func](values)}

def display_results(data: Union[List[Dict], Dict]):
    """Форматированный вывод результатов"""
    if isinstance(data, list):
        if not data:
            print("Нет данных, соответствующих условиям")
            return
        print(tabulate(data, headers="keys", tablefmt="grid"))
    elif isinstance(data, dict):
        print(tabulate([data], headers="keys", tablefmt="grid"))

def main():
    parser = argparse.ArgumentParser(description="Обработчик CSV с фильтрацией и агрегацией")
    parser.add_argument('--file', required=True, help="Путь к CSV файлу")
    parser.add_argument('--where', default='', help="Условие фильтрации (колонка>значение)")
    parser.add_argument('--aggregate', default='', help="Агрегация (колонка=функция)")
    
    args = parser.parse_args()

    try:
        data = read_csv_file(args.file)
        
        if args.where:
            data = apply_filter(data, args.where)
        
        result = apply_aggregation(data, args.aggregate) if args.aggregate else data
        display_results(result)

    except Exception as e:
        print(f"Ошибка: {e}")

if __name__ == '__main__':
    main()