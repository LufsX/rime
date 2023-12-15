import os, sys, re

workDir = os.path.abspath(os.path.dirname(sys.path[0]))
pattern = re.compile(r"^[\u4e00-\u9fa5]+$")

with open(
    os.path.join(workDir, "opencc", "emoji_word.txt"), "r", encoding="utf-8"
) as f:
    text = f.read()

lines = text.split("\n")

with open(
    os.path.join(workDir, "opencc", "emoji_word.txt"),
    "w",
    encoding="utf-8",
    newline="\n",
) as outFile:
    for line in lines:
        if line:
            parts = line.split("\t")
            if pattern.match(parts[0]):
                outFile.write(line + "\n")

print("Clear non-Chinese characters successfully")
