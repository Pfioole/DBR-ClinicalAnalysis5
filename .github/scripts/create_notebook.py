import nbformat
import sys
import os
import re
import yaml

title = sys.argv[1]
body = sys.argv[2]

# Extract TLG ID and title
match = re.match(r"\[TLG\]\s*-\s*(.*?)\s*-\s*(.*)", title)
if not match:
    print("❌ Title must follow format: [TLG] - <ID> - <Title>")
    sys.exit(1)

tlg_id = match.group(1).strip()
tlg_title = match.group(2).strip()

# Extract type from issue body
type_match = re.search(r"### Type\s*\n(.+)", body)
if not type_match:
    print("❌ Could not extract TLG type (Table/Listing/Figure).")
    sys.exit(1)

tlg_type = type_match.group(1).strip().lower()

# Decide subdirectory
if "table" in tlg_type:
    subfolder = "tables"
elif "listing" in tlg_type:
    subfolder = "listings"
elif "figure" in tlg_type:
    subfolder = "figures"
else:
    subfolder = "misc"

# Define path
folder_path = f"programs/tfl/{subfolder}"
os.makedirs(folder_path, exist_ok=True)
notebook_path = f"{folder_path}/{tlg_id}_{tlg_title.replace(' ', '_')}.ipynb"

# Create notebook
nb = nbformat.v4.new_notebook()
nb.cells.append(nbformat.v4.new_markdown_cell(f"# {tlg_title}\n\n**TLG ID:** {tlg_id}\n**Type:** {tlg_type.title()}"))
nbformat.write(nb, notebook_path)

print(f"✅ Notebook created at: {notebook_path}")
