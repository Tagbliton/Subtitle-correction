import gradio as gr
import time

from action import action, run, write_config_value
from difflib import Differ
from config import api_key



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



with gr.Blocks() as demo:
    #侧边栏配置信息
    with gr.Sidebar():
        api_key = gr.Textbox(label="api_key", type="password")
        with gr.Row():
            with gr.Column(scale=1):
                save = gr.Button("保存配置")
            with gr.Column(scale=1):
                default = gr.Button("恢复默认")
        out_state_put = gr.Textbox(show_label=False, value=password_state)
        None_api = gr.Textbox(value="YOUR API KEY", visible=False)

        save.click(fn=write_config_value, inputs=api_key, outputs=out_state_put)
        default.click(fn=write_config_value, inputs=None_api, outputs=out_state_put)

    #主要运行界面
    with gr.Group():
        with gr.Row():
            #预处理面板
            with gr.Column(scale=1):
                with gr.Row():
                    with gr.Column(scale=2):
                        load_file = gr.File(label="上传字幕")
                        cut_lines = gr.Slider(label="分割阈值", minimum=100, maximum=1000, value=500, interactive=True)
                    with gr.Column(scale=2):
                        output1 = gr.Textbox(label="输出", lines=4)
                        output2 = gr.File(label="输出", height=40)
                start1 = gr.Button("预处理", variant="primary", size="lg")

            start1.click(fn=action, inputs=(load_file, cut_lines), outputs=(output1, output2))


            #运行配置面板
            with gr.Column(scale=1):
                model = gr.Dropdown(label="选择模型", choices=["deepseek-r1-0528", "Gemini-2.5-Flash"], interactive=True)
                with gr.Row():
                    with gr.Column(scale=1):
                        index = gr.Number(label="索引值", value=1)
                    with gr.Column(scale=1):
                        batch = gr.Number(label="并发数", value=1)


                start2 = gr.Button("运行", variant="primary", size="lg")
                results1 = gr.Textbox(label="消息")
        #结果面板
        with gr.Row():
            with gr.Column(scale=1):
                results2 = gr.TextArea(label="修改前")
                results3 = gr.TextArea(label="修改后")
                compare = gr.HighlightedText(
                    label="Diff",
                    combine_adjacent=True,
                    show_legend=True,
                    color_map={"+": "green", "-": "red"})
            # with gr.Column(scale=1):


        start2.click(fn=run, inputs=(index, cut_lines), outputs=(results1, results2, results3))

        gr.Interface(diff_texts, [results2, results3], compare, theme=gr.themes.Base(), submit_btn="检视",clear_btn=None)

demo.launch()
