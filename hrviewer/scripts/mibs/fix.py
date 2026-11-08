#!/usr/bin/env python3
# Nutzung: python3 fixmib.py original.mib fixed.mib
import re, sys

src = open(sys.argv[1], encoding='utf-8', errors='replace').read()
src = src.replace('\r\n', '\n').replace('\r', '\n').replace('\u00a0', ' ')

# 1) Enum-Labels: "Text mit Leerzeichen"(1) -> gueltige Identifier
def fix_enum(m):
    kind, body = m.group(1), m.group(2)
    seen, out = {}, []
    for label, val in re.findall(r'"([^"]*)"\s*\(\s*(-?\d+)\s*\)', body):
        name = re.sub(r'[^A-Za-z0-9]+', '-', label).strip('-').lower()
        if not name or not name[0].isalpha():
            name = 'v-' + name
        seen[name] = seen.get(name, 0) + 1
        if seen[name] > 1:
            name += f'-{val}'
        out.append(f'{name}({val})')
    return f'{kind} {{ ' + ', '.join(out) + ' }'

src = re.sub(r'\b(INTEGER|BITS)\s*\{([^{}]*"[^{}]*)\}', fix_enum, src)

# 2) Objektnamen (vor OBJECT-TYPE usw.) muessen klein beginnen
module = re.match(r'\s*([A-Za-z0-9-]+)\s+DEFINITIONS', src).group(1)
RESERVED = {'SYNTAX', 'ACCESS', 'MAX-ACCESS', 'STATUS', 'DESCRIPTION', 'INDEX',
            'REFERENCE', 'UNITS', 'DEFVAL', 'AUGMENTS', 'OBJECTS', 'MODULE',
            'IMPORTS', 'FROM', 'BEGIN', 'END', 'SIZE', 'ENTERPRISE', 'VARIABLES'}

obj_names = set(re.findall(
    r'^[ \t]*([A-Z][A-Za-z0-9-]*)[ \t]+'
    r'(?:OBJECT-TYPE|OBJECT-IDENTITY|MODULE-IDENTITY|NOTIFICATION-TYPE|TRAP-TYPE'
    r'|OBJECT[ \t]+IDENTIFIER[ \t]*::=)',
    src, re.M))
obj_names -= RESERVED
obj_names.discard(module)

for n in sorted(obj_names, key=len, reverse=True):
    src = re.sub(rf'(?<![\w-]){re.escape(n)}(?![\w-])', n[0].lower() + n[1:], src)

# 3) Zeilentypen: Namen aus "SEQUENCE OF X" ableiten, ueberall gross schreiben
of_types = set(re.findall(r'SEQUENCE\s+OF\s+([A-Za-z][\w-]*)', src))
seq_types = set(re.findall(r'^[ \t]*([A-Za-z][\w-]*)\s*::=\s*SEQUENCE\b', src, re.M))
types = {t[0].upper() + t[1:] for t in of_types | seq_types}
lower_to_type = {t[0].lower() + t[1:]: t for t in types}

def to_type(name):
    return lower_to_type.get(name[0].lower() + name[1:], name)

src = re.sub(r'(SEQUENCE\s+OF\s+)([A-Za-z][\w-]*)',
             lambda m: m.group(1) + to_type(m.group(2)), src)
src = re.sub(r'(SYNTAX\s+)([A-Za-z][\w-]*)(?=\s*(?:\n|$))',
             lambda m: m.group(1) + to_type(m.group(2)), src)
src = re.sub(r'^([ \t]*)([A-Za-z][\w-]*)(\s*::=\s*SEQUENCE\b)',
             lambda m: m.group(1) + to_type(m.group(2)) + m.group(3), src, flags=re.M)

# 4) Leere OBJECTS-Klauseln entfernen
src = re.sub(r'^[ \t]*OBJECTS[ \t]*\{\s*\}[ \t]*\n', '', src, flags=re.M)

open(sys.argv[2], 'w', encoding='utf-8').write(src)
print(f'{len(obj_names)} Objektnamen, {len(seq_types)} Zeilentypen bearbeitet')