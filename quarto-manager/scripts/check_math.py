#!/usr/bin/env python3
"""Check math delimiter consistency in .qmd/.Rmd files.

Enforces user preferences: $...$ for inline, $$...$$ for display.
Detects LaTeX-style \\(...\\) and \\[...\\] delimiters.
"""

import sys
import re
from pathlib import Path


def check_math_delimiters(filepath: Path) -> list[dict]:
    """Check math delimiters in a file. Returns list of issues."""
    issues = []
    content = filepath.read_text(encoding="utf-8")
    lines = content.splitlines()

    in_code_block = False
    in_yaml = False
    yaml_count = 0

    for lineno, line in enumerate(lines, start=1):
        # Track YAML header
        if line.strip() == "---":
            yaml_count += 1
            if yaml_count <= 2:
                in_yaml = not in_yaml
                continue
        if in_yaml:
            continue

        # Track code blocks
        if line.strip().startswith("```"):
            in_code_block = not in_code_block
            continue
        if in_code_block:
            continue

        # Check for LaTeX-style delimiters
        if r"\(" in line or r"\)" in line:
            issues.append({
                "level": "warning",
                "line": lineno,
                "message": r"Délimiteur LaTeX \(...\) détecté, utiliser $...$ à la place"
            })

        if r"\[" in line or r"\]" in line:
            # Avoid false positives with markdown links
            # Only flag if not preceded by ] or followed by (
            stripped = re.sub(r'\[[^\]]*\]\([^)]*\)', '', line)  # remove md links
            if r"\[" in stripped or r"\]" in stripped:
                issues.append({
                    "level": "warning",
                    "line": lineno,
                    "message": r"Délimiteur LaTeX \[...\] détecté, utiliser $$...$$ à la place"
                })

        # Check for unbalanced single $ (inline math)
        # Remove $$ first to avoid false positives
        line_no_display = line.replace("$$", "  ")
        # Remove escaped \$
        line_clean = line_no_display.replace(r"\$", "  ")
        # Count remaining $
        dollar_count = line_clean.count("$")
        if dollar_count % 2 != 0:
            issues.append({
                "level": "warning",
                "line": lineno,
                "message": f"Nombre impair de $ sur cette ligne ({dollar_count}) — possible délimiteur non fermé"
            })

    # Check for unbalanced $$ (display math) across the file
    non_code_content = []
    in_code = False
    in_y = False
    y_count = 0
    for line in lines:
        if line.strip() == "---":
            y_count += 1
            if y_count <= 2:
                in_y = not in_y
                continue
        if in_y:
            continue
        if line.strip().startswith("```"):
            in_code = not in_code
            continue
        if not in_code:
            non_code_content.append(line)

    full_text = "\n".join(non_code_content)
    display_count = full_text.count("$$")
    if display_count % 2 != 0:
        issues.append({
            "level": "error",
            "line": 0,
            "message": f"Nombre impair de $$ dans le fichier ({display_count}) — équation display non fermée"
        })

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: check_math.py <fichier.qmd> [fichier2.qmd ...]")
        sys.exit(1)

    all_ok = True
    for arg in sys.argv[1:]:
        filepath = Path(arg)
        if not filepath.exists():
            print(f"❌ {filepath} : fichier introuvable")
            all_ok = False
            continue

        issues = check_math_delimiters(filepath)
        if not issues:
            print(f"✅ {filepath} : délimiteurs mathématiques cohérents")
        else:
            all_ok = False
            for issue in issues:
                icon = "❌" if issue["level"] == "error" else "⚠️"
                loc = f":{issue['line']}" if issue["line"] > 0 else ""
                print(f"{icon} {filepath}{loc} — {issue['message']}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
