def extract_text_from_srt(input_file):
    output_file='output.txt'
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text_lines = []
    for i in range(2, len(lines), 4):  # Skip the index and timestamp lines
        text_lines.append(lines[i].strip())

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(text_lines))

    return "字幕文本已提取至output.txt", "output.txt"



def split_file(max_lines):
    input_file_path = "output.txt"
    output_prefix = "results"
    with open(input_file_path, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    total_lines = len(lines)
    num_files = (total_lines + max_lines - 1) // max_lines  # 计算需要多少个文件
    message= ""

    for i in range(num_files):
        start_line = i * max_lines
        end_line = min(start_line + max_lines, total_lines)
        output_file_path = f"{output_prefix}_{i + 1}.txt"

        with open(output_file_path, 'w', encoding='utf-8') as out_file:
            out_file.writelines(lines[start_line:end_line])

        message = f"{message}Created {output_file_path} with {end_line - start_line} lines.\n"


    return f"发现{total_lines}条字幕.\n{message}"


def action(input_file, max_lines):
    output1, output2=extract_text_from_srt(input_file)
    output3=split_file(max_lines)

    return (f"{output1}\n{output3}", output2)