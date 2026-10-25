from pathlib import Path
import ast
import nbformat

root = Path(__file__).resolve().parents[1] / "notebooks"
failed = []
for path in sorted(root.glob("*.ipynb")):
    nb = nbformat.read(path, as_version=4)
    for idx, cell in enumerate(nb.cells):
        if cell.cell_type != "code":
            continue
        src = "\n".join(
            line for line in cell.source.splitlines()
            if not line.lstrip().startswith(("%", "!"))
        )
        try:
            ast.parse(src)
        except SyntaxError as exc:
            failed.append((path.name, idx, str(exc)))
if failed:
    for item in failed:
        print("FAIL", item)
    raise SystemExit(1)
print("Notebook static syntax check passed.")
