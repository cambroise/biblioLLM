#!/usr/bin/env python3
"""Check bibliography consistency: citations in .qmd vs entries in .bib."""

import sys
import re
from pathlib import Path


def parse_bib_keys(bib_path: Path) -> set[str]:
    """Extract all entry keys from a .bib file."""
    content = bib_path.read_text(encoding="utf-8")
    # Match @type{key,
    keys = set(re.findall(r'@\w+\{([^,\s]+)', content))
    return keys


def validate_bib_syntax(bib_path: Path) -> list[dict]:
    """Basic syntax validation of .bib file."""
    issues = []
    content = bib_path.read_text(encoding="utf-8")
    lines = content.splitlines()

    brace_depth = 0
    current_entry = None
    entry_start = 0

    for lineno, line in enumerate(lines, start=1):
        # Track entry starts
        entry_match = re.match(r'@(\w+)\{([^,\s]*)', line)
        if entry_match:
            if brace_depth != 0:
                issues.append({
                    "level": "error",
                    "line": lineno,
                    "message": f"Nouvelle entrée '{entry_match.group(2)}' avant la fin de l'entrée précédente"
                })
            current_entry = entry_match.group(2)
            entry_start = lineno
            if not current_entry:
                issues.append({
                    "level": "error",
                    "line": lineno,
                    "message": f"Entrée @{entry_match.group(1)} sans clé"
                })

        brace_depth += line.count("{") - line.count("}")

    if brace_depth != 0:
        issues.append({
            "level": "error",
            "line": len(lines),
            "message": f"Accolades non appariées (profondeur finale : {brace_depth})"
        })

    return issues


def extract_citations(qmd_dir: Path) -> dict[str, list[tuple[str, int]]]:
    """Extract all citations from .qmd files. Returns {key: [(file, line), ...]}."""
    citations = {}
    # Match @key but exclude @fig-, @tbl-, @eq-, @sec- (cross-references)
    citation_re = re.compile(r'(?<!\\)@(?!fig-|tbl-|eq-|sec-)([a-zA-Z0-9_][a-zA-Z0-9_:.\-]*)')

    for qmd_file in sorted(qmd_dir.rglob("*.qmd")):
        # Skip generated directories
        if "_site" in qmd_file.parts or "_book" in qmd_file.parts:
            continue

        content = qmd_file.read_text(encoding="utf-8")
        lines = content.splitlines()

        in_code = False
        in_yaml = False
        yaml_count = 0

        for lineno, line in enumerate(lines, start=1):
            if line.strip() == "---":
                yaml_count += 1
                if yaml_count <= 2:
                    in_yaml = not in_yaml
                continue
            if in_yaml:
                continue
            if line.strip().startswith("```"):
                in_code = not in_code
                continue
            if in_code:
                continue

            for match in citation_re.finditer(line):
                key = match.group(1)
                if key not in citations:
                    citations[key] = []
                rel_path = qmd_file.relative_to(qmd_dir)
                citations[key].append((str(rel_path), lineno))

    return citations


def main():
    if len(sys.argv) < 2:
        print("Usage: check_bib.py <references.bib> [--qmd-dir <project-dir>]")
        sys.exit(1)

    bib_path = Path(sys.argv[1])
    qmd_dir = None

    if "--qmd-dir" in sys.argv:
        idx = sys.argv.index("--qmd-dir")
        if idx + 1 < len(sys.argv):
            qmd_dir = Path(sys.argv[idx + 1])

    if not bib_path.exists():
        print(f"❌ Fichier .bib introuvable : {bib_path}")
        sys.exit(1)

    # Validate .bib syntax
    syntax_issues = validate_bib_syntax(bib_path)
    if syntax_issues:
        print(f"\n## Problèmes de syntaxe dans {bib_path}")
        for issue in syntax_issues:
            icon = "❌" if issue["level"] == "error" else "⚠️"
            print(f"  {icon} ligne {issue['line']} — {issue['message']}")
    else:
        print(f"✅ {bib_path} : syntaxe BibTeX valide")

    # Extract bib keys
    bib_keys = parse_bib_keys(bib_path)
    print(f"\nEntrées dans le .bib : {len(bib_keys)}")

    # Cross-reference with .qmd files
    if qmd_dir and qmd_dir.exists():
        citations = extract_citations(qmd_dir)
        cited_keys = set(citations.keys())

        # Orphan citations (in .qmd but not in .bib)
        orphans = cited_keys - bib_keys
        if orphans:
            print(f"\n⚠️ Citations sans entrée .bib ({len(orphans)}) :")
            for key in sorted(orphans):
                locations = citations[key]
                locs_str = ", ".join(f"{f}:{l}" for f, l in locations)
                print(f"  - @{key} (dans {locs_str})")

        # Unused entries (in .bib but never cited)
        unused = bib_keys - cited_keys
        if unused:
            print(f"\nℹ️ Entrées .bib non citées ({len(unused)}) :")
            for key in sorted(unused):
                print(f"  - @{key}")

        # Summary
        if not orphans and not unused:
            print("\n✅ Toutes les citations correspondent à des entrées .bib et vice versa")
        elif not orphans:
            print(f"\n✅ Toutes les citations sont résolues ({len(unused)} entrée(s) .bib non utilisée(s))")
    else:
        if qmd_dir:
            print(f"\n⚠️ Répertoire {qmd_dir} introuvable, vérification croisée impossible")
        else:
            print("\nℹ️ Utilisez --qmd-dir pour croiser les citations avec les fichiers .qmd")


if __name__ == "__main__":
    main()
