import re

with open("docs-site/src/content/docs/release-notes.md", "r") as f:
    lines = f.readlines()

new_lines = []
in_breaking = False

for line in lines:
    if line.strip() == "### ⚠️ BREAKING CHANGES":
        new_lines.append(":::danger[BREAKING CHANGES]\n")
        in_breaking = True
    elif in_breaking and line.startswith("##"):
        new_lines.append(":::\n\n")
        new_lines.append(line)
        in_breaking = False
    else:
        new_lines.append(line)

# If the file ended while still in a breaking block
if in_breaking:
    new_lines.append(":::\n")

with open("docs-site/src/content/docs/release-notes.md", "w") as f:
    f.writelines(new_lines)
