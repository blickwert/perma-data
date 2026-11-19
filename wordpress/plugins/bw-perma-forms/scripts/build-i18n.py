#!/usr/bin/env python3
"""Compiles free/languages/*.po into .mo (PHP) and the JSON file for the admin app (wp_set_script_translations).

    python3 scripts/build-i18n.py
"""
import ast
import hashlib
import json
import re
import struct
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LANG = ROOT / "free/languages"
DOMAIN = "bw-perma-forms"
SCRIPTS = ["build/admin.js", "blocks/perma-form/editor.js"]  # relative to the plugin folder, as WordPress hashes them


def parse_po(text):
    entries, key, cur = {}, None, None
    for line in text.splitlines():
        line = line.strip()
        if line.startswith("msgid "):
            key, cur = ast.literal_eval(line[6:]), "id"
        elif line.startswith("msgstr "):
            entries[key] = ast.literal_eval(line[7:])
            cur = "str"
        elif line.startswith('"') and key is not None:
            if cur == "id":
                key += ast.literal_eval(line)
            else:
                entries[key] += ast.literal_eval(line)
    return entries


def write_mo(entries, path):
    keys = sorted(entries)
    ids = b"".join(k.encode() + b"\0" for k in keys)
    strs = b"".join(entries[k].encode() + b"\0" for k in keys)
    n = len(keys)
    o_ids, o_strs = 7 * 4, 7 * 4 + n * 8
    start = o_strs + n * 8
    id_table, pos = [], 0
    for k in keys:
        b = k.encode()
        id_table += [len(b), start + pos]
        pos += len(b) + 1
    str_start, str_table, pos = start + len(ids), [], 0
    for k in keys:
        b = entries[k].encode()
        str_table += [len(b), str_start + pos]
        pos += len(b) + 1
    data = struct.pack("Iiiiiii", 0x950412DE, 0, n, o_ids, o_strs, 0, 0)
    data += struct.pack(f"{2 * n}i", *id_table) + struct.pack(f"{2 * n}i", *str_table) + ids + strs
    path.write_bytes(data)


for po in LANG.glob(f"{DOMAIN}-*.po"):
    locale = po.stem[len(DOMAIN) + 1:]
    entries = parse_po(po.read_text("utf-8"))
    header = entries.get("", "")
    write_mo(entries, po.with_suffix(".mo"))
    messages = {"": {"domain": "messages", "lang": locale, "plural-forms": "nplurals=2; plural=(n != 1);"}}
    messages.update({k: [v] for k, v in entries.items() if k})
    for script in SCRIPTS:
        h = hashlib.md5(script.encode()).hexdigest()
        out = LANG / f"{DOMAIN}-{locale}-{h}.json"
        out.write_text(json.dumps({"domain": "messages", "locale_data": {"messages": messages}}, ensure_ascii=False), "utf-8")
    print(f"{po.name}: {len(entries) - 1} Texte -> .mo + {len(SCRIPTS)} JSON")
