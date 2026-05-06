import re
import os

with open('../syllabus_text_utf8.txt', 'r', encoding='utf-8') as f:
    lines = f.readlines()

schedule_start = 0
schedule_end = 0
for i, line in enumerate(lines):
    if "Course Schedule" in line and i > 200:
        schedule_start = i
    if "Alignment of Competencies with Assessments" in line:
        schedule_end = i
        break

schedule_lines = lines[schedule_start:schedule_end]

md_content = '''# Course Schedule

*Readings marked * are available as open-access PDFs via Carmen. Schedule is subject to adjustment; changes will be announced via Carmen.*

'''

for line in schedule_lines:
    line = line.strip()
    if not line:
        continue
    
    if line.startswith("SECTION"):
        md_content += f"\n## {line}\n\n---\n\n"
        continue
        
    if line.startswith("Week ") or line.startswith("SPRING BREAK"):
        parts = [p.strip() for p in line.split("|")]
        title = " | ".join(parts)
        md_content += f"\n### {title}\n\n"
        continue
        
    if line.startswith("Theme:") or line.startswith("Required Readings") or line.startswith("Classroom Lab Demonstration") or line.startswith("Self-Graded Lab:"):
        md_content += f"**{line}**\n\n"
    elif line.startswith("Legal Focus:") or line.startswith("Health Focus:") or line.startswith("Data:") or line.startswith("R Code:") or line.startswith("check_answer()") or line.startswith("Reflection"):
        parts = line.split(":", 1)
        if len(parts) > 1:
            md_content += f"- **{parts[0]}:** {parts[1]}\n"
        else:
            md_content += f"- {line}\n"
    elif "Assignment" in line and "Due" in line:
        md_content += f"\n> **{line}**\n\n"
    elif "ASSIGNMENT" in line and "DUE" in line:
        md_content += f"\n> **{line}**\n\n"
    elif "Assignment" in line and "Check-In" in line:
        md_content += f"\n> *{line}*\n\n"
    else:
        if "Course Schedule" not in line and "Readings marked" not in line:
            md_content += f"{line}\n\n"

with open('schedule.qmd', 'w', encoding='utf-8') as f:
    f.write(md_content)
