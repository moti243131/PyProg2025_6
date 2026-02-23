"""
Модуль сравнения рекурсивной и итеративной реализации построения бинарного дерева.

Содержит функции build_tree_recursive и build_tree_iterative для построения
дерева с заданными root, height и формулами ветвления (left=root+1, right=root-1).
Поддерживает форматы dict и list. Включает бенчмарк через timeit и построение
графика зависимости времени от высоты дерева.

Пример использования:
    data = {"root": 13, "height": 3}
    tree_rec = build_tree_recursive(data)
    tree_iter = build_tree_iterative(data)
"""

import timeit
from pathlib import Path
from typing import Any, Callable, TypedDict

DEFAULT_ROOT = 13
DEFAULT_HEIGHT = 3


class TreeData(TypedDict, total=False):
    """Параметры для построения бинарного дерева."""

    root: int
    height: int
    left_branch: Callable[[int], int]
    right_branch: Callable[[int], int]
    structure: str


def _parse_data(data: TreeData) -> tuple[int, int, Callable[[int], int], Callable[[int], int], str]:
    """Извлекает параметры из data с подстановкой значений по умолчанию."""
    root = data.get("root", DEFAULT_ROOT)
    height = data.get("height", DEFAULT_HEIGHT)
    left_branch = data.get("left_branch", lambda r: r + 1)
    right_branch = data.get("right_branch", lambda r: r - 1)
    structure = data.get("structure", "dict")
    return root, height, left_branch, right_branch, structure


def _build_recursive_dict(
    val: int,
    height: int,
    left_fn: Callable[[int], int],
    right_fn: Callable[[int], int],
) -> dict[str, Any]:
    """Строит дерево рекурсивно. height=0 — лист без потомков."""
    if height == 0:
        return {str(val): []}
    left_tree = _build_recursive_dict(left_fn(val), height - 1, left_fn, right_fn)
    right_tree = _build_recursive_dict(right_fn(val), height - 1, left_fn, right_fn)
    return {str(val): [left_tree, right_tree]}


def _build_recursive_list(
    val: int,
    height: int,
    left_fn: Callable[[int], int],
    right_fn: Callable[[int], int],
) -> list[Any]:
    """Строит дерево рекурсивно в формате [root, left, right]."""
    if height == 0:
        return [val, [], []]
    left_tree = _build_recursive_list(left_fn(val), height - 1, left_fn, right_fn)
    right_tree = _build_recursive_list(right_fn(val), height - 1, left_fn, right_fn)
    return [val, left_tree, right_tree]


def build_tree_recursive(data: TreeData) -> dict[str, Any] | list[Any]:
    """
    Строит бинарное дерево рекурсивным способом.

    Дерево строится рекурсивными вызовами для левого и правого поддерева.
    root=13, height=3, left=root+1, right=root-1.

    Args:
        data: Словарь с ключами root, height, left_branch, right_branch, structure.

    Returns:
        Дерево в формате dict или list.
    """
    root, height, left_fn, right_fn, structure = _parse_data(data)
    if structure == "dict":
        return _build_recursive_dict(root, height, left_fn, right_fn)
    if structure == "list":
        return _build_recursive_list(root, height, left_fn, right_fn)
    raise ValueError(f"structure должен быть 'dict' или 'list', получено: {structure}")


def _build_iterative_dict_stack(
    root: int,
    height: int,
    left_fn: Callable[[int], int],
    right_fn: Callable[[int], int],
) -> dict[str, Any]:
    """
    Итеративное построение через стек: симуляция рекурсии.

    Стек задач: ("combine", val) — объединить последние 2 результата;
    (val, h) — построить узел. При h=0 — лист; иначе кладём детей в стек.
    """
    if height < 0:
        return {}
    stack: list[tuple[int | str, int | str]] = []
    results: list[dict[str, Any]] = []
    stack.append((root, height))
    while stack:
        a, b = stack.pop()
        if a == "combine":
            val = b
            right_tree = results.pop()
            left_tree = results.pop()
            results.append({str(val): [left_tree, right_tree]})
            continue
        val, h = int(a), int(b)
        if h == 0:
            results.append({str(val): []})
            continue
        stack.append(("combine", val))
        stack.append((right_fn(val), h - 1))
        stack.append((left_fn(val), h - 1))
    return results[0] if results else {}


