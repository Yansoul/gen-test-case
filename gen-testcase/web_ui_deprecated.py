# coding: utf-8
import time

import gradio
import gradio as gr
import pandas as pd

import llm_apis
from output_parser import TestPointSet, TestCaseSet

test_case_set = TestCaseSet(测试用例集=[])
df = pd.DataFrame([t.dict() for t in test_case_set.测试用例集])


# 定期检查 df 变化的函数
def update_output_table():
    global df
    # 假设此处有代码检查和更新 df
    # ...
    time.sleep(10)  # 每 10 秒检查一次
    return df


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
    print(f"api_def: \n{api_def}")
    return llm_apis.try_again_if_failed(llm_apis.get_test_points(api_def))


def button_test_cases(api_def, test_points):
    """
    按钮事件：测试案例生成
    :param api_def:
    :param test_points:
    :return:
    """
    # for i in range(len(test_points)):
    #     field = test_points[i][0]
    #     test_point = test_points[i][1]
    for inner_list in test_points:
        field, test_point = inner_list
        test_case_set_single = llm_apis.try_again_if_failed(llm_apis.get_test_cases(api_def, field, test_point))
        test_case_set.测试用例集.extend(test_case_set_single.测试用例集)
        global df
        df = pd.DataFrame([t.dict() for t in test_case_set.测试用例集])
    return df


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
        # btn.click(button_test_point(), inputs="", outputs="")

    # 生成测试用例
    with gr.Row():
        btn = gr.Button(value="测试案例生成")

        interface = gradio.Text(label="""
        | 参数名 | 类型 | 长度 | 是否必填 | 描述 |
        | --- | --- | --- | --- | --- |
        | custNbr | 字符 | 17 | 客户号、卡账号证件号必须有一个必输   | 客户号 |
        | crdAcNbr | 字符 | 22 | 客户号、卡账号、证件号必须有一个必输 | 卡账号 |
        | crdAcType | 字符 | 2 | 卡账号为必输时卡账号类型也为必输 | 卡账号类型(10-账号21-借记卡卡号，22-信用卡卡) |
        | idType | 字符 | 2 | 证件号码为必输时证件类型也为必输 | 证件类型 |
        | idNbr | 字符 | 24 | 客户号、卡账号、证件号必须有二个必输 | 证件号码 |
        | ownBrorg | 字符 | 4 | true | 机构 |
        | pageSize | 数字 | 2 | true | 每页记录数 |
        | currentPage | 数字 | 10 | true | 当前页数 |
        """)
        array_points = [
            ["custNbr", "必填校验"],
            ["custNbr", "长度校验"],
            ["crdAcNbr", "必填校验"],
            ["crdAcNbr", "长度校验"],
            ["crdAcType", "必填校验"],
            ["crdAcType", "长度校验"],
            ["crdAcType", "码值校验"],
            ["idType", "必填校验"],
            ["idType", "长度校验"],
            ["idType", "码值校验"],
            ["idNbr", "必填校验"],
            ["idNbr", "长度校验"],
            ["ownBrorg", "必填校验"],
            ["ownBrorg", "长度校验"],
            ["pageSize", "必填校验"],
            ["pageSize", "长度校验"],
            ["currentPage", "必填校验"],
            ["currentPage", "长度校验"]
        ]
        json_points = gr.JSON(label="JSON Points", value=array_points)

        # 用于显示测试用例
        output_table = gr.Dataframe(headers=["用例描述", "正反例", "步骤说明", "预期结果"],
                                    label='测试用例集',
                                    interactive=True,
                                    wrap=True)

        # 将按钮和表格添加到行中
        btn.click(fn=button_test_cases, inputs=[interface, json_points], outputs=output_table)
        # 设置一个定期运行的函数来更新 output_table
        gr.update_loop(update_output_table, output_table)

# 运行接口
interface.launch()
