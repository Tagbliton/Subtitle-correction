import gradio as gr
import modelscope_studio.components.antd as antd
import modelscope_studio.components.base as ms


from action import action, run, write_config_value, token, system_prompt
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
#索引变化
def indexs(index, max, mode="递增"):
    if mode == "递增":
        if index != max:
            index += 1
            print(index)
        return index




with gr.Blocks(fill_height=True, fill_width=True) as demo:
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
                maxindex = gr.Number(visible=False)

                save.click(fn=write_config_value, inputs=api_key, outputs=out_state_put)
                default.click(fn=write_config_value, inputs=None_api, outputs=out_state_put)

            #主要运行界面
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





                    #预处理
                    start1.click(fn=action, inputs=(load_file, cut_lines), outputs=(output1, output2, maxindex))



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



                    #预处理后计算token
                    start1.click(fn=token, inputs=index, outputs=message)
                    #切换索引计算token
                    index.change(fn=token, inputs=index, outputs=message)


            #结果面板
            with gr.Group():
                with gr.Row():
                    with gr.Column(scale=1):
                        results3 = gr.Textbox(label="确定的错误", lines=12, interactive=True)
                    with gr.Column(scale=1):
                        results4 = gr.Textbox(label="可能的错误", lines=12, interactive=True)
                    results2 = gr.Textbox(label="修改前", lines=16, interactive=True)
                    results5 = gr.Textbox(label="修改后", lines=16, interactive=True)
                    compare = gr.HighlightedText(
                        label="Diff",
                        combine_adjacent=True,
                        show_legend=True,
                        color_map={"+": "green", "-": "red"})
                    # with gr.Column(scale=1):


                #索引递增
                start2.click(fn=indexs, inputs=(index, maxindex),outputs=index)
                #运行
                start2.click(fn=run, inputs=(index, cut_lines), outputs=(results1, results2, results3, results4, results5, results6, results7))
                #检视对比
                gr.Interface(diff_texts, [results2, results5], compare, theme=gr.themes.Base(), submit_btn="检视",clear_btn=None)

demo.launch(inbrowser=True)
