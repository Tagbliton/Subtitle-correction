from config import client, role, read_file_to_variable




file="results_7"
role=role
text=read_file_to_variable(f"{file}.txt")





reasoning_content = ""  # 定义完整思考过程
answer_content = ""     # 定义完整回复
is_answering = False   # 判断是否结束思考过程并开始回复




completion = client.chat.completions.create(
    model="deepseek-r1-0528",  # 此处以 deepseek-r1 为例，可按需更换模型名称。
    messages=[
        {'role': 'system', 'content': role},
        {'role': 'user', 'content': text}
    ],
    stream=True,
)

print("\n" + "=" * 20 + "思考过程" + "=" * 20 + "\n")

for chunk in completion:
    # 如果chunk.choices为空，则打印usage
    if not chunk.choices:
        print("\nUsage:")
        print(chunk.usage)
    else:
        delta = chunk.choices[0].delta
        # 打印思考过程
        if hasattr(delta, 'reasoning_content') and delta.reasoning_content != None:
            print(delta.reasoning_content, end='', flush=True)
            reasoning_content += delta.reasoning_content
        else:
            # 开始回复
            if delta.content != "" and is_answering == False:
                print("\n" + "=" * 20 + "完整回复" + "=" * 20 + "\n")
                is_answering = True
            # 打印回复过程
            print(delta.content, end='', flush=True)
            answer_content += delta.content

results = f"Reasoning Content:\n{reasoning_content}\n\nAnswer Content:\n{answer_content}"

with open(f'{file}修改.txt', 'w', encoding='utf-8') as file:
    file.write(results)


print(f"\n内容已成功写入 {file}.txt 文件。")