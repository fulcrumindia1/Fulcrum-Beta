import os
import re

for root, dirs, files in os.walk("."):
    if ".git" in root or "__pycache__" in root or ".pytest_cache" in root:
        continue
    for file in files:
        if file.endswith(".py"):
            path = os.path.join(root, file)
            with open(path, "r", encoding="utf-8") as f:
                try:
                    lines = f.readlines()
                except Exception:
                    continue
            for idx, line in enumerate(lines, 1):
                if "f\"" in line or "f'" in line or 'f"""' in line or "f'''" in line:
                    for match in re.finditer(r'\{([^}]+)\}', line):
                        expr = match.group(1)
                        if '\\' in expr:
                            print(f"{path}:{idx}: {line.strip()}")
