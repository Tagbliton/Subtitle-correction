from config import client, system_prompt
import json



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




def read_file_to_variable(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        A = file.read()
    return A









#ali
# def run1(index):
#     file = f"results_{index}"
#     text = read_file_to_variable(f"{file}.txt")
#     user_prompt = f"{role}\n以下为输入内容：\n{text}"
#
#     reasoning_content = ""  # 定义完整思考过程
#     answer_content = ""  # 定义完整回复
#     is_answering = False  # 判断是否结束思考过程并开始回复
#
#     completion = client.chat.completions.create(
#         model="deepseek-chat",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
#         messages=[
#             {'role': 'system', 'content': system_prompt},
#             {'role': 'user', 'content': user_prompt}
#         ],
#         stream=True,
#         response_format={'type': 'json_object'}
#     )
#
#     print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")
#
#     for chunk in completion:
#         # 如果chunk.choices为空，则打印usage
#         if not chunk.choices:
#             print("\nUsage:")
#             print(chunk.usage)
#         else:
#             delta = chunk.choices[0].delta
#             # 打印思考过程
#             if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
#                 print(delta.reasoning_content, end='', flush=True)
#                 reasoning_content += delta.reasoning_content
#             else:
#                 # 开始回复
#                 if delta.content != "" and is_answering == False:
#                     print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
#                     is_answering = True
#                 # 打印回复过程
#                 print(delta.content, end='', flush=True)
#                 answer_content += delta.content
#
#     results = f"Reasoning Content:\n{reasoning_content}\n\nAnswer Content:\n{answer_content}"
#
#     with open(f'{file}修改.txt', 'w', encoding='utf-8') as file:
#         file.write(results)
#
#     print(f"\n内容已成功写入 {file}.txt 文件。")
#     return f"\n已成功写入 {file}.txt 文件。", reasoning_content, answer_content




#deepseek
def run(index, cut_lines):
    file = f"results_{index}"
    user_prompt = read_file_to_variable(f"{file}.txt")


    response = client.chat.completions.create(
        model="deepseek-chat",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
        messages=[
            {'role': 'system', 'content': system_prompt(index, cut_lines)},
            {'role': 'user', 'content': user_prompt}
        ],
        stream=False,
        response_format={'type': 'json_object'}
    )

    results = json.loads(response.choices[0].message.content)

    before = results['before']

    # 2. 遍历这个字典的键和值
    print("--- 'before' 中的序号和内容 ---")
    before_lines = ""
    for key, value in before.items():
        before_lines = f"{before_lines}{key}: {value}\n"
    print(before_lines)



    after = results['after']

    # 2. 遍历这个字典的键和值
    print("--- 'before' 中的序号和内容 ---")
    after_lines = ""
    for key, value in after.items():
        after_lines = f"{after_lines}{key}: {value}\n"
    print(after_lines)

    print(f"\n内容已成功写入 {file}.txt 文件。")
    return f"\n已成功写入 {file}.txt 文件。", before_lines, after_lines
