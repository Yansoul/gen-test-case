# coding: utf-8
import json
import time

import gradio
import gradio as gr
import pandas as pd

import llm_apis
from output_parser import TestPointSet, TestCaseSet


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
    array_points = []

    json_test_points = llm_apis.try_again_if_failed(llm_apis.get_test_points,
                                                    api_def)

    # 检查返回数据
    json_data = json.dumps(json_test_points,
                           ensure_ascii=False,
                           indent=4)
    print("web_ui_data: \n")
    print(json_data)

    json_test_points = json_test_points["test_points"]
    array_points.extend([[case["field"], case["test_point"]] for case in json_test_points])
    return array_points


def button_test_cases(api_def, test_points):
    """
    按钮事件：测试案例生成
    :param api_def:
    :param test_points:
    :return:
    """
    test_cases = []

    for row in test_points.itertuples():
        field = getattr(row, "字段")
        test_point = getattr(row, "验证点")
        print("field = " + field + "    test_point = " + test_point)
        json_test_cases = llm_apis.try_again_if_failed(llm_apis.get_test_cases,
                                                       api_def,
                                                       field,
                                                       test_point)

        # 检查返回数据
        json_data = json.dumps(json_test_cases,
                               ensure_ascii=False,
                               indent=4)
        print("web_ui_data:\n")
        print(json_data)

        json_test_cases = json_test_cases["测试用例集"]
        test_cases.extend([[case["用例描述"], case["正反例"], case["步骤说明"], case["预期结果"]] for case in json_test_cases])
    return test_cases


with gr.Blocks(theme=gr.themes.Soft()) as interface:
    # 接口文档解析展示
    with gr.Row():
        input_textbox = gr.Textbox(lines=3, placeholder="String Here...", label="接口文档")
        interfaceDoc = input_textbox  # 保存输入接口数据
    with gr.Row():
        api_table = gr.DataFrame(headers=["参数名", "类型", "长度", "是否必填", "描述"],
                                 label='接口定义解析',
                                 interactive=True,
                                 wrap=True)
    input_textbox.change(make_list, inputs=input_textbox, outputs=api_table)
    gr.Column()
    gr.Column()
    gr.Column()
    gr.Column()
    gr.Column()

    # 分析测试需求点
    with gr.Row():
        btn = gr.Button(value="需求点分析")
    with gr.Row():
        test_point_table = gr.Dataframe(headers=["字段", "验证点"],
                                        label='测试点',
                                        interactive=True,
                                        wrap=True)
        btn.click(fn=button_test_point,
                  inputs=api_table,
                  outputs=test_point_table)
    gr.Column()
    gr.Column()
    gr.Column()
    gr.Column()
    gr.Column()

    # 生成测试用例
    with gr.Row():
        btn = gr.Button(value="测试用例生成")
    with gr.Row():
        # 用于显示测试用例
        test_case_table = gr.Dataframe(headers=["用例描述", "正反例", "步骤说明", "预期结果"],
                                       label='测试用例集',
                                       interactive=True,
                                       wrap=True)
        # 将按钮和表格添加到行中
        btn.click(fn=button_test_cases,
                  inputs=[api_table, test_point_table],
                  outputs=test_case_table)

# 运行接口
interface.launch()

