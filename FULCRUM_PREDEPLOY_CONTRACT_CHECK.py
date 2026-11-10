#!/usr/bin/env python3
"""Read-only static release gate for Fulcrum-Beta.

Usage: python FULCRUM_PREDEPLOY_CONTRACT_CHECK.py /path/to/Fulcrum-Beta-main
For real release safety run this *inside* the Python 3.11 Docker image and also
run DB integration / authenticated browser smoke tests; this does not replace them.
"""
from __future__ import annotations
import ast
import collections
import pathlib
import re
import sys

ROOT = pathlib.Path(sys.argv[1] if len(sys.argv) > 1 else '.').resolve()
CHECK_PY = [ROOT/'app.py', *sorted((ROOT/'services').glob('*.py')), *sorted((ROOT/'views').glob('*.py'))]
MIGRATIONS = sorted((ROOT/'migrations').glob('*.sql'))
errors = []
print('FULCRUM PREDEPLOY STATIC CONTRACT CHECK (read-only)')
print('Root:', ROOT, '| Python:', sys.version.split()[0])

# Stage 1 - syntax checks on actual runtime interpreter, *not* host dev version.
trees = {}
for file in CHECK_PY:
    try:
        source=file.read_text(encoding='utf-8')
        compile(source, str(file), 'exec')
        trees[file]=ast.parse(source)
    except Exception as ex:
        errors.append(f'SYNTAX {file.relative_to(ROOT)}: {type(ex).__name__}: {ex}')
print('Parsed', len(trees), 'runtime Python modules')
if sys.version_info[:2] != (3, 11):
    print('WARNING: run this in the Docker image (Python 3.11) to validate deployed syntax.')

# Stage 2 - internal import names (module-level exports only; conservative).
modules = {}
for file, t in trees.items():
    mod='.'.join(file.relative_to(ROOT).with_suffix('').parts)
    exports=set()
    for n in t.body:
        if isinstance(n,(ast.FunctionDef,ast.AsyncFunctionDef,ast.ClassDef)):
            exports.add(n.name)
        elif isinstance(n,(ast.Import,ast.ImportFrom)):
            exports.update(a.asname or (a.name.split('.')[0] if isinstance(n,ast.Import) else a.name) for a in n.names)
        elif isinstance(n,(ast.Assign,ast.AnnAssign)):
            tgts=n.targets if isinstance(n,ast.Assign) else [n.target]
            for target in tgts:
                exports.update(x.id for x in ast.walk(target) if isinstance(x,ast.Name) and isinstance(x.ctx,ast.Store))
    modules[mod]=exports
for file,t in trees.items():
    for n in ast.walk(t):
        if isinstance(n,ast.ImportFrom) and n.module in modules:
            for a in n.names:
                if a.name!='*' and a.name not in modules[n.module]:
                    errors.append(f'IMPORT {file.relative_to(ROOT)}:{n.lineno}: {n.module}.{a.name} does not exist')

# Stage 3 - extract DDL columns from CREATE and ALTER statements.
sql='\n'.join(p.read_text(encoding='utf-8') for p in MIGRATIONS)
sql='\n'.join(re.sub(r'--.*','',line) for line in sql.splitlines())
columns=collections.defaultdict(set)
for m in re.finditer(r'CREATE\s+TABLE\s+(?:IF\s+NOT\s+EXISTS\s+)?(?:public\.)?(\w+)\s*\(',sql,re.I):
    tname=m.group(1); pos=m.end(); depth=1; quote=None; begin=pos
    while pos<len(sql) and depth:
        ch=sql[pos]
        if quote:
            if ch==quote and sql[pos-1]!='\\':quote=None
        elif ch in ("'",'"'):quote=ch
        elif ch=='(':depth+=1
        elif ch==')':depth-=1
        pos+=1
    for line in sql[begin:pos-1].splitlines():
        match=re.match(r'^\s*"?(\w+)"?\s+([\w\[\]]+)',line)
        if match and match.group(2).upper() not in {'CONSTRAINT','FOREIGN','CHECK','UNIQUE','PRIMARY','REFERENCES'}:
            columns[tname].add(match.group(1))
for m in re.finditer(r'ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:public\.)?(\w+)\s+ADD\s+COLUMN\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)',sql,re.I):
    columns[m.group(1)].add(m.group(2))
# Include multiple ADD COLUMN clauses in a single ALTER statement.
for m in re.finditer(r'ALTER\s+TABLE\s+(?:IF\s+EXISTS\s+)?(?:public\.)?(\w+)([^;]+);',sql,re.I|re.S):
    for col in re.findall(r'(?:,\s*)?ADD\s+COLUMN\s+(?:IF\s+NOT\s+EXISTS\s+)?(\w+)',m.group(2),re.I):
        columns[m.group(1)].add(col)

# Stage 4 - check root production Python against *bundled* SQL contracts.
checked=0
for file,t in trees.items():
    for n in ast.walk(t):
        if not (isinstance(n,ast.Call) and isinstance(n.func,ast.Attribute) and n.func.attr in ('select','update','insert','upsert')):
            continue
        chain=n.func.value; table=None
        while isinstance(chain,ast.Call):
            f=chain.func
            if isinstance(f,ast.Attribute) and f.attr=='table' and chain.args and isinstance(chain.args[0],ast.Constant):
                table=chain.args[0].value;break
            chain=f.value if isinstance(f,ast.Attribute) else None
        if table not in ('profiles','account_lifecycle_log', 'account_lifecycle_audit_log') or not n.args:
            continue
        names=[]; arg=n.args[0]
        if n.func.attr=='select' and isinstance(arg,ast.Constant) and isinstance(arg.value,str):
            names=[piece.strip() for piece in arg.value.split(',') if re.fullmatch(r'\w+',piece.strip())]
        if n.func.attr in ('insert','update','upsert') and isinstance(arg,ast.Dict):
            names=[k.value for k in arg.keys if isinstance(k,ast.Constant) and isinstance(k.value,str)]
        for name in names:
            checked+=1
            if name not in columns[table]:
                errors.append(f'SCHEMA {file.relative_to(ROOT)}:{n.lineno}: {n.func.attr} on {table}.{name} (column absent from bundled migrations)')
print('Checked',checked,'literal profile/lifecycle column references')

# Stage 5 - hardcoded old Admin identity contradicts the fresh-Auth setup.
OLD_UUID = '616304b5-aef5-4cd0-88be-2fda7ddf7f88'
for path in MIGRATIONS:
    if path.name.startswith(('008_','009_')):
        for i, line in enumerate(path.read_text(encoding='utf-8').splitlines(),1):
            if OLD_UUID in line and not line.lstrip().startswith('--'):
                errors.append(f'ADMIN-BOOTSTRAP {path.relative_to(ROOT)}:{i}: fixed old UUID conflicts with fresh Supabase Admin UUID')

print('\nRESULT:',len(errors),'release blockers/static warnings detected')
for err in errors:
    print(' -',err)
if errors:
    print('\nBLOCK RELEASE. Resolve these, then rerun with the exact 3.11 image and live staging schema/browser checks.')
    sys.exit(1)
print('Static contracts passed. DB integration and authenticated browser smoke tests still required.')

