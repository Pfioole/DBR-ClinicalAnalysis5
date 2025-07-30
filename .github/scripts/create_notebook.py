import sys
import os
import re
import nbformat
from nbformat.v4 import new_notebook, new_markdown_cell, new_code_cell

title = sys.argv[1]
body = sys.argv[2]

match = re.match(r"\[TLG\]\s*-\s*(.*?)\s*-\s*(.*)", title)
tlg_id = match.group(1).strip()
tlg_title = match.group(2).strip()

def extract(label):
    m = re.search(rf"\*\*{label}\*\*:\s*@?(\w+)", body)
    return m.group(1) if m else ""

programmer = extract("Programmer")
qc = extract("QC Reviewer")

folder = "programs/misc"
filename = f"{folder}/{tlg_id.replace('.', '_')}_{tlg_title.replace(' ', '_')}.ipynb"
os.makedirs(folder, exist_ok=True)

nb = new_notebook(cells=[
    new_markdown_cell(f"# 📊 TLG Notebook\n- **TLG ID**: {tlg_id}\n- **Title**: {tlg_title}\n- **Programmer**: @{programmer}\n- **QC Reviewer**: @{qc}"),
    new_code_cell("# Start your analysis\n# spark.read.format('delta').table('adam.adsl')")
])

with open(filename, 'w') as f:
    nbformat.write(nb, f)
print(f"Notebook created: {filename}")

