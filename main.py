import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms
import os




from action import action1, action2, run, write_config_value, math_token, system_prompt, write_text
from difflib import Differ
from config import api_key





folder_name = 'temp'

if not os.path.exists(folder_name):
    os.makedirs(folder_name)
    print(f"文件夹 '{folder_name}' 已创建。")
else:
    pass




if api_key != "YOUR API KEY":
    password_state="API已输入"
else:
    password_state="API未输入"



#对比替换函数
def diff_texts(text1, text2):
    d = Differ()
    return [
        (token[2:], token[0] if token[0] != " " else None)
        for token in d.compare(text1, text2)
    ]
#索引变化
def indexs(index_value, max_number, mode="递增"):
    if mode == "递增":
        if index_value != max_number:
            index_value += 1
        return index_value


with gr.Blocks() as demo:
    with ms.Application():
        with antd.ConfigProvider():
            #侧边栏配置信息
            with gr.Sidebar():
                api_key = gr.Textbox(label="api_key", type="password")
                save = gr.Button("保存配置")
                default = gr.Button("恢复默认")
                out_state_put = gr.Textbox(show_label=False, value=password_state)
                system_prompt = antd.Input.Textarea()
                None_api = gr.Textbox(value="YOUR API KEY", visible=False)
                results7 = gr.Textbox(visible=False)
                max_index = gr.Number(visible=False)
                now_index = gr.File(visible=False)

            # #主要运行界面
            with gr.Group():
                with gr.Row():
                    #预处理面板
                    with gr.Column(scale=1):
                        with gr.Row():
                            with gr.Column(scale=2):
                                load_file = gr.File(label="上传字幕", height=237)
                                cut_lines = gr.Slider(label="分割阈值", minimum=100, maximum=1000, value=500, interactive=True)
                            with gr.Column(scale=2):
                                output1 = gr.Textbox(label="输出", lines=7)
                                output2 = gr.File(label="输出", height=237)
                        start1 = gr.Button("预处理", variant="primary", size="lg")

                    #运行配置面板
                    with gr.Column(scale=1):
                        with gr.Row():
                            with gr.Column(scale=1):
                                model = gr.Dropdown(label="选择模型", choices=["deepseek-r1-0528", "Gemini-2.5-Flash"],interactive=True)
                                message = gr.Textbox(label="Token count", value=f"838/64000")
                            with gr.Column(scale=1):
                                index = gr.Number(label="索引值", value=1, minimum=1)
                                batch = gr.Number(label="并发数", value=1, minimum=1)
                        start2 = gr.Button("运行", variant="primary", size="lg")
                        results1 = gr.Textbox(label="状态")
                        results6 = gr.File(label="输出", height=237)



            #结果面板
            with gr.Group():
                with gr.Row():
                    with gr.Column(scale=1):
                        results3 = gr.Textbox(label="确定的错误", lines=12, interactive=True)
                        results4 = gr.Textbox(label="可能的错误", lines=12, interactive=True)
                    with gr.Column(scale=1):
                        save_text = gr.Button("应用", variant="primary", size="lg")
                        output_text = gr.Button("输出新字幕", variant="primary", size="lg")
                        save_output = gr.Textbox(label="输出")

                    results2 = gr.Textbox(label="修改前", lines=16, interactive=True)
                    results5 = gr.Textbox(label="修改后", lines=16, interactive=True)
                    compare = gr.HighlightedText(
                        label="Diff",
                        combine_adjacent=True,
                        show_legend=True,
                        color_map={"+": "green", "-": "red"})
                # 检视对比
                gr.Interface(diff_texts, [results2, results5], compare, theme=gr.themes.Base(), submit_btn="检视",clear_btn=None)





                # 保存配置
                save.click(fn=write_config_value, inputs=api_key, outputs=out_state_put)
                # 恢复默认
                default.click(fn=write_config_value, inputs=None_api, outputs=out_state_put)

                # 预处理 #提取并切分
                start1.click(fn=action1, inputs=(load_file, cut_lines),outputs=(output1, output2, max_index))

                # 预处理后计算token
                start1.click(fn=math_token, inputs=index, outputs=message)
                # 切换索引计算token
                index.change(fn=math_token, inputs=index, outputs=message)

                # 索引递增
                start2.click(fn=indexs, inputs=(index, max_index),outputs=index)
                # 运行
                start2.click(fn=run, inputs=(index, cut_lines), outputs=(results1, results2, results3, results4, results5, results6, results7, now_index))

                # 应用
                save_text.click(fn=write_text, inputs=(results5, now_index))

                # 一键合并并替换
                output_text.click(fn=action2, inputs=(load_file, max_index))







demo.launch(inbrowser=True)