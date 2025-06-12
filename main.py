import gradio as gr
import time
from openai import OpenAI
from action import action, run
from difflib import Differ




def client(api_key):
    client = OpenAI(
        # 若没有配置环境变量，请用阿里云百炼API Key将下行替换为：api_key="sk-xxx",
        api_key="YOUR API KET",  # 如何获取API Key：https://help.aliyun.com/zh/model-studio/developer-reference/get-api-key
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1"
    )
    return client


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
        role = gr.Textbox(label="system")
        with gr.Row():
            with gr.Column(scale=1):
                save = gr.Button("保存配置")
            with gr.Column(scale=1):
                default = gr.Button("恢复默认")
        out_client = gr.Textbox()
        save.click(fn=client, inputs=api_key, outputs=out_client)

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
                        index = gr.Textbox(label="索引值", value=1)
                    with gr.Column(scale=1):
                        batch = gr.Textbox(label="并发数", value=1)


                start2 = gr.Button("运行", variant="primary", size="lg")
                results1 = gr.Textbox(label="消息")
        #结果面板
        with gr.Row():
            with gr.Column(scale=1):
                results2 = gr.Textbox(label="修改前")
                results3 = gr.Textbox(label="修改后")
                compare = gr.HighlightedText(
                    label="Diff",
                    combine_adjacent=True,
                    show_legend=True,
                    color_map={"+": "green", "-": "red"})
            # with gr.Column(scale=1):


        start2.click(fn=run, inputs=(index, cut_lines), outputs=(results1, results2, results3))

        gr.Interface(diff_texts, [results2, results3], compare, theme=gr.themes.Base(), submit_btn="检视",clear_btn=None)

demo.launch()
