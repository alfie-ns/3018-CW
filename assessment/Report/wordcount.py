#!/usr/bin/env python3
"""Prose-only word count for COMP_3018_Report.md, split by task.
Excludes: YAML frontmatter, HTML comments, LaTeX environments, code blocks,
inline code, maths, images, block quotes, reference sections, inline quotes,
heading markers, checkboxes, appendix."""

import re, sys

def strip_prose(text: str) -> int:
    """Strip non-prose content and return word count of remaining text."""

    # HTML comments
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)

    # LaTeX environments (figure, table, tikzpicture, lstlisting, mdframed, etc.)
    text = re.sub(r'\\begin\{[^}]*\}.*?\\end\{[^}]*\}', '', text, flags=re.DOTALL)

    # remaining standalone LaTeX commands on their own lines
    text = re.sub(r'(?m)^\\[a-zA-Z].*$', '', text)

    # fenced code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)

    # inline code
    text = re.sub(r'`[^`]+`', '', text)

    # display maths ($$...$$)
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)

    # inline maths ($...$)
    text = re.sub(r'\$[^$]+\$', '', text)

    # images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)

    # block quotes
    text = re.sub(r'(?m)^>.*$', '', text)

    # reference sections: detect heading at level N, skip until heading at level <= N
    in_refs = False
    ref_level = 0
    filtered = []
    for line in text.split('\n'):
        heading_match = re.match(r'^(#{1,3})\s+', line)
        if heading_match:
            level = len(heading_match.group(1))
            if re.search(r'[Rr]eferences', line):
                in_refs = True
                ref_level = level
                continue
            elif in_refs and level <= ref_level:
                in_refs = False
        if in_refs:
            continue
        filtered.append(line)
    text = '\n'.join(filtered)

    # inline quotes: "..." or "..." (15+ chars = cited material)
    text = re.sub(r'“[^”]{15,}”', '', text)
    text = re.sub(r'"[^"]{15,}"', '', text)

    # heading markers
    text = re.sub(r'(?m)^#+\s*', '', text)

    # checkbox prefixes
    text = re.sub(r'- \[.\]\s*', '', text)

    # markdown links (keep text, drop URL)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)

    # bold/italic markers
    text = re.sub(r'[*_]{1,2}', '', text)

    return len(text.split())


def main():
    fp = sys.argv[1] if len(sys.argv) > 1 else 'COMP_3018_Report.md'
    with open(fp, 'r') as f:
        lines = f.readlines()

    # find task boundaries by heading patterns
    task3_start = task4_start = appendix_start = None
    for i, line in enumerate(lines):
        if re.match(r'^#\s+1-\s+Task', line):
            task3_start = i
        elif re.match(r'^#\s+2-\s+Task', line):
            task4_start = i
        elif re.match(r'^#\s+3\.\s+Appendix', line):
            appendix_start = i

    if task3_start is None or task4_start is None:
        print("Could not detect task boundaries.")
        sys.exit(1)

    task3_text = ''.join(lines[task3_start:task4_start])
    task4_end = appendix_start if appendix_start else len(lines)
    task4_text = ''.join(lines[task4_start:task4_end])

    # split Task 4 by section/author
    t4_sections = {}
    current_section = None
    section_lines = {}
    for i in range(task4_start, task4_end):
        line = lines[i]
        m = re.match(r'^##\s+(\d+\.\d+\.?)\s+(.*)', line)
        if m:
            current_section = m.group(1).rstrip('.') + ' ' + m.group(2).strip()
            section_lines[current_section] = []
        elif current_section:
            section_lines[current_section].append(line)

    t3 = strip_prose(task3_text)
    t4 = strip_prose(task4_text)

    print(f"Task 3 (Lit Review):       {t3} words  (limit: 1,800)")
    print(f"Task 4 (Programming):      {t4} words  (limit: 2,200)")
    print(f"Combined:                  {t3 + t4} words")
    print()

    alfie_total = 0
    salman_total = 0
    print("  Task 4 breakdown by section:")
    for section, slines in section_lines.items():
        count = strip_prose(''.join(slines))
        author = "Salman" if any(x in section.lower() for x in ["salman", "introduction", "outcome"]) else "Alfie"
        if "references" in section.lower():
            author = "Joint"
        print(f"    {section:<50s}  {count:>4d} w  ({author})")
        if author == "Alfie":
            alfie_total += count
        elif author == "Salman":
            salman_total += count

    print()
    print(f"  Alfie's Task 4 prose:    {alfie_total} words")
    print(f"  Salman's Task 4 prose:   {salman_total} words")
    print(f"  Remaining in Task 4:     {2200 - t4} words")
    print(f"  Salman's budget left:    {2200 - t4} words (all remaining space is his sections)")


if __name__ == '__main__':
    main()
