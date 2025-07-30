import nbformat
import sys
import os
import re

title = sys.argv[1]
body = sys.argv[2]

# Extract TLG ID and title
match = re.match(r"\[TLG\]\s*-\s*(.*?)\s*-\s*(.*)", title)
if not match:
    print("❌ Title must follow format: [TLG] - <ID> - <Title>")
    sys.exit(1)

tlg_id = match.group(1).strip()
tlg_title = match.group(2).strip()

# Extract type
type_match = re.search(r"### Type\s*\n(.+)", body)
tlg_type = type_match.group(1).strip().lower() if type_match else "misc"

# Extract programmer and reviewer
prog_match = re.search(r"### Programmer GitHub handle\s*\n(.+)", body)
qc_match = re.search(r"### QC Reviewer GitHub handle\s*\n(.+)", body)
programmer = prog_match.group(1).strip() if prog_match else "N/A"
qc_reviewer = qc_match.group(1).strip() if qc_match else "N/A"

# Determine subfolder
if "table" in tlg_type:
    subfolder = "tables"
elif "listing" in tlg_type:
    subfolder = "listings"
elif "figure" in tlg_type:
    subfolder = "figures"
else:
    subfolder = "misc"

# File path
folder_path = f"programs/tfl/{subfolder}"
os.makedirs(folder_path, exist_ok=True)
safe_title = re.sub(r'[^\w\d_-]', '_', tlg_title)
notebook_path = f"{folder_path}/{tlg_id}_{safe_title}.ipynb"

# Load template
if not os.path.exists(template_path):
    print(f"❌ Template not found at {template_path}")
    sys.exit(1)
template_path = "templates/tlg_notebook_template.ipynb"
nb = nbformat.read(template_path, as_version=4)

# Replace placeholders in first markdown cell
for cell in nb.cells:
    if cell.cell_type == "markdown":
        cell.source = cell.source.replace("{{TLG_ID}}", tlg_id)
        cell.source = cell.source.replace("{{TITLE}}", tlg_title)
        cell.source = cell.source.replace("{{PROGRAMMER}}", f"@{programmer}")
        cell.source = cell.source.replace("{{QC_REVIEWER}}", f"@{qc_reviewer}")

# Write final notebook
nbformat.write(nb, notebook_path)
print(f"✅ Created notebook at {notebook_path}")
