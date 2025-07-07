# CSV-Handler

Обработчик CSV-файлов с фильтрацией и агрегацией данных

## Зависимости
```bash
pip install -r requirements.txt
```

## Использование
```bash
python main.py --file <filename.csv> [--where "колонка<оператор>значение"] [--aggregate "колонка=функция"]
```

## Примеры
### Показать все данные
```bash
python main.py --file products.csv
```

### Фильтр: рейтинг > 4.7
```bash
python main.py --file products.csv --where "rating>4.7"
```

### Агрегация: средняя цена
```bash
python main.py --file products.csv --aggregate "price=avg"
```

### Комбинированный запрос
```bash
python main.py --file products.csv --where "brand=xiaomi" --aggregate "rating=min"
```
