import os, sys, re, datetime
from pypinyin import pinyin, Style

workDir = os.path.abspath(os.path.dirname(sys.path[0]))
pattern = re.compile(r"^[\u4e00-\u9fa5]+$")

# now = datetime.datetime.now().strftime("%Y-%m-%d")
# dateStr = now.strftime("%Y-%m-%d")
infoStr = f"""# Rime dictionary
# encoding: utf-8
# source: https://github.com/iDvel/rime-ice/blob/main/opencc/emoji.txt

---
name: emoji
version: "{datetime.datetime.now().strftime("%Y-%m-%d")}"
sort: by_weight
...

"""

with open(
    os.path.join(workDir, "opencc", "emoji_word.txt"), "r", encoding="utf-8"
) as f:
    text = f.read()

lines = text.split("\n")


with open(
    os.path.join(workDir, "dicts", "emoji.dict.yaml"),
    "w",
    encoding="utf-8",
    newline="\n",
) as outFile:
    outFile.write(infoStr)
    for line in lines:
        if line:
            parts = line.split("\t")
            # emoji = parts[1].strip().split(" ")[-1]
            name = parts[0].strip().split(" ")[-1]
            pinyin_name = " ".join([p[0] for p in pinyin(name, style=Style.NORMAL)])
            if pattern.match(name):
                # print(f"{name}\t{pinyin_name}")
                outFile.write(f"{name}\t{pinyin_name}\n")

print("Emoji to dictionary successfully")
