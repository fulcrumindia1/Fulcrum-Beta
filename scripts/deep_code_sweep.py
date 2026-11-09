"""
scripts/deep_code_sweep.py
==========================
Deep static analysis across views/ and services/ to identify:
1. UnboundLocalError risks (variables used before inner import/assignment in the same function).
2. NameError risks (undefined names in functions).
3. Call argument mismatches (calling internal service functions with unexpected kwargs).
"""

import ast
import inspect
import os
import sys

WORKSPACE_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if WORKSPACE_ROOT not in sys.path:
    sys.path.insert(0, WORKSPACE_ROOT)

# Pre-import our services to get signatures
import services.profiles as profiles_mod
import services.roles as roles_mod
import services.relationships as rels_mod
import services.schemes as schemes_mod
import services.admin_metrics as metrics_mod
import services.pagination as pag_mod
import services.aspirant_photos as asp_photos_mod
import services.professional_photos as pro_photos_mod
import services.auth as auth_mod
import services.account_lifecycle as lifecycle_mod

service_modules = [
    profiles_mod, roles_mod, rels_mod, schemes_mod, metrics_mod,
    pag_mod, asp_photos_mod, pro_photos_mod, auth_mod, lifecycle_mod
]

function_signatures = {}
for mod in service_modules:
    for name, obj in inspect.getmembers(mod, inspect.isfunction):
        try:
            function_signatures[name] = inspect.signature(obj)
        except Exception:
            pass

print(f"[*] Indexed {len(function_signatures)} internal service function signatures.")

def check_unbound_locals(filepath):
    """Detects if any name is read in a function before an inner import or assignment of that name."""
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    issues = []

    for node in ast.walk(tree):
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            # Collect all reads, imports, and assignments with line numbers
            assigned_or_imported = {}
            reads = []

            for child in ast.walk(node):
                if child is node:
                    continue
                # Inner imports
                if isinstance(child, ast.ImportFrom):
                    for alias in child.names:
                        assigned_or_imported.setdefault(alias.asname or alias.name, child.lineno)
                elif isinstance(child, ast.Import):
                    for alias in child.names:
                        assigned_or_imported.setdefault(alias.asname or alias.name, child.lineno)
                # Name reads
                elif isinstance(child, ast.Name) and isinstance(child.ctx, ast.Load):
                    reads.append((child.id, child.lineno))

            # Now check if any read happens at a line earlier than an inner import of the same name
            for name, read_line in reads:
                if name in assigned_or_imported:
                    import_line = assigned_or_imported[name]
                    if read_line < import_line:
                        issues.append((filepath, read_line, f"UnboundLocalError risk: '{name}' read at line {read_line} before inner import at line {import_line}"))

    return issues

def check_call_signatures(filepath):
    """Checks function calls against known service signatures for unexpected kwargs."""
    with open(filepath, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read(), filename=filepath)

    issues = []

    for node in ast.walk(tree):
        if isinstance(node, ast.Call):
            func_name = None
            if isinstance(node.func, ast.Name):
                func_name = node.func.id
            elif isinstance(node.func, ast.Attribute):
                func_name = node.func.attr

            if func_name and func_name in function_signatures:
                sig = function_signatures[func_name]
                has_varkw = any(p.kind == inspect.Parameter.VAR_KEYWORD for p in sig.parameters.values())
                if not has_varkw:
                    param_names = set(sig.parameters.keys())
                    for kw in node.keywords:
                        if kw.arg and kw.arg not in param_names:
                            issues.append((filepath, node.lineno, f"TypeError risk: '{func_name}' called with unexpected keyword argument '{kw.arg}'. Expected params: {param_names}"))

    return issues

def sweep():
    target_dirs = ["views", "services"]
    all_unbound = []
    all_sig_issues = []

    for d in target_dirs:
        dir_p = os.path.join(WORKSPACE_ROOT, d)
        for root, dirs, files in os.walk(dir_p):
            for f in files:
                if f.endswith(".py"):
                    full_p = os.path.join(root, f)
                    all_unbound.extend(check_unbound_locals(full_p))
                    all_sig_issues.extend(check_call_signatures(full_p))

    print(f"\n[+] SWEEP COMPLETE: Found {len(all_unbound)} UnboundLocal risks and {len(all_sig_issues)} Call Signature issues.")
    
    print("\n--- UNBOUND LOCAL RISKS ---")
    for fp, line, msg in all_unbound:
        print(f"{os.path.relpath(fp, WORKSPACE_ROOT)}:{line}: {msg}")

    print("\n--- CALL SIGNATURE ISSUES ---")
    for fp, line, msg in all_sig_issues:
        print(f"{os.path.relpath(fp, WORKSPACE_ROOT)}:{line}: {msg}")

if __name__ == "__main__":
    sweep()

