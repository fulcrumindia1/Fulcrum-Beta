import ast
import builtins
import os
import sys

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
views_dir = os.path.join(WORKSPACE_ROOT, "views")

builtin_names = set(dir(builtins))

class ScopeVisitor(ast.NodeVisitor):
    def __init__(self, parent_scope=None):
        self.parent = parent_scope
        self.defined = set()
        self.used = [] # (name, lineno)

    def is_defined(self, name):
        if name in self.defined or name in builtin_names:
            return True
        if self.parent:
            return self.parent.is_defined(name)
        return False

def check_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    try:
        tree = ast.parse(code, filename=filepath)
    except Exception as e:
        return [f"SyntaxError: {e}"]

    # We can use pyflakes or custom scope resolver
    import subprocess
    cmd = [sys.executable, "-m", "pyflakes", filepath]
    res = subprocess.run(cmd, capture_output=True, text=True)
    lines = [line.strip() for line in res.stdout.splitlines() if "undefined name" in line]
    return lines

for f in sorted(os.listdir(views_dir)):
    if f.endswith(".py"):
        fp = os.path.join(views_dir, f)
        issues = check_file(fp)
        if issues:
            print(f"\n[!] Issues in views/{f}:")
            for iss in issues:
                print(f"    {iss}")
        else:
            print(f"[+] views/{f}: CLEAN")