def _build_iterative_list_stack(
    root: int,
    height: int,
    left_fn: Callable[[int], int],
    right_fn: Callable[[int], int],
) -> list[Any]:
    """Итеративное построение в формате list через стек (симуляция рекурсии)."""
    if height < 0:
        return []
    stack: list[tuple[int | str, int | str]] = []
    results: list[list[Any]] = []
    stack.append((root, height))
    while stack:
        a, b = stack.pop()
        if a == "combine":
            val = b
            right_tree = results.pop()
            left_tree = results.pop()
            results.append([val, left_tree, right_tree])
            continue
        val, h = int(a), int(b)
        if h == 0:
            results.append([val, [], []])
            continue
        stack.append(("combine", val))
        stack.append((right_fn(val), h - 1))
        stack.append((left_fn(val), h - 1))
    return results[0] if results else []


def build_tree_iterative(data: TreeData) -> dict[str, Any] | list[Any]:
    """
    Строит бинарное дерево итеративно (цикл + стек).

    Использует явный стек для симуляции рекурсии. Нет риска RecursionError.

    Args:
        data: Словарь с ключами root, height, left_branch, right_branch, structure.

    Returns:
        Дерево в формате dict или list.
    """
    root, height, left_fn, right_fn, structure = _parse_data(data)
    if structure == "dict":
        return _build_iterative_dict_stack(root, height, left_fn, right_fn)
    if structure == "list":
        return _build_iterative_list_stack(root, height, left_fn, right_fn)
    raise ValueError(f"structure должен быть 'dict' или 'list', получено: {structure}")


def run_benchmark(
    heights: list[int],
    root: int = DEFAULT_ROOT,
    structure: str = "dict",
    number: int = 100,
) -> tuple[list[float], list[float]]:
    """Измеряет время построения дерева для каждой высоты через timeit."""
    times_rec: list[float] = []
    times_iter: list[float] = []
    g = globals()
    for h in heights:
        data: TreeData = {"root": root, "height": h, "structure": structure}
        g["_bench_data"] = data
        t_rec = timeit.timeit(
            "build_tree_recursive(_bench_data)",
            globals=g,
            number=number,
        )
        t_iter = timeit.timeit(
            "build_tree_iterative(_bench_data)",
            globals=g,
            number=number,
        )
        times_rec.append(t_rec)
        times_iter.append(t_iter)
    return times_rec, times_iter


def plot_comparison(
    heights: list[int],
    times_recursive: list[float],
    times_iterative: list[float],
    output_path: str | Path | None = None,
) -> None:
    """Строит график: X — высота, Y — время (сек)."""
    import matplotlib.pyplot as plt

    path = Path(output_path) if output_path else Path(__file__).parent / "comparison_plot.png"
    plt.figure(figsize=(10, 6))
    plt.plot(heights, times_recursive, "o-", label="Рекурсивная", markersize=6)
    plt.plot(heights, times_iterative, "s-", label="Итеративная", markersize=6)
    plt.xlabel("Высота дерева")
    plt.ylabel("Время построения (сек)")
    plt.title("Сравнение рекурсивной и итеративной реализации бинарного дерева")
    plt.legend()
    plt.grid(True, alpha=0.3)
    plt.tight_layout()
    plt.savefig(path, dpi=150)
    plt.close()
    print(f"График сохранён: {path}")


def main() -> None:
    """Демонстрация: построение дерева, бенчмарк, график, выводы."""
    print("Lab6: Сравнение рекурсивной и итеративной реализации\n")

    data: TreeData = {"root": 13, "height": 3}
    print("Дерево (root=13, height=3):")
    rec = build_tree_recursive(data)
    it = build_tree_iterative(data)
    s = str(rec)
    print("Рекурсивная:", s[:150] + "..." if len(s) > 150 else s)
    s = str(it)
    print("Итеративная:", s[:150] + "..." if len(s) > 150 else s)

    heights = list(range(1, 11))
    print(f"\nБенчмарк для высот {heights}...")
    times_rec, times_iter = run_benchmark(heights, root=13, structure="dict")

    print("\nРезультаты (сек):")
    print("Height | Recursive | Iterative")
    print("-" * 35)
    for h, tr, ti in zip(heights, times_rec, times_iter):
        print(f"  {h:2d}   | {tr:.6f} | {ti:.6f}")

    plot_comparison(heights, times_rec, times_iter)

    print("\nВыводы")
    print("1. Рекурсивная: проще читать, но при больших height — RecursionError.")
    print("2. Итеративная (стек): нет переполнения стека вызовов.")
    print("3. Обе O(n) по узлам; разница во времени — константные факторы.")


if __name__ == "__main__":
    main()
