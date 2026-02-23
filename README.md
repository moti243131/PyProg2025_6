# Lab6: Сравнение рекурсивной и итеративной реализации бинарного дерева

Глушков Матвей группа P3120

## Назначение

Модуль сравнивает время работы двух реализаций построения бинарного дерева:

- **Рекурсивная** — дерево строится рекурсивными вызовами для левого и правого поддерева
- **Итеративная** — дерево строится через цикл и явную структуру данных (буфер уровней)

Результаты измеряются через `timeit`, визуализируются на графике и сопровождаются выводами.

## Установка

```bash
pip install -r requirements.txt
```

## Запуск

```bash
python binary_tree_comparison.py
```

Программа выведет дерево, таблицу времени для высот 1–10, сохранит график `comparison_plot.png` и выведет выводы.

## Тесты

```bash
python -m unittest test_binary_tree_comparison -v
```

## Структура проекта

| Файл | Назначение |
|------|------------|
| `binary_tree_comparison.py` | Основной модуль: функции построения, бенчмарк, график |
| `test_binary_tree_comparison.py` | Модульные тесты |
| `requirements.txt` | Зависимости (matplotlib) |
| `tz.txt` | Техническое задание |
| `comparison_plot.png` | График (создаётся при запуске) |

## Описание функций

### `build_tree_recursive(data: TreeData) -> dict | list`

Строит бинарное дерево рекурсивным способом.

- **Базовый случай:** `height=0` → лист без потомков
- **Рекурсия:** для каждого узла строит левое и правое поддеревья

### `build_tree_iterative(data: TreeData) -> dict | list`

Строит бинарное дерево итеративно через **стек** (явная структура данных):

1. Стек задач: `(val, height)` — построить узел; `("combine", val)` — объединить последние 2 результата
2. При height=0 — лист; иначе кладём детей в стек, затем объединяем результаты

Не использует рекурсию — нет риска переполнения стека.

### `run_benchmark(heights, root, structure, number) -> tuple[list[float], list[float]]`

Измеряет время построения дерева для каждой высоты через `timeit`.

- **heights** — список высот (ось X графика)
- **root** — значение корня (по умолчанию 13)
- **structure** — `"dict"` или `"list"`
- **number** — количество повторений timeit (по умолчанию 100)

Возвращает `(times_recursive, times_iterative)`.

### `plot_comparison(heights, times_recursive, times_iterative, output_path?) -> None`

Строит график сравнения времени построения.

- **heights** — высоты дерева (ось X)
- **times_recursive**, **times_iterative** — время в секундах (ось Y)
- **output_path** — путь для сохранения (по умолчанию `comparison_plot.png`)

## Структура данных `data`

Словарь с ключами:

| Ключ | Тип | По умолчанию | Описание |
|------|-----|--------------|----------|
| `root` | int | 13 | Значение в корне |
| `height` | int | 3 | Высота дерева |
| `left_branch` | Callable | `lambda r: r+1` | Функция левого потомка |
| `right_branch` | Callable | `lambda r: r-1` | Функция правого потомка |
| `structure` | str | `"dict"` | Формат вывода: `"dict"` или `"list"` |

## Форматы вывода

**Dict** (по умолчанию):
```python
{"13": [{"14": [{"15": []}, {"13": []}]}, {"12": [{"13": []}, {"11": []}]}]}
```

**List** — `[root, left_subtree, right_subtree]`:
```python
[13, [14, [15, [], []], [13, [], []]], [12, [13, [], []], [11, [], []]]]
```

## Примеры использования

```python
from binary_tree_comparison import build_tree_recursive, build_tree_iterative

# Параметры по умолчанию (root=13, height=3)
data = {"root": 13, "height": 3}
tree_rec = build_tree_recursive(data)
tree_iter = build_tree_iterative(data)

# Формат list
data_list = {"root": 13, "height": 2, "structure": "list"}
tree = build_tree_iterative(data_list)  # [13, [14, [], []], [12, [], []]]

# Кастомные формулы ветвления
data_custom = {
    "root": 5,
    "height": 2,
    "left_branch": lambda r: r + 1,
    "right_branch": lambda r: r**2,
}
tree = build_tree_recursive(data_custom)
```

## Результат работы

- **Консоль:** дерево, таблица времени, выводы
- **Файл:** `comparison_plot.png` — график зависимости времени от высоты

## Выводы

1. **Рекурсивная версия** — проще читать, но при больших `height` возможен `RecursionError` (лимит ~1000 в Python).
2. **Итеративная версия** — не использует стек вызовов, нет риска переполнения.
3. На малых высотах разница во времени незначительна; на больших итеративная может быть стабильнее.
