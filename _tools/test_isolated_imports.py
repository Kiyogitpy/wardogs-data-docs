"""Static check: a _tools script (has a __main__ guard) that imports a sibling _tools module must put its own folder on sys.path first, so `python -I` works. Run: python -I -W ignore -m unittest discover -s _tools -p test_isolated_imports.py -v"""
import ast
from pathlib import Path
import unittest

TOOLS = Path(__file__).resolve().parent
SIBLINGS = {p.stem for p in TOOLS.glob("*.py")}


def is_script(tree):
    return any(isinstance(node, ast.If) and ast.unparse(node.test) == "__name__ == '__main__'"
               for node in tree.body)


def sibling_import_lines(tree):
    lines = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            names = [a.name.split(".")[0] for a in node.names]
        elif isinstance(node, ast.ImportFrom) and node.level == 0 and node.module:
            names = [node.module.split(".")[0]]
        else:
            continue
        if any(n in SIBLINGS for n in names):
            lines.append(node.lineno)
    return lines


def own_folder_insert_lines(tree):
    assigns = {t.id: node.value for node in tree.body if isinstance(node, ast.Assign)
               for t in node.targets if isinstance(t, ast.Name)}
    lines = []
    for node in ast.walk(tree):
        if not (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute)
                and node.func.attr == "insert" and ast.unparse(node.func.value) == "sys.path"
                and len(node.args) == 2 and isinstance(node.args[0], ast.Constant)
                and node.args[0].value == 0):
            continue
        arg = node.args[1]
        if isinstance(arg, ast.Name) and arg.id in assigns:
            arg = assigns[arg.id]
        if "__file__" in ast.unparse(arg):
            lines.append(node.lineno)
    return lines


class IsolatedImports(unittest.TestCase):
    def test_sibling_imports_follow_own_folder_on_sys_path(self):
        checked = []
        problems = []
        for path in sorted(TOOLS.glob("*.py")):
            tree = ast.parse(path.read_text(encoding="utf-8"), filename=str(path))
            imports = sibling_import_lines(tree)
            if not imports or not is_script(tree):
                continue
            checked.append(path.name)
            inserts = own_folder_insert_lines(tree)
            if not inserts or min(inserts) > min(imports):
                problems.append(f"{path.name}: first sibling import at line {min(imports)}, "
                                f"own-folder sys.path.insert at {min(inserts) if inserts else 'none'}")
        self.assertTrue(checked, "no sibling imports found; the scan is broken")
        self.assertEqual(problems, [])


if __name__ == "__main__":
    unittest.main()
