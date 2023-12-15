def deduplicate(src_file, dest_file):
    lines_seen = set()
    output_lines = []

    with open(src_file, "r", encoding="utf-8") as file:
        for line in file:
            stripped_line = line.strip()
            if (
                stripped_line == ""
                or stripped_line.startswith("#")
                or stripped_line not in lines_seen
            ):
                output_lines.append(line)
                if stripped_line != "":
                    lines_seen.add(stripped_line)

    with open(dest_file, "w", encoding="utf-8", newline="\n") as file:
        file.writelines(output_lines)


def get_info(src_file):
    with open(src_file, "r", encoding="utf-8") as f:
        lines = f.readlines()

    info = []
    flag_continue = False

    for line in lines:
        if line == "\n" or line.startswith("#"):
            info.append(line)
        elif line == "---\n":
            info.append(line)
            flag_continue = True
        elif flag_continue:
            info.append(line)
            if line == "...\n":
                flag_continue = False
        else:
            break

    return info


def sort(src_file, dest_file):
    info = get_info(src_file)

    # 跳过处理 THUOCL 词库
    if "thuocl" in src_file:
        return

    with open(src_file, "r", encoding="utf-8") as f:
        lines = f.readlines()[len(info) :]

    format_type = len(lines[0].split("\t"))

    # format_type == 2 时，排序「字	zi」此类，规则是按拼音排序
    # format_type == 3 时，排序「字	zi	1」此类，规则是按拼音+字频排序
    # 暂时不支持混排
    if format_type == 2:
        wait_to_write = []
        part_to_sort = []

        for line in lines:
            if line.startswith("#") or line == "\n":
                if part_to_sort:
                    sorted_lines = sorted(
                        part_to_sort,
                        key=lambda x: x.split("\t")[1]
                        if len(x.split("\t")) > 1
                        else "",
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
        with open(dest_file, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(info + wait_to_write)
    elif format_type == 3:
        wait_to_write = []
        part_to_sort = []

        for line in lines:
            if line.startswith("#") or line == "\n":
                if part_to_sort:
                    sorted_lines = sorted(
                        part_to_sort,
                        key=lambda x: (
                            x.split("\t")[1] if len(x.split("\t")) > 1 else "",
                            int(x.split("\t")[2])
                            if len(x.split("\t")) > 2 and x.split("\t")[2].isdigit()
                            else 0,
                        ),
                    )
                    wait_to_write += sorted_lines
                    part_to_sort.clear()
                wait_to_write.append(line)
                continue
            part_to_sort.append(line)

        if part_to_sort:
            wait_to_write += sorted(
                part_to_sort,
                key=lambda x: (
                    x.split("\t")[1] if len(x.split("\t")) > 1 else "",
                    int(x.split("\t")[2])
                    if len(x.split("\t")) > 2 and x.split("\t")[2].isdigit()
                    else 0,
                ),
            )
        with open(dest_file, "w", encoding="utf-8", newline="\n") as f:
            f.writelines(info + wait_to_write)


if __name__ == "__main__":
    import os
    import sys

    dicts_dir = os.path.join(os.path.abspath(os.path.dirname(sys.path[0])), "dicts")

    for root, _, files in os.walk(dicts_dir):
        for file in files:
            if file.endswith(".yaml"):
                file_path = os.path.join(root, file)
                print(f"Processing {file_path}")
                deduplicate(file_path, file_path)
                sort(file_path, file_path)

    print("Processing completed")
