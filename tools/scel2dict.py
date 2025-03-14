# Usage: python scel2dict.py -i <input_file> -o <output_file> -u <url>
# License: GPL-3.0
# Description: Convert Sogou SCEL dictionary to Rime dictionary format
# Author:
# - LufsX
# Reference Code:
# - https://github.com/studyzy/imewlconverter/blob/master/src/ImeWlConverterCore/IME/SougouPinyinScel.cs
# Thanks to:
# - https://github.com/nopdan
# - https://github.com/studyzy/imewlconverter
# - https://github.com/studyzy/imewlconverter/issues/275#issuecomment-1911748289

import argparse
import os
import requests
import struct
import sys
import tempfile
import time
import urllib


class SougouScelReader:
    """搜狗细胞词库解析"""

    def __init__(self, path):
        self.path = path
        self.py_dic = {}
        self.words = []

    def read_scel_info(self):
        """读取词库基本信息"""
        info = {}
        with open(self.path, "rb") as f:
            # 读取词条数量
            f.seek(0x124)
            count_word = struct.unpack("<I", f.read(4))[0]
            info["CountWord"] = count_word

            # 读取词库名称
            f.seek(0x130)
            info["Name"] = self._read_scel_field_text(f, 64)

            # 读取词库类型
            f.seek(0x338)
            info["Type"] = self._read_scel_field_text(f, 64)

            # 读取词库描述
            f.seek(0x540)
            info["Info"] = self._read_scel_field_text(f, 1024)

            # 读取词库示例
            f.seek(0xD40)
            info["Sample"] = self._read_scel_field_text(f, 1024)

        return info

    def _read_scel_field_text(self, file_obj, length=64):
        """读取词库字段文本"""
        bytes_data = file_obj.read(length)
        text = bytes_data.decode("utf-16-le", errors="ignore")
        end = text.find("\0")
        if end >= 0:
            return text[:end]
        return text

    def read_scel(self):
        """读取整个 SCEL 词库文件"""
        with open(self.path, "rb") as f:
            # 词条数量
            f.seek(0x120)
            dict_len = struct.unpack("<I", f.read(4))[0]

            # 拼音表的长度
            f.seek(0x1540)
            py_dic_len = struct.unpack("<I", f.read(4))[0]

            # 读取拼音表
            for _ in range(py_dic_len):
                idx = struct.unpack("<H", f.read(2))[0]
                size = struct.unpack("<H", f.read(2))[0]
                py_bytes = f.read(size)
                py = py_bytes.decode("utf-16-le")
                self.py_dic[idx] = py

            # 读取词条
            for _ in range(dict_len):
                try:
                    self.words.extend(self._read_a_pinyin_word(f))
                except Exception as e:
                    print(f"Error reading word: {e}", file=sys.stderr)

        return self.words

    def _read_a_pinyin_word(self, f):
        """读取一个拼音对应的多个词"""
        num_bytes = f.read(4)
        same_py_count = num_bytes[0] + num_bytes[1] * 256
        count = num_bytes[2] + num_bytes[3] * 256

        # 读取拼音
        py_bytes = f.read(count)
        word_py = []
        for i in range(count // 2):
            key = py_bytes[i * 2] + py_bytes[i * 2 + 1] * 256
            if key < len(self.py_dic):
                word_py.append(self.py_dic[key])
            else:
                word_py.append(chr(key - len(self.py_dic) + 97))

        words = []
        # 读取同音词
        for s in range(same_py_count):
            # 词组字节数
            num = f.read(2)
            hz_byte_count = num[0] + num[1] * 256

            # 读取词组
            word_bytes = f.read(hz_byte_count)
            word = word_bytes.decode("utf-16-le")

            # 读取但忽略未知数据
            unknown1 = struct.unpack("<H", f.read(2))[0]  # 通常是10
            unknown2 = struct.unpack("<I", f.read(4))[0]  # 可能与词频相关

            # 词条数据
            words.append({"word": word, "pinyin": word_py, "freq": 10})  # 默认频率

            # 跳过剩余的未知字节
            f.read(6)

        return words


class SougouScelDownloader:
    """搜狗细胞词库下载器"""

    def __init__(self, url=None):
        self.url = url

    def download(self, url=None, output_path=None):
        """下载词库文件"""
        temp_flag = [False, None, None]

        url = url or self.url
        if not url:
            raise ValueError("No URL provided")

        # 下载文件
        print(f"Downloading {url} to {output_path}")
        headers = {
            "User-Agent": "Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Mobile Safari/537.36 Edg/134.0.0.0"
        }
        response = requests.get(url, headers=headers, stream=True)
        response.raise_for_status()

        # 如果没有指定输出路径，使用 URL 中的文件名
        if not output_path:
            # 创建临时文件
            temp_dir = tempfile.gettempdir()
            timestamp = int(time.time())
            # 尝试从 Content-Disposition 获取文件名
            if "Content-Disposition" in response.headers:
                disposition = response.headers["Content-Disposition"]
                if "filename=" in disposition:
                    filename = disposition.split("filename=")[1].strip('"')
                    # UTF-8 解码
                    filename = filename.encode("latin1").decode("utf-8")
                    name, ext = os.path.splitext(filename)
                    output_path = os.path.join(temp_dir, f"{name}_{timestamp}{ext}")
            else:
                # 若无，则使用 URL 中的文件名
                parsed_url = urllib.parse.urlparse(url)
                filename = os.path.basename(parsed_url.path)
                if not filename.endswith(".scel"):
                    filename += f"_{timestamp}.scel"
                output_path = os.path.join(temp_dir, filename)
            temp_flag[0], temp_flag[1], temp_flag[2] = True, temp_dir, output_path

        # 保存文件
        with open(output_path, "wb") as f:
            for chunk in response.iter_content(chunk_size=8192):
                f.write(chunk)

        return output_path, temp_flag


class RimeDictConverter:
    """转换为 Rime 词典格式"""

    @staticmethod
    def convert_to_rime(words, output_file, name=None):
        if name is None:
            name = "Converted Sogou Dictionary"

        # 写入 Rime 词典头部
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(f"# Rime dictionary\n")
            f.write(f"# encoding: utf-8\n")
            f.write(f"# {name}\n\n")
            f.write(
                f"---\nname: {os.path.basename(output_file).replace('.dict.yaml', '')}\n"
            )
            f.write(f"version: \"{time.strftime('%Y-%m-%d')}\"\n")
            f.write(f"sort: by_weight\n")
            f.write(f"...\n\n")

            # 写入词条
            for word_info in words:
                word = word_info["word"]
                pinyin = " ".join(word_info["pinyin"])
                freq = word_info.get("freq", 10)
                f.write(f"{word}\t{pinyin}\t{freq}\n")

        print(f"Converted {len(words)} words to {output_file}")


def main():
    parser = argparse.ArgumentParser(description="搜狗细胞词库转换工具")
    parser.add_argument("-i", "--input", help="输入的 SCEL 文件路径")
    parser.add_argument("-o", "--output", help="输出的 RIME 词典文件路径")
    parser.add_argument("-u", "--url", help="搜狗词库下载 URL")
    parser.add_argument("-n", "--name", help="词典名称")

    args = parser.parse_args()

    # 检查参数
    if not args.input and not args.url:
        parser.error("需要提供输入文件路径或下载 URL")

    # 如果提供了 URL，先下载
    if args.url:
        downloader = SougouScelDownloader()
        try:
            if args.input:
                scel_file, temp_flag = downloader.download(args.url, args.input)
            else:
                scel_file, temp_flag = downloader.download(args.url)
        except Exception as e:
            print(f"下载失败: {e}")
            return 1
    else:
        scel_file = args.input

    # 设置输出文件名
    if not args.output:
        output_file = os.path.splitext(os.path.basename(scel_file))[0] + ".dict.yaml"
    else:
        output_file = args.output
        if not output_file.endswith(".dict.yaml"):
            output_file += ".dict.yaml"

    # 读取 SCEL 文件
    try:
        reader = SougouScelReader(scel_file)
        info = reader.read_scel_info()
        print(f"词库名称: {info.get('Name')}")
        print(f"词库类型: {info.get('Type')}")
        print(f"词条数量: {info.get('CountWord')}")
        print(f"词库描述: {info.get('Info')}")
        print(
            f"词库示例: {info.get('Sample').replace('\u3000', '').replace('\r', '|')}"
        )

        words = reader.read_scel()
        print(f"实际解析词条: {len(words)}")
    except Exception as e:
        print(f"读取词库失败: {e}")
        return 1

    # 转换为 RIME 词典
    try:
        name = args.name or info.get("Name")
        RimeDictConverter.convert_to_rime(words, output_file, name)
    except Exception as e:
        print(f"转换失败: {e}")
        return 1

    # 如果使用了临时文件，删除它
    if temp_flag[0] and os.path.exists(temp_flag[2]):
        os.remove(temp_flag[2])

    return 0


if __name__ == "__main__":
    # 测试参数
    # sys.argv = [
    #     "scel2dict.py",
    #     "-i",
    #     "test.scel",
    #     "-o",
    #     "test.dict.yaml",
    #     "-u",
    #     "https://pinyin.sogou.com/d/dict/download_cell.php?id=4&name=%E7%BD%91%E7%BB%9C%E6%B5%81%E8%A1%8C%E6%96%B0%E8%AF%8D",
    # ]
    sys.exit(main())
