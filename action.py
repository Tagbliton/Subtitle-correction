import json
from config import api_key
from openai import OpenAI
from deepseek_v3_tokenizer.deepseek_tokenizer import tokenizer

#提取文本
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


#切分字幕
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

#一键提取并切分
def action(input_file, max_lines):
    output1, output2=extract_text_from_srt(input_file)
    output3=split_file(max_lines)

    return (f"{output1}\n{output3}", output2)



#读取文本
def read_file_to_variable(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        A = file.read()
    return A

#保存文件
def save_file(file, value):
    with open(file, 'w', encoding='utf-8') as f:
        f.write(value)
    print(f"内容已成功写入 {file}.txt 文件。")
    return f"内容已成功写入 {file}.txt 文件。"

#计算token
def token(index):
    value = read_file_to_variable(f"results_{index}.txt")
    return f"{tokenizer(value)}/64000"






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






#系统提示词处理
def system_prompt(index, cut_lines):
    lines = int(index-1) * int(cut_lines) + 1
    prompt = f'用户将提供一些视频字幕文本，序号从{lines}开始标注，校正其中明显的错别字，有些内容虽然表述错误但可能符合视频人物说出的话，请将"修改前"、"确定的错误"、"可能的错误"以及"修改后"分别解析为"before"、"error"、"maybe"和"after"，并以json格式输出.'
    example = """
    示例输入: 
    183. 这个项目占不占自然岸线
    184. 基本上的分类的
    185. 一个一个
    186. 一个简单的一个现场认定标准啊
    187. 那么案线保有率的管控啊
    188. 这个国家对于我们自然案线的保有率
    189. 其实是有要求的啊
    190. 呃三审仪式啊
    191. 东海区的三审仪式呢
    192. 这个新修测案线的这个成果
    193. 已经进入经各个省市人民政府的批准
    194. 已经实施了
    195. 那么下阶段这个自然案线呢
    196. 也是海洋督查
    197. 呃这
    198. 个督查的一个重点啊


    EXAMPLE JSON OUTPUT:
    {
        "before": {
        183. 这个项目占不占自然岸线
        184. 基本上的分类的
        185. 一个一个
        186. 一个简单的一个现场认定标准啊
        187. 那么案线保有率的管控啊
        188. 这个国家对于我们自然案线的保有率
        189. 其实是有要求的啊
        190. 呃三审仪式啊
        191. 东海区的三审仪式呢
        192. 这个新修测案线的这个成果
        193. 已经进入经各个省市人民政府的批准
        194. 已经实施了
        195. 那么下阶段这个自然案线呢
        196. 也是海洋督查
        197. 呃这个
        198. 督查的一个重点啊
        },
        "error": {
        187. 那么案线保有率的管控啊  // 案线 -> 岸线 //（海岸线术语）
        188. 这个国家对于我们自然案线的保有率  // 案线 -> 岸线
        190. 呃三审仪式啊  // 三审仪式 -> 三省一市 //（指上海、江苏、浙江、福建）
        191. 东海区的三审仪式呢  // 三审仪式 -> 三省一市
        192. 这个新修测案线的这个成果  // 案线 -> 岸线
        195. 那么下阶段这个自然案线呢  // 案线 -> 岸线
        196. 也是海洋督查  // 督查 -> 督察 //（行政监督术语）
        198. 督查的一个重点啊  // 督查 -> 督察
        },
        "maybe": {
        185. 一个一个  //  一个
        190. 呃三省一市啊  //  三省一市啊
        193. 已经进入经各个省市人民政府的批准  //  已经经各个省市人民政府的批准
        },
        "after": {
        183. 这个项目占不占自然岸线
        184. 基本上的分类
        185. 一个
        186. 一个简单的现场认定标准啊
        187. 那么岸线保有率的管控啊
        188. 这个国家对于我们自然岸线的保有率
        189. 其实是有要求的
        190. 三省一市啊
        191. 东海区的三省一市呢
        192. 这个新修测案线的成果
        193. 已经经各个省市人民政府的批准
        194. 已经实施了
        195. 那么下阶段这个自然岸线呢
        196. 也是海洋督察
        197. 这个
        198. 督查的一个重点啊
        },  
    }
    """
    system_prompt = f"{prompt}{example}"

    return system_prompt





#deepseek
def run(index, cut_lines):
    client = OpenAI(api_key=api_key, base_url="https://api.deepseek.com")
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
    print(response.choices[0].message.content)
    results = json.loads(response.choices[0].message.content)



    # 1. 遍历before字典的键和值
    before = results['before']
    print("--- 'before' 中的序号和内容 ---")
    before_lines = ""
    for key, value in before.items():
        before_lines = f"{before_lines}{key}: {value}\n"
    print(before_lines)


    # 2. 遍历error字典的键和值
    error = results['error']
    print("--- 'error' 中的序号和内容 ---")
    error_lines = ""
    for key, value in error.items():
        error_lines = f"{error_lines}{key}: {value}\n"
    print(error_lines)

    # 3. 遍历maybe字典的键和值
    maybe = results['maybe']
    print("--- 'maybe' 中的序号和内容 ---")
    maybe_lines = ""
    for key, value in maybe.items():
        maybe_lines = f"{maybe_lines}{key}: {value}\n"
    print(maybe_lines)

    # 4. 遍历after字典的键和值
    after = results['after']
    print("--- 'after' 中的序号和内容 ---")
    after_lines = ""
    for key, value in after.items():
        after_lines = f"{after_lines}{key}: {value}\n"
    print(after_lines)


    #保存结果
    message= save_file(f"{file}修改建议.txt", f"{before_lines}{error_lines}{maybe_lines}{after_lines}")


    return message, before_lines, error_lines, maybe_lines, after_lines, f"{file}修改建议.txt"


def write_config_value(value):
    """将新值写入配置文件"""
    new_value=f'api_key="{value}"'
    with open("config.py", "w") as f:
        f.writelines(new_value)
    if value != "YOUR API KEY":
        return "配置已保存，请重新启动以应用"
    else:
        return "已恢复默认，请重新启动以应用"




# role="""文本为srt字幕文件内容，校正其中明显的错别字，有些内容虽然表述错误但可能符合视频人物说出的话，仅仅修改其中明显的错别字，并在每一行文本前添加序号，将可能错误的地方进行总结好方便我修改。
# 输出示例：
# ### 错误总结（方便您修改）：
# 我修改了所有 ** 明显的错别字 ** （基于常见错误），但对表述错误或口语化内容（如重复、语法问题）未改动。以下是详细列表：
#
# #### **已校正的明显错别字**（共38处）：
# | 序号 | 原词 | 校正后 | 上下文示例 |
# | ------ | ------ | -------- | ------------ |
# | 48 | 建 | 检 | "总量也要去建" → 应为"检"（检查 / 检测） |
# | 49 | 废气物 | 废弃物 | "会产生那个废气物的" → 标准术语 |
# | 56 | 船子 | 船只 | "清除的船子" → 音近字错误 |
# | 90 | 桥梦 | 桥墩 | "这里桥梦有灌注的" → 形近字错误（"梦"→"墩"） |
# | 91 | 桥梦 | 桥墩 | 同上 |
# | 110 | 废气物 | 废弃物 | "它会产生那个废气物的" → 同上 |
# | 128 | 青岛 | 倾倒 | "青岛的设备" → 音近字错误（"青岛"→"倾倒"） |
# #### **未修改的可能错误**（符合人物口语或表述，但需您确认）：
# - **序号17-18、42等："正压层"**：可能是"正压层"（地质术语），但未改动，因人物可能口语化说错。
# - **序号28："要设置定"**：可能应为"要设定"或"要固定"，但保留口语表述。
# - **序号30："炸有个孔呢"**：口语化重复（"炸礁石炸"），未改动。
# - **序号103："外力转盘还是用水枪重提转盘"**：表述模糊（可能指设备类型），未改动。"""
