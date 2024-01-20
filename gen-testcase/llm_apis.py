import traceback

from langchain.chains import ConversationChain
from langchain.memory import ConversationTokenBufferMemory
from yi_34b_chat import YI_34B as llm

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
    return ""


def get_test_cases(api_def, test_points):
    """
    生成测试用例列表接口
    :param api_def:
    :param test_points:
    :return:
    """

    return ""


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
