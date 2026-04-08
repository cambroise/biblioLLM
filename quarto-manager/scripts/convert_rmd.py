#!/usr/bin/env python3
"""Convert .Rmd files to .qmd format.

Handles: YAML header (output→format), chunk options (inline→hashpipe),
cross-references (bookdown→quarto), math delimiters, callouts.
"""

import sys
import re
import shutil
from pathlib import Path


# YAML output format mappings
FORMAT_MAP = {
    "html_document": "html",
    "pdf_document": "pdf",
    "word_document": "docx",
    "bookdown::html_document2": "html",
    "bookdown::pdf_document2": "pdf",
    "bookdown::pdf_book": "pdf",
    "bookdown::gitbook": "html",
    "bookdown::word_document2": "docx",
    "xaringan::moon_reader": "revealjs",
    "beamer_presentation": "beamer",
    "powerpoint_presentation": "pptx",
    "ioslides_presentation": "revealjs",
}

# Chunk option mappings (Rmd → qmd hashpipe)
OPTION_MAP = {
    "echo": "echo",
    "eval": "eval",
    "include": "include",
    "message": "message",
    "warning": "warning",
    "cache": "cache",
    "fig.cap": "fig-cap",
    "fig.width": "fig-width",
    "fig.height": "fig-height",
    "fig.align": "fig-align",
    "out.width": "out-width",
    "out.height": "out-height",
    "fig.alt": "fig-alt",
    "results": None,  # special handling
}


def convert_yaml_header(yaml_lines: list[str]) -> list[str]:
    """Convert Rmd YAML header to qmd format."""
    result = []
    for line in yaml_lines:
        # Replace 'output:' with 'format:'
        new_line = re.sub(r'^(\s*)output:', r'\1format:', line)
        # Replace format names
        for rmd_fmt, qmd_fmt in FORMAT_MAP.items():
            new_line = new_line.replace(rmd_fmt, qmd_fmt)
        # toc_float → toc-location
        new_line = re.sub(r'(\s*)toc_float:\s*true', r'\1toc-location: left', new_line)
        new_line = re.sub(r'(\s*)toc_float:\s*false', '', new_line)
        # number_sections → number-sections
        new_line = new_line.replace("number_sections:", "number-sections:")
        new_line = new_line.replace("code_folding:", "code-fold:")
        result.append(new_line)
    return result


def convert_chunk_header(match: re.Match) -> str:
    """Convert a chunk header from Rmd to qmd format."""
    engine = match.group(1)  # r, python, etc.
    options_str = match.group(2) if match.group(2) else ""

    hashpipe_lines = []

    # Parse options
    if options_str:
        options_str = options_str.strip().rstrip(",")
        # First token might be the label (no = sign)
        parts = re.split(r',\s*(?=[a-zA-Z._]+\s*=)', options_str)
        for part in parts:
            part = part.strip()
            if not part:
                continue
            if "=" not in part:
                # This is a label
                hashpipe_lines.append(f"#| label: {part.strip()}")
            else:
                key, _, value = part.partition("=")
                key = key.strip()
                value = value.strip()

                # Convert boolean values
                if value.upper() in ("TRUE", "T"):
                    value = "true"
                elif value.upper() in ("FALSE", "F"):
                    value = "false"

                # Remove quotes for simple strings
                if value.startswith('"') and value.endswith('"'):
                    pass  # keep quoted
                elif value.startswith("'") and value.endswith("'"):
                    value = f'"{value[1:-1]}"'

                # Map option names
                if key == "results":
                    if value in ("'hide'", '"hide"'):
                        hashpipe_lines.append("#| output: false")
                    elif value in ("'asis'", '"asis"'):
                        hashpipe_lines.append("#| output: asis")
                    else:
                        hashpipe_lines.append(f"#| results: {value}")
                elif key in OPTION_MAP and OPTION_MAP[key]:
                    hashpipe_lines.append(f"#| {OPTION_MAP[key]}: {value}")
                else:
                    # Pass through unknown options with dot→dash
                    qmd_key = key.replace(".", "-")
                    hashpipe_lines.append(f"#| {qmd_key}: {value}")

    result = f"```{{{engine}}}\n"
    if hashpipe_lines:
        result += "\n".join(hashpipe_lines) + "\n"
    return result


