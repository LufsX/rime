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

    with open(dest_file, "w", encoding="utf-8") as file:
        file.writelines(output_lines)




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
