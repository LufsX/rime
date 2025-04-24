import os, re, requests, sys

workDir = os.path.abspath(os.path.dirname(sys.path[0]))

# iDvel/rime-ice 仓库词库更新
update_url = {
    os.path.join(
        "dicts", "simp.dict.yaml"
    ): "https://github.com/iDvel/rime-ice/raw/main/cn_dicts/8105.dict.yaml",
    os.path.join(
        "opencc", "emoji_word.txt"
    ): "https://github.com/iDvel/rime-ice/raw/main/opencc/emoji.txt",
}

for path, link in update_url.items():
    try:
        response = requests.get(link)
        if response.status_code == 200:
            with open(os.path.join(workDir, path), "wb") as f:
                f.write(response.content)
            print(f"[Dict] Update {path} successful")
    except Exception as e:
        print(f"[Dict] {path} error: {str(e)}")

# 萌娘百科词库更新
moegirl_github_api = "https://api.github.com/repos/outloudvi/mw2fcitx/releases/latest"
moegirl_dict_path = os.path.join("dicts", "moegirl.dict.yaml")

try:
    response = requests.get(moegirl_github_api)
    if response.status_code == 200:
        moegirl_assets = response.json()["assets"]
        for asset in moegirl_assets:
            if asset["name"] == "moegirl.dict.yaml":
                moegirl_link = asset["browser_download_url"]
                infoStr = f"""# Rime dictionary
# encoding: utf-8
# source: {moegirl_link}
"""
                moegirl_response = requests.get(moegirl_link)
                if moegirl_response.status_code == 200:
                    with open(os.path.join(workDir, moegirl_dict_path), "wb") as f:
                        f.write(infoStr.encode("utf-8"))
                        f.write(moegirl_response.content)
                    print(f"[Dict] Update {moegirl_dict_path} successful")
                break
except Exception as e:
    print(f"[Dict] {moegirl_dict_path} error: {str(e)}")

# 去除 opencc/emoji_word.txt 非中文字符
pattern = re.compile(r"^[\u4e00-\u9fa5]+$")
emoji_path = os.path.join(workDir, "opencc", "emoji_word.txt")

with open(emoji_path, "r", encoding="utf-8") as f:
    text = f.read()

lines = text.split("\n")

with open(emoji_path, "w", encoding="utf-8", newline="\n") as outFile:
    for line in lines:
        if line:
            parts = line.split("\t")
            if pattern.match(parts[0]):
                outFile.write(line + "\n")

print("[Emoji](OpenCC) Clear non-Chinese characters successfully")
