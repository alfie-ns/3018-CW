#!/usr/bin/env python3
"""Show what gets stripped between conservative and best-case for Task 4."""
import re
from wc_compare import strip_conservative

with open('COMP_3018_Report.md') as f:
    lines = f.readlines()

task4_start = appendix_start = None
for i, line in enumerate(lines):
    if re.match(r'^#\s+2-\s+Task', line):
        task4_start = i
    elif re.match(r'^#\s+3\.\s+Appendix', line):
        appendix_start = i

task4_text = ''.join(lines[task4_start:appendix_start])
conservative = strip_conservative(task4_text)

# find every quoted segment of 15+ chars in the conservative output
matches = re.findall(r'"[^"]{15,}"', conservative) + re.findall(r'“[^”]{15,}”', conservative)
print(f"Total quoted segments (15+ chars): {len(matches)}")
print(f"Total words in those segments: {sum(len(m.split()) for m in matches)}\n")
print("First 25 segments:")
for i, m in enumerate(matches[:25], 1):
    wc = len(m.split())
    print(f"  [{i:>2}] ({wc:>3}w) {m[:120]}{'...' if len(m) > 120 else ''}")
