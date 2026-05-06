import re
import os

syllabus_path = r"c:\Users\barboza-salerno.1\Downloads\ED injury\new course\syllabus_text_from_docx.md"
out_dir = r"c:\Users\barboza-salerno.1\Downloads\ED injury\new course\website\labs"

if not os.path.exists(out_dir):
    os.makedirs(out_dir)

with open(syllabus_path, 'r', encoding='utf-8') as f:
    text = f.read()

# We want to match: **Week <num> \| <date> \|** <Title>
# Note: The pipes are escaped as \| in the text.
week_pattern = re.compile(r'\*\*Week\s+(\d+)\s+\\\|.*?\\\|\*\*\s*(.*)')

weeks_data = []

# Find all week headers
matches = list(week_pattern.finditer(text))

print(f"Found {len(matches)} weeks.")

for i, match in enumerate(matches):
    week_num = match.group(1)
    week_title = match.group(2).strip()
    
    start_idx = match.end()
    end_idx = matches[i+1].start() if i + 1 < len(matches) else len(text)
    
    content = text[start_idx:end_idx]
    
    # Now extract the Theme, Classroom Lab Demonstration, and Self-Graded Lab
    # Theme:
    theme_match = re.search(r'\*\*Theme:\s*(.*?)\*\*(.*?)(?=\*\*Required Readings\*\*|\*\*Classroom Lab Demonstration\*\*|$)', content, re.DOTALL)
    theme_title = ""
    theme_desc = ""
    if theme_match:
        theme_title = theme_match.group(1).strip()
        theme_desc = theme_match.group(2).strip()
        
    # Classroom Lab Demo:
    demo_match = re.search(r'\*\*Classroom Lab Demonstration\*\*(.*?)(?=\*\*Self-Graded Lab|\*\*ASSIGNMENT|$)', content, re.DOTALL | re.IGNORECASE)
    demo_content = ""
    if demo_match:
        demo_content = demo_match.group(1).strip()
        
    # Self-Graded Lab:
    lab_match = re.search(r'\*\*Self-Graded Lab[^\n]*\*\*(.*?)(?=\*\*ASSIGNMENT|\*\*Week|SPRING BREAK|SECTION|$)', content, re.DOTALL | re.IGNORECASE)
    lab_content = ""
    lab_title = ""
    lab_title_match = re.search(r'\*\*Self-Graded Lab:\s*(.*?)\*\*', content, re.IGNORECASE)
    if lab_title_match:
        lab_title = lab_title_match.group(1).strip()
    
    if demo_content or lab_content:
        # Build QMD content
        clean_title = week_title.replace("\\'", "'").replace('\\"', '"')
        qmd = f"---\ntitle: \"Week {week_num}: {clean_title}\"\n---\n\n"
        
        if theme_title:
            qmd += f"## Theme: {theme_title}\n\n{theme_desc}\n\n"
            
        if demo_content:
            qmd += f"## Classroom Lab Demonstration\n\n{demo_content}\n\n"
            
        if lab_content:
            qmd += f"## Self-Graded Lab\n\n"
            if lab_title:
                qmd += f"### {lab_title}\n\n"
            qmd += f"{lab_content}\n\n"
            
        out_file = os.path.join(out_dir, f"week{int(week_num):02d}.qmd")
        with open(out_file, "w", encoding="utf-8") as out_f:
            out_f.write(qmd)
        print(f"Generated {out_file}")
