"""Check local Markdown file links without network access or external packages."""
from pathlib import Path
import re
from urllib.parse import unquote

root = Path(__file__).resolve().parents[1]
errors = []
checked = 0
for source in root.rglob("*.md"):
    if ".git" in source.relative_to(root).parts:
        continue
    for match in re.finditer(r"!?\[[^\]]*\]\(([^)]+)\)", source.read_text(encoding="utf-8-sig")):
        target = match.group(1).split(' "', 1)[0].strip("<>")
        if target.startswith(("http:", "https:", "mailto:", "#")):
            continue
        checked += 1
        file_part = unquote(target.split("#", 1)[0])
        if file_part and not (source.parent / file_part).exists():
            errors.append(f"{source.relative_to(root)}: {target}")
if errors:
    raise SystemExit("Broken local links:\n" + "\n".join(errors))
print(f"Checked {checked} local Markdown links; no missing files.")
