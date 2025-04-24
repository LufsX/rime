from scel2dict import SougouScelReader, SougouScelDownloader
import os
import sys
import urllib.parse
import time
import requests
import re

workDir = os.path.abspath(os.path.dirname(sys.path[0]))
dict_list = {
    "sogou_net.dict.yaml": {"id": 4, "name": "网络流行新词", "increment": True},
    "sogou_minecraft.dict.yaml": {
        "id": 124017,
        "name": "Minecraft最全词库（更新至1.16.2）",
    },
    "sogou_touhou.dict.yaml": {"id": 50826, "name": "【东方project】"},
}


# 从网页提取更新日期
def extract_update_date(dict_id):
    url = f"https://pinyin.sogou.com/dict/detail/index/{dict_id}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
    }
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        if not response.text:
            return None

        # 正则匹配更新日期
        pattern = r"<div>更&nbsp;&nbsp;&nbsp;新：(\d{4}-\d{2}-\d{2}) (\d{2}:\d{2}:\d{2})</div>"
        match = re.search(pattern, response.text)

        if match:
            return match.group(1)
        return None
    except Exception as e:
        print(f"[Dict](Sogou) Failed to obtain the vocabulary update time: {str(e)}")
        return None


# 转换为 Rime 词典格式的函数
def convert_to_rime(words, output_file, id, update_date=None, increment=False):
    if increment:
        # 增量更新处理
        existing_words = set()
        existing_lines = []
        flag = False

        # 如果文件已存在，读取现有内容
        if os.path.exists(output_file):
            with open(output_file, "r", encoding="utf-8") as f:
                lines = f.readlines()
                # 分离词条
                for line in lines:
                    if flag or line == "...\n":
                        existing_lines.append(line)
                        flag = True

        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Rime dictionary\n")
            f.write(f"# encoding: utf-8\n")
            f.write(f"# source: https://pinyin.sogou.com/dict/detail/index/{id}\n\n")
            f.write(
                f"---\nname: {os.path.basename(output_file).replace('.dict.yaml', '').replace('sogou_', '')}\n"
            )
            version_date = update_date if update_date else time.strftime("%Y-%m-%d")
            f.write(f'version: "{version_date}"\n')
            f.write(f"sort: by_weight\n")

            # 写回现有词条
            for line in existing_lines:
                f.write(line)

            # 添加新词条
            new_count = 0
            for word_info in words:
                word = word_info["word"]
                # 过滤词条
                if re.search(r"[a-zA-Z]", word):
                    continue
                # 只加新增的词条
                if word not in existing_words:
                    pinyin = " ".join(word_info["pinyin"])
                    f.write(f"{word}\t{pinyin}\n")
                    new_count += 1
                    existing_words.add(word)

        print(
            f"[Dict](Sogou) Incremental update: Added {new_count} new entries to {output_file}"
        )
    else:
        # 写入 Rime 词典头部
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Rime dictionary\n")
            f.write(f"# encoding: utf-8\n")
            f.write(f"# source: https://pinyin.sogou.com/dict/detail/index/{id}\n\n")
            f.write(
                f"---\nname: {os.path.basename(output_file).replace('.dict.yaml', '').replace('sogou_', '')}\n"
            )
            version_date = update_date if update_date else time.strftime("%Y-%m-%d")
            f.write(f'version: "{version_date}"\n')
            f.write(f"sort: by_weight\n")
            f.write(f"...\n\n")

            # 写入词条
            for word_info in words:
                word = word_info["word"]
                pinyin = " ".join(word_info["pinyin"])
                f.write(f"{word}\t{pinyin}\n")

    print(
        f"[Dict](Sogou) Translation completed: {len(words)} entries saved to {output_file}"
    )


for key in dict_list:
    info = dict_list[key]
    dict_id = info["id"]
    dict_name = info["name"]
    dict_increment = info.get("increment", False)

    print(f"[Dict](Sogou) Processing: {dict_name} (ID: {dict_id})")

    # 获取词库网页内容并提取更新日期
    update_date = extract_update_date(dict_id)
    if update_date:
        print(f"[Dict](Sogou) Dict Update Date: {update_date}")

    # 构建URL
    url = f"https://pinyin.sogou.com/d/dict/download_cell.php?id={dict_id}&name={urllib.parse.quote(dict_name)}"

    # 输出路径
    output_path = os.path.join(workDir, "dicts", key)

    # 确保输出目录存在
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    try:
        # 下载词库
        downloader = SougouScelDownloader()
        scel_file, temp_flag = downloader.download(url)

        # 读取词库
        reader = SougouScelReader(scel_file)
        dict_info = reader.read_scel_info()
        print(f"[Dict](Sogou) Dict Name: {dict_info.get('Name')}")
        print(f"[Dict](Sogou) Count: {dict_info.get('CountWord')}")

        words = reader.read_scel()
        print(f"[Dict](Sogou) Actual Count: {len(words)}")

        # 转换为 RIME 词典，传递提取的更新日期
        convert_to_rime(words, output_path, dict_id, update_date=update_date, increment=dict_increment)
        print(f"[Dict](Sogou) Saved to: {output_path}")

        # 清理临时文件
        if temp_flag[0] and os.path.exists(temp_flag[2]):
            os.remove(temp_flag[2])

    except Exception as e:
        print(f"[Dict](Sogou) Failed to update dict {dict_name}: {str(e)}")
        continue

print("[Dict](Sogou) All dict update completed!")
