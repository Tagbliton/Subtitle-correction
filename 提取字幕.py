def extract_text_from_srt(input_file, output_file):
    with open(input_file, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    text_lines = []
    for i in range(2, len(lines), 4):  # Skip the index and timestamp lines
        text_lines.append(lines[i].strip())

    with open(output_file, 'w', encoding='utf-8') as file:
        file.write('\n'.join(text_lines))

# 使用函数
extract_text_from_srt('2.srt', 'output.txt')