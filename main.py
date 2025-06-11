import gradio as gr
import time
from action import action




with gr.Blocks() as demo:
    with gr.Sidebar():
        api_key = gr.Textbox(label="api_key")
    with gr.Group():
        with gr.Row():
            with gr.Column(scale=3):
                start1 = gr.Button("预处理", variant="primary", size="lg")
                load_file = gr.File(label="上传字幕")
                lines = gr.Slider(label="分割阈值", minimum=100, maximum=1000, value=500, interactive=True)
            with gr.Column(scale=2):
                output1 = gr.Textbox(label="输出", lines=4)
                output2 = gr.File(label="输出", height=40)

            start1.click(fn=action, inputs=(load_file, lines), outputs=(output1, output2))
    with gr.Group():
        with gr.Row():
            with gr.Column(scale=8):
                model = gr.Dropdown(choices=["DeepSeek-R1", "Gemini-2.5-Flash"])
                with gr.Column(scale=2):
                    run = gr.Checkbox(label="并发")
                with gr.Column(scale=2):
                    batch = gr.Textbox(label="并发数")
            with gr.Column(scale=2):
                start2 = gr.Button("运行", variant="primary", size="lg")


demo.launch()