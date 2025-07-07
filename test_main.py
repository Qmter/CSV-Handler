import pytest
from main import read_csv_file, apply_filter, apply_aggregation, parse_condition
import os
import csv
from tempfile import NamedTemporaryFile

@pytest.fixture
def sample_csv_data():
    """Фикстура с тестовыми данными в формате списка словарей."""
    return [
        {'name': 'iphone 15 pro', 'brand': 'apple', 'price': '999', 'rating': '4.9'},
        {'name': 'galaxy s23 ultra', 'brand': 'samsung', 'price': '1199', 'rating': '4.8'},
        {'name': 'redmi note 12', 'brand': 'xiaomi', 'price': '199', 'rating': '4.6'},
        {'name': 'poco x5 pro', 'brand': 'xiaomi', 'price': '299', 'rating': '4.4'}
    ]

@pytest.fixture
def sample_csv_file(sample_csv_data):
    """Фикстура, создающая временный CSV файл с тестовыми данными."""
    with NamedTemporaryFile(mode='w', delete=False, suffix='.csv') as f:
        writer = csv.DictWriter(f, fieldnames=['name', 'brand', 'price', 'rating'])
        writer.writeheader()
        writer.writerows(sample_csv_data)
    
    yield f.name 
    os.unlink(f.name)  

def test_read_csv_file(sample_csv_file, sample_csv_data):
    """Тестирование чтения CSV файла."""
    data = read_csv_file(sample_csv_file)
    assert len(data) == 4
    assert data == sample_csv_data

@pytest.mark.parametrize("condition,expected_count", [
    ("brand=apple", 1),
    ("brand=xiaomi", 2),
    ("price>1000", 1),
    ("price<300", 2),
    ("rating>4.7", 2),
    ("rating<=4.6", 2),
    ("name=galaxy s23 ultra", 1),
])
def test_apply_filter(sample_csv_data, condition, expected_count):
    """Тестирование фильтрации с различными условиями."""
    filtered = apply_filter(sample_csv_data, condition)
    assert len(filtered) == expected_count

@pytest.mark.parametrize("aggregation,expected_result", [
    ("rating=avg", {'avg': pytest.approx(4.675, 0.01)}),
    ("rating=min", {'min': 4.4}),
    ("rating=max", {'max': 4.9}),
    ("price=sum", {'sum': 2696.0}),
    ("price=count", {'count': 4}),
])
def test_apply_aggregation(sample_csv_data, aggregation, expected_result):
    """Тестирование агрегационных функций."""
    result = apply_aggregation(sample_csv_data, aggregation)
    assert result == expected_result

@pytest.mark.parametrize("condition,expected", [
    ("price>100", ('price', '>', '100')),
    ("brand=apple", ('brand', '=', 'apple')),
    ("rating<=4.5", ('rating', '<=', '4.5')),
    ("name>=iphone", ('name', '>=', 'iphone')),
])
def test_parse_condition(condition, expected):
    """Тестирование парсинга условий фильтрации."""
    assert parse_condition(condition) == expected

def test_apply_filter_empty_result(sample_csv_data):
    """Тестирование пустого результата фильтрации."""
    filtered = apply_filter(sample_csv_data, "brand=nokia")
    assert len(filtered) == 0

def test_apply_aggregation_non_numeric(sample_csv_data):
    """Тестирование агрегации по нечисловой колонке."""
    with pytest.raises(ValueError, match="содержит нечисловые значения"):
        apply_aggregation(sample_csv_data, "brand=avg")

def test_parse_condition_invalid_format():
    """Тестирование обработки некорректных условий."""
    with pytest.raises(ValueError, match="Некорректное условие фильтрации"):
        parse_condition("invalid_condition")