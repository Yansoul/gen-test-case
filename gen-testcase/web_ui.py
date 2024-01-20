import gradio as gr
import llm_apis


def make_list(input_str):
    """
    分词解析 txt 接口文档
    """
    return [_.split(',') for _ in input_str.split('\n')]


def button_test_point(api_def):
    """
    按钮事件：需求点分析
    :param api_def:
    :return:
    """
    return llm_apis.try_again_if_failed(llm_apis.get_test_points(api_def))


def button_test_cases(api_def, test_points):
    """
    按钮事件：测试案例生成
    :param api_def:
    :param test_points:
    :return:
    """
    return llm_apis.try_again_if_failed(llm_apis.get_test_cases(api_def, test_points))


with gr.Blocks(theme=gr.themes.Soft()) as interface:
    # 接口文档txt
    with gr.Row():
        input_textbox = gr.Textbox(lines=3, placeholder="String Here...", label="接口文档")
        interfaceDoc = input_textbox  # 保存输入接口数据

    # 接口文档解析展示
    with gr.Row():
        output_table = gr.DataFrame(headers=["参数名", "类型", "长度", "是否必填", "描述"],
                                    label='接口定义解析',
                                    interactive=True,
                                    wrap=True)
    input_textbox.change(make_list, inputs=input_textbox, outputs=output_table)

    # 分析测试需求点
    with gr.Row():
        btn = gr.Button(value="需求点分析")
        btn.click(button_test_point(), inputs="", outputs="")

    # 生成测试用例
    with gr.Row():
        btn = gr.Button(value="测试案例生成")
        btn.click(button_test_cases(), inputs="", outputs="")

# 运行接口
interface.launch()
