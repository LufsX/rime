import requests, os, sys

workDir = os.path.abspath(os.path.dirname(sys.path[0]))

update_url = {
    os.path.join(
        workDir, "dicts", "simp.dict.yaml"
    ): "https://github.com/iDvel/rime-ice/raw/main/cn_dicts/8105.dict.yaml",
    os.path.join(
        workDir, "opencc", "emoji_word.txt"
    ): "https://github.com/iDvel/rime-ice/raw/main/opencc/emoji.txt",
}

for path, link in update_url.items():
    try:
        response = requests.get(link)
        if response.status_code == 200:
            with open(path, "wb") as f:
                f.write(response.content)
    except Exception as e:
        print(f"{path} 报错: {str(e)}")

print("Update successful")
