# coding: utf-8
import json
import traceback
import re

from langchain.chains import ConversationChain, LLMChain
from langchain.memory import ConversationTokenBufferMemory
from langchain.output_parsers import PydanticOutputParser
from langchain_core.prompts import PromptTemplate
from prompt_tpls import test_point_extraction, test_case_generation
from yi_34b_chat import YI_34B as llm
from output_parser import TestPointSet, TestCaseSet

MY_MEMORY = ConversationTokenBufferMemory(llm=llm, max_token_limit=2048)


def basic_chat(prompt):
    """
    基础的聊天接口，接收一个prompt，返回一个回答
    """
    global MY_MEMORY

    # 聊天提示词模板
    conversation = ConversationChain(
        llm=llm,
        memory=MY_MEMORY
    )
    resp = conversation.invoke(prompt)
    print("resp:", resp)
    resp = resp["response"]
    return resp


def get_test_points(api_def):
    """
    生成测试需求点接口
    :param api_def:
    :return:
    """
    # 调用 llm 生成测试点
    prompt = PromptTemplate(template=test_point_extraction, input_variables=["接口定义内容"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)
    resp = llm_chain.invoke(api_def)
    resp = resp["text"]

    # 解决一些格式问题
    resp = resp.replace("\"，", "\",")

    # 将测试点解析为JSON
    test_point_parser = PydanticOutputParser(pydantic_object=TestPointSet)
    test_points = test_point_parser.parse(resp)
    test_points = json.loads(test_points.json())

    test_points["code"] = 0
    test_points["msg"] = f"成功提取{len(test_points['test_points'])}个测试点"

    return test_points


def get_test_cases(api_def, field, test_point):
    """
    生成测试用例列表接口
    :param api_def:
    :param field:
    :param test_point:
    :return:
    """
    # 组装 prompt 模板
    prompt = PromptTemplate(template=test_case_generation, input_variables=["接口定义内容", "字段", "验证点"])
    llm_chain = LLMChain(prompt=prompt, llm=llm)

    # 调用大模型生成指定 Field 的指定验证点的用例
    field = str(field)
    test_point = str(test_point)
    print("Field: " + field + "\nTest_point: " + test_point)

    resp = llm_chain.invoke({
        '接口定义内容': api_def,
        '字段': field,
        '验证点': test_point
    })
    resp = resp["text"]
    # print("origin_text: \n" + resp)

    # 解决一些格式问题
    result = re.search(r'```json(.*?)```', resp, re.DOTALL)
    resp = result.group(1)
    # print("format: \n" + resp)
    test_case_parser = PydanticOutputParser(pydantic_object=TestCaseSet)
    test_case_obj = test_case_parser.parse(resp)
    test_case_obj = json.loads(test_case_obj.json())

    # print("final: \n" + json.dumps(test_case_obj, indent=4))

    return test_case_obj


def try_again_if_failed(fun_def, *args, **kwargs):
    """
    如果失败则重新调用函数，再试一次
    :param fun_def: 需要调用的函数
    :param args: 函数参数
    :param kwargs: 函数关键字参数
    :return: 函数返回值
    """
    try:
        return fun_def(*args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")

    try:
        return fun_def(*args, **kwargs)
    except Exception as e:
        print(f"Error: {e}")
        traceback.print_exc()

    return None



#
# get_test_points(interface)
# get_test_cases(interface, points)