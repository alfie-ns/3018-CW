#!/usr/bin/env python3
"""Compare different word-count methods for Task 3 and Task 4.

Per the user's `feedback_word_count.md` rule:
  - Definitely excluded: figure/table captions, code listings, maths, references, appendices
  - Conservatively included (until Dr. Aly confirms otherwise): direct quotes
"""
import re

with open('COMP_3018_Report.md') as f:
    lines = f.readlines()

# task boundaries
task3_start = task4_start = appendix_start = None
for i, line in enumerate(lines):
    if re.match(r'^#\s+1-\s+Task', line):
        task3_start = i
    elif re.match(r'^#\s+2-\s+Task', line):
        task4_start = i
    elif re.match(r'^#\s+3\.\s+Appendix', line):
        appendix_start = i

task3_text = ''.join(lines[task3_start:task4_start])
task4_text = ''.join(lines[task4_start:appendix_start])

def strip_word_equivalent(text):
    """What Word would count: everything visible except references/appendix/comments.
    Word does NOT strip captions or code blocks unless explicitly marked. Approximation."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # strip references section: from the heading onward (line-by-line)
    in_refs = False
    out = []
    for line in text.split('\n'):
        if re.match(r'^#{1,3}\s+.*[Rr]eferences', line):
            in_refs = True
            continue
        if in_refs:
            # don't exit; refs are the last thing in each task block here
            continue
        out.append(line)
    text = '\n'.join(out)
    # strip YAML metadata
    text = re.sub(r'^---.*?---', '', text, count=1, flags=re.DOTALL)
    # strip markdown formatting (so * and ** don't count as words but inner text does)
    text = re.sub(r'(?m)^#+\s*', '', text)
    text = re.sub(r'- \[.\]\s*', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[*_]{1,2}', '', text)
    return text

def strip_conservative(text):
    """User's rule: strip captions/code/maths/references/comments/LaTeX-envs;
    KEEP inline quotes (counted conservatively until Dr. Aly clarifies)."""
    text = re.sub(r'<!--.*?-->', '', text, flags=re.DOTALL)
    # LaTeX environments (figures, tables, lstlisting) -- removes captions inside too
    text = re.sub(r'\\begin\{[^}]*\}.*?\\end\{[^}]*\}', '', text, flags=re.DOTALL)
    text = re.sub(r'(?m)^\\[a-zA-Z].*$', '', text)
    # fenced code blocks
    text = re.sub(r'```.*?```', '', text, flags=re.DOTALL)
    text = re.sub(r'`[^`]+`', '', text)
    # maths
    text = re.sub(r'\$\$.*?\$\$', '', text, flags=re.DOTALL)
    text = re.sub(r'\$[^$]+\$', '', text)
    # images
    text = re.sub(r'!\[.*?\]\(.*?\)', '', text)
    text = re.sub(r'(?m)^>.*$', '', text)
    # strip references section (heading + bullets at same/lower level)
    in_refs = False
    ref_level = 0
    filtered = []
    for line in text.split('\n'):
        m = re.match(r'^(#{1,3})\s+', line)
        if m:
            level = len(m.group(1))
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
    # markdown formatting
    text = re.sub(r'(?m)^#+\s*', '', text)
    text = re.sub(r'- \[.\]\s*', '', text)
    text = re.sub(r'\[([^\]]+)\]\([^)]+\)', r'\1', text)
    text = re.sub(r'[*_]{1,2}', '', text)
    return text

def strip_best_case(text):
    """Conservative + remove inline quotes whose content is 15+ chars.
    Pair quotes left-to-right so short quotes like "skip" don't mis-pair with later quotes."""
    text = strip_conservative(text)
    def maybe_strip(m):
        content = m.group(1)
        return '' if len(content) >= 15 else m.group(0)
    text = re.sub(r'"([^"]*)"', maybe_strip, text)
    text = re.sub(r'“([^”]*)”', maybe_strip, text)
    return text

def strip_ultra(text):
    """Best-case + strip inline citations (Author, Year[, ...])."""
    text = strip_best_case(text)
    # inline citations: ( Capitalised-name ... year ... )
    text = re.sub(r'\([A-Z][^)]*?\b(19|20)\d{2}[a-z]?[^)]*?\)', '', text)
    return text

def report(label, text, limit):
    word_eq = len(strip_word_equivalent(text).split())
    conservative = len(strip_conservative(text).split())
    best_case = len(strip_best_case(text).split())
    ultra = len(strip_ultra(text).split())
    print(f"\n{label} (limit: {limit:,})")
    print(f"  Word-equivalent (visible text):    {word_eq:>5} words   {'OVER' if word_eq > limit else 'OK':>4} (Δ {word_eq - limit:+d})")
    print(f"  Conservative (user's rule):        {conservative:>5} words   {'OVER' if conservative > limit else 'OK':>4} (Δ {conservative - limit:+d})")
    print(f"  Best case (no quotes):             {best_case:>5} words   {'OVER' if best_case > limit else 'OK':>4} (Δ {best_case - limit:+d})")
    print(f"  Ultra (no quotes + no citations):  {ultra:>5} words   {'OVER' if ultra > limit else 'OK':>4} (Δ {ultra - limit:+d})")

print("=" * 70)
print("WORD COUNT VERIFICATION (per feedback_word_count.md)")
print("=" * 70)
report("TASK 3 (Lit Review)", task3_text, 1800)
report("TASK 4 (Programming Project)", task4_text, 2200)
print()
print("Note: 'Conservative' is the user's standing rule. 'Best case' assumes")
print("Dr. Aly confirms direct quotes don't count toward the limit.")
