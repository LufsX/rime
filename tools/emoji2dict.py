import os, sys, re, datetime
from pypinyin import pinyin, Style

workDir = os.path.abspath(os.path.dirname(sys.path[0]))
pattern = re.compile(r"^[\u4e00-\u9fa5]+$")

with open(
    os.path.join(workDir, "opencc", "emoji_word.txt"), "r", encoding="utf-8"
) as f:
    text = f.read()

lines = text.split("\n")


def generate_dict_content():
    infoStr = f"""# Rime dictionary
# encoding: utf-8
# source: https://github.com/iDvel/rime-ice/blob/main/opencc/emoji.txt

---
name: emoji
version: "{datetime.datetime.now().strftime("%Y-%m-%d")}"
sort: by_weight
...
"""
    content = [infoStr]
    for line in lines:
        if line:
            parts = line.split("\t")
            name = parts[0].strip().split(" ")[-1]
            pinyin_name = " ".join([p[0] for p in pinyin(name, style=Style.NORMAL)])
            if pattern.match(name):
                content.append(f"{name}\t{pinyin_name}\n")
    return "".join(content)


new_content = generate_dict_content()

# 按拼音排序
lines = new_content.split("\n")
wait_to_write = []
part_to_sort = []

for line in lines:
    if line.startswith("#") or line == "\n":
        if part_to_sort:
            sorted_lines = sorted(
                part_to_sort,
                key=lambda x: x.split("\t")[1] if len(x.split("\t")) > 1 else "",
            )
            wait_to_write += sorted_lines
            part_to_sort.clear()
        wait_to_write.append(line)
        continue
    part_to_sort.append(line)

if part_to_sort:
    wait_to_write += sorted(
        part_to_sort,
        key=lambda x: x.split("\t")[1] if len(x.split("\t")) > 1 else "",
    )

sorted_content = "\n".join(wait_to_write) + "\n"

dict_path = os.path.join(workDir, "dicts", "emoji.dict.yaml")
if os.path.exists(dict_path):
    with open(dict_path, "r", encoding="utf-8") as existing_file:
        existing_content = existing_file.read()
else:
    existing_content = ""

temp_sorted_content = []
for line in sorted_content.splitlines():
    if not line.startswith("version:"):
        temp_sorted_content.append(line)
temp_sorted_content = "\n".join(temp_sorted_content)

temp_existing_content = []
for line in existing_content.splitlines():
    if not line.startswith("version:"):
        temp_existing_content.append(line)
temp_existing_content = "\n".join(temp_existing_content)

if temp_sorted_content != temp_existing_content:
    with open(dict_path, "w", encoding="utf-8", newline="\n") as outFile:
        outFile.write(sorted_content)
    print("[Emoji] Emoji to dictionary successfully")
else:
    print("[Emoji] No changes detected, version not updated")
