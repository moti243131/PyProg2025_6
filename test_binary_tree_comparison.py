import unittest

from binary_tree_comparison import (
    build_tree_iterative,
    build_tree_recursive,
)


class TestBuildTreeRecursive(unittest.TestCase):
    """Тесты функции build_tree_recursive."""

    def test_default_params(self) -> None:
        """Проверка с параметрами по умолчанию (root=13, height=3)."""
        data = {"root": 13, "height": 3}
        tree = build_tree_recursive(data)
        self.assertIn("13", tree)
        children = tree["13"]
        self.assertEqual(len(children), 2)
        self.assertIn("14", children[0])
        self.assertIn("12", children[1])

    def test_height_zero(self) -> None:
        """При height=0 возвращается только корень без потомков."""
        data = {"root": 13, "height": 0}
        tree = build_tree_recursive(data)
        self.assertEqual(tree, {"13": []})

    def test_height_one(self) -> None:
        """При height=1 — корень с двумя листьями."""
        data = {"root": 13, "height": 1}
        tree = build_tree_recursive(data)
        self.assertEqual(tree, {"13": [{"14": []}, {"12": []}]})

    def test_list_structure(self) -> None:
        """Проверка формата list."""
        data = {"root": 13, "height": 1, "structure": "list"}
        tree = build_tree_recursive(data)
        self.assertEqual(tree, [13, [14, [], []], [12, [], []]])

    def test_invalid_structure_raises(self) -> None:
        """Неизвестный structure вызывает ValueError."""
        with self.assertRaises(ValueError):
            build_tree_recursive({"root": 13, "height": 1, "structure": "invalid"})


class TestBuildTreeIterative(unittest.TestCase):
    """Тесты функции build_tree_iterative."""

    def test_default_params(self) -> None:
        """Проверка с параметрами по умолчанию."""
        data = {"root": 13, "height": 3}
        tree = build_tree_iterative(data)
        self.assertIn("13", tree)
        children = tree["13"]
        self.assertEqual(len(children), 2)
        self.assertIn("14", children[0])
        self.assertIn("12", children[1])

    def test_height_zero(self) -> None:
        """При height=0 возвращается только корень."""
        data = {"root": 13, "height": 0}
        tree = build_tree_iterative(data)
        self.assertEqual(tree, {"13": []})

    def test_height_one(self) -> None:
        """При height=1 — корень с двумя листьями."""
        data = {"root": 13, "height": 1}
        tree = build_tree_iterative(data)
        self.assertEqual(tree, {"13": [{"14": []}, {"12": []}]})

    def test_list_structure(self) -> None:
        """Проверка формата list."""
        data = {"root": 13, "height": 1, "structure": "list"}
        tree = build_tree_iterative(data)
        self.assertEqual(tree, [13, [14, [], []], [12, [], []]])


if __name__ == "__main__":
    unittest.main()
