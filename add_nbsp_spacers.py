import re, io, sys
from pathlib import Path

try:
    import yaml  # PyYAML
except ImportError:
    print("PyYAML not found. Install with: pip install pyyaml")
    sys.exit(1)

PATH = Path("templates.yaml")

if not PATH.exists():
    print("templates.yaml not found at repo root.")
    sys.exit(1)

with io.open(PATH, "r", encoding="utf-8") as f:
    data = yaml.safe_load(f)

def add_spacers_to_body(body: str) -> str:
    """
    For each bold section line (e.g., '**KA:**' or '**API Specific Info**'),
    insert a following line '  \\u00A0' if not already present.
    """
    lines = body.splitlines()
    out = []
    i = 0
    while i < len(lines):
        line = lines[i]
        out.append(line)

        is_section_with_colon = re.match(r'^\s*\*\*.+\*\*:', line) is not None
        is_section_header_only = re.match(r'^\s*\*\*.+\*\*\s*$', line) is not None

        if is_section_with_colon or is_section_header_only:
            nxt = lines[i+1] if i + 1 < len(lines) else ""
            if nxt.strip() != r"\u00A0":
                out.append("  \\u00A0")  # keep as the literal backslash-u sequence
        i += 1
    return "\n".join(out)

changed = False
for t in (data.get("templates") or []):
    if isinstance(t, dict) and isinstance(t.get("body"), str):
        new_body = add_spacers_to_body(t["body"])
        if new_body != t["body"]:
            t["body"] = new_body
            changed = True

if not changed:
    print("No changes necessary; spacer lines already present.")
    sys.exit(0)

with io.open(PATH, "w", encoding="utf-8") as f:
    # sort_keys=False preserves your key order; width avoids unwanted line wraps
    yaml.safe_dump(data, f, sort_keys=False, allow_unicode=True, width=1000)

print("Inserted \\u00A0 spacer lines after bold sections across all templates.")
