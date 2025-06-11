def split_file(input_file_path, output_prefix, max_lines=250):
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_lines = len(lines)
    num_files = (total_lines + max_lines - 1) // max_lines  # 计算需要多少个文件

    for i in range(num_files):
        start_line = i * max_lines
        end_line = min(start_line + max_lines, total_lines)
        output_file_path = f"{output_prefix}_{i + 1}.txt"

        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            out_file.writelines(lines[start_line:end_line])

        print(f"Created {output_file_path} with {end_line - start_line} lines.")


# 使用示例
input_file_path = 'output.txt'  # 输入文件路径
output_prefix = 'results'  # 输出文件的前缀名
split_file(input_file_path, output_prefix, 500)

