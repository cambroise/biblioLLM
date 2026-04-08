#!/usr/bin/env python3
"""Validate YAML headers in .qmd and .Rmd files."""

import sys
import re
import yaml
from pathlib import Path


def extract_yaml_header(filepath: Path) -> tuple[str | None, int]:
    """Extract YAML header from a qmd/Rmd file. Returns (yaml_str, end_line)."""
    lines = filepath.read_text(encoding="utf-8").splitlines()
    if not lines or lines[0].strip() != "---":
        return None, 0

    for i, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return "\n".join(lines[1:i]), i
    return None, 0


def validate_yaml(filepath: Path) -> list[dict]:
    """Validate YAML header and return list of issues."""
    issues = []
    yaml_str, end_line = extract_yaml_header(filepath)

    if yaml_str is None:
        issues.append({
            "level": "error",
            "line": 1,
            "message": "Header YAML absent ou mal formé (pas de délimiteurs ---)"
        })
        return issues

    try:
        data = yaml.safe_load(yaml_str)
    except yaml.YAMLError as e:
        line = getattr(e, 'problem_mark', None)
        lineno = (line.line + 2) if line else 1
        issues.append({
            "level": "error",
            "line": lineno,
            "message": f"Erreur de syntaxe YAML : {e}"
        })
        return issues

    if not isinstance(data, dict):
        issues.append({
            "level": "error",
            "line": 1,
            "message": "Le header YAML n'est pas un dictionnaire valide"
        })
        return issues

    # Check for title
    if "title" not in data:
        issues.append({
            "level": "warning",
            "line": 1,
            "message": "Champ 'title' manquant dans le header YAML"
        })

    # Check format field
    if "format" in data:
        fmt = data["format"]
        valid_formats = {"html", "pdf", "docx", "revealjs", "beamer", "pptx",
                         "epub", "gfm", "hugo-md", "typst"}
        if isinstance(fmt, dict):
            for key in fmt:
                if key not in valid_formats:
                    issues.append({
                        "level": "warning",
                        "line": 1,
                        "message": f"Format '{key}' non standard (valides : {', '.join(sorted(valid_formats))})"
                    })
    elif "output" in data:
        issues.append({
            "level": "warning",
            "line": 1,
            "message": "Utilise 'output:' (syntaxe Rmd) au lieu de 'format:' (syntaxe qmd)"
        })

    # Check bibliography file exists
    if "bibliography" in data:
        bib_path = filepath.parent / data["bibliography"]
        if not bib_path.exists():
            issues.append({
                "level": "error",
                "line": 1,
                "message": f"Fichier bibliographie '{data['bibliography']}' introuvable"
            })

    return issues


def main():
    if len(sys.argv) < 2:
        print("Usage: check_yaml.py <fichier.qmd> [fichier2.qmd ...]")
        sys.exit(1)

    all_ok = True
    for arg in sys.argv[1:]:
        filepath = Path(arg)
        if not filepath.exists():
            print(f"❌ {filepath} : fichier introuvable")
            all_ok = False
            continue

        issues = validate_yaml(filepath)
        if not issues:
            print(f"✅ {filepath} : header YAML valide")
        else:
            all_ok = False
            for issue in issues:
                icon = "❌" if issue["level"] == "error" else "⚠️"
                print(f"{icon} {filepath}:{issue['line']} — {issue['message']}")

    sys.exit(0 if all_ok else 1)


if __name__ == "__main__":
    main()