def convert_crossrefs(content: str) -> str:
    """Convert bookdown cross-references to Quarto format."""
    # \@ref(fig:label) → @fig-label
    content = re.sub(r'\\@ref\(fig:([^)]+)\)', r'@fig-\1', content)
    content = re.sub(r'\\@ref\(tab:([^)]+)\)', r'@tbl-\1', content)
    content = re.sub(r'\\@ref\(eq:([^)]+)\)', r'@eq-\1', content)
    content = re.sub(r'\\@ref\(sec:([^)]+)\)', r'@sec-\1', content)
    return content


def convert_callouts(content: str) -> str:
    """Convert Rmd custom divs to Quarto callouts."""
    callout_map = {
        "rmdnote": "callout-note",
        "rmdwarning": "callout-warning",
        "rmdtip": "callout-tip",
        "rmdimportant": "callout-important",
        "rmdcaution": "callout-caution",
    }
    for rmd_class, qmd_class in callout_map.items():
        content = content.replace(f".{rmd_class}", f".{qmd_class}")
    return content


def convert_math_delimiters(content: str) -> str:
    """Convert LaTeX delimiters to $ and $$."""
    # \( ... \) → $ ... $
    content = re.sub(r'\\\(', '$', content)
    content = re.sub(r'\\\)', '$', content)
    # \[ ... \] → $$ ... $$
    content = re.sub(r'\\\[', '$$', content)
    content = re.sub(r'\\\]', '$$', content)
    return content


def convert_file(input_path: Path, output_path: Path, backup_dir: Path | None = None):
    """Convert a single .Rmd file to .qmd."""
    content = input_path.read_text(encoding="utf-8")

    # Backup
    if backup_dir:
        backup_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(input_path, backup_dir / f"{input_path.name}.bak")

    lines = content.splitlines(keepends=True)

    # Split YAML header from body
    yaml_start = -1
    yaml_end = -1
    dash_count = 0
    for i, line in enumerate(lines):
        if line.strip() == "---":
            dash_count += 1
            if dash_count == 1:
                yaml_start = i
            elif dash_count == 2:
                yaml_end = i
                break

    if yaml_start >= 0 and yaml_end > yaml_start:
        yaml_lines = lines[yaml_start + 1:yaml_end]
        yaml_converted = convert_yaml_header(yaml_lines)
        body = "".join(lines[yaml_end + 1:])
    else:
        yaml_converted = None
        body = content

    # Convert chunk headers
    body = re.sub(
        r'```\{(\w+)(?:\s*,?\s*(.*?))?\}\s*\n',
        convert_chunk_header,
        body
    )

    # Convert cross-references
    body = convert_crossrefs(body)

    # Convert callouts
    body = convert_callouts(body)

    # Convert math delimiters
    body = convert_math_delimiters(body)

    # Reassemble
    if yaml_converted is not None:
        output = "---\n" + "".join(yaml_converted) + "---\n" + body
    else:
        output = body

    output_path.write_text(output, encoding="utf-8")
    print(f"✅ {input_path} → {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: convert_rmd.py <fichier.Rmd> [--output <fichier.qmd>] [--backup-dir backup/]")
        sys.exit(1)

    input_path = Path(sys.argv[1])
    output_path = input_path.with_suffix(".qmd")
    backup_dir = None

    args = sys.argv[2:]
    i = 0
    while i < len(args):
        if args[i] == "--output" and i + 1 < len(args):
            output_path = Path(args[i + 1])
            i += 2
        elif args[i] == "--backup-dir" and i + 1 < len(args):
            backup_dir = Path(args[i + 1])
            i += 2
        else:
            i += 1

    if not input_path.exists():
        print(f"❌ Fichier introuvable : {input_path}")
        sys.exit(1)

    convert_file(input_path, output_path, backup_dir)


if __name__ == "__main__":
    main()
