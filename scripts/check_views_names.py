import ast
import builtins
import os
import sys

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
views_dir = os.path.join(WORKSPACE_ROOT, "views")

builtin_names = set(dir(builtins))

def check_undefined_names_in_file(filepath):
    with open(filepath, "r", encoding="utf-8") as f:
        code = f.read()
    try:
        tree = ast.parse(code, filename=filepath)
    except Exception as e:
        return [f"SyntaxError: {e}"]

    # Module-level defined names
    mod_defined = set(builtin_names)
    for node in tree.body:
        if isinstance(node, (ast.Import, ast.ImportFrom)):
            for a in node.names:
                mod_defined.add(a.asname or a.name)
        elif isinstance(node, ast.Assign):
            for t in node.targets:
                for n in ast.walk(t):
                    if isinstance(n, ast.Name):
                        mod_defined.add(n.id)
        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            mod_defined.add(node.name)

    issues = []
    # Check each function
    for func in ast.walk(tree):
        if isinstance(func, (ast.FunctionDef, ast.AsyncFunctionDef)):
            func_defined = set(mod_defined)
            # Add parameters
            for a in func.args.args + func.args.posonlyargs + func.args.kwonlyargs:
                func_defined.add(a.arg)
            if func.args.vararg:
                func_defined.add(func.args.vararg.arg)
            if func.args.kwarg:
                func_defined.add(func.args.kwarg.arg)

            # Add all assignments, stores, imports within the function
            for child in ast.walk(func):
                if isinstance(child, (ast.Import, ast.ImportFrom)):
                    for a in child.names:
                        func_defined.add(a.asname or a.name)
                elif isinstance(child, ast.Assign):
                    for t in child.targets:
                        for n in ast.walk(t):
                            if isinstance(n, ast.Name):
                                func_defined.add(n.id)
                elif isinstance(child, (ast.AnnAssign, ast.AugAssign)):
                    t = getattr(child, 'target', None)
                    if isinstance(t, ast.Name):
                        func_defined.add(t.id)
                elif isinstance(child, (ast.For, ast.With, ast.ExceptHandler)):
                    for n in ast.walk(child):
                        if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                            func_defined.add(n.id)
                elif isinstance(child, (ast.ListComp, ast.SetComp, ast.DictComp, ast.GeneratorExp)):
                    for gen in child.generators:
                        for n in ast.walk(gen.target):
                            if isinstance(n, ast.Name) and isinstance(n.ctx, ast.Store):
                                func_defined.add(n.id)

            # Now check all Name loads
            for child in ast.walk(func):
                if isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                    if child.id not in func_defined:
                        # Exclude common streamlit/dynamic patterns if any
                        issues.append((func.name, child.lineno, child.id))

    return issues

for f in sorted(os.listdir(views_dir)):
    if f.endswith(".py"):
        fp = os.path.join(views_dir, f)
        res = check_undefined_names_in_file(fp)
        if res:
            print(f"\n[!] Issues in views/{f}:")
            for item in res:
                if isinstance(item, tuple):
                    print(f"    Line {item[1]} in {item[0]}(): undefined '{item[2]}'")
                else:
                    print(f"    {item}")
        else:
            print(f"[+] views/{f}: CLEAN (0 undefined names)")

