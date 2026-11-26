"""Rebuild the word lists inside index.html from a spelling-words.json file and bump the
offline cache version so installed copies refresh.
Usage: python3 tools/update_words.py path/to/spelling-words.json"""
import json, re, sys, pathlib
root = pathlib.Path(__file__).resolve().parent.parent
d = json.load(open(sys.argv[1]))
words = {l["id"]: [[w["word"], w["sentence"], w["definition"]] for w in l["words"]] for l in d["levels"]}
ages = {"level1": "age 5", "level2": "age 8", "level3": "grown-ups", "level4": "grown-up champs"}
levels = {l["id"]: {"name": l["name"], "age": ages.get(l["id"], l.get("ages", "")), "free": 1 if l["id"] == "level1" else 0} for l in d["levels"]}
p = root / "index.html"; s = p.read_text()
s, n1 = re.subn(r"const WORDS = .*?;\n", lambda m: "const WORDS = " + json.dumps(words, separators=(",", ":")) + ";\n", s, count=1)
s, n2 = re.subn(r"const LEVELS = .*?;\n", lambda m: "const LEVELS = " + json.dumps(levels) + ";\n", s, count=1)
assert n1 == n2 == 1, "word list markers not found"
p.write_text(s)
sw = root / "sw.js"; t = sw.read_text()
t = re.sub(r'family-bee-v(\d+)', lambda m: f"family-bee-v{int(m.group(1)) + 1}", t, count=1)
sw.write_text(t)
print({k: len(v) for k, v in words.items()}, re.search(r'family-bee-v\d+', t).group(0))
