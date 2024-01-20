from langchain.chains import ConversationChain, llm
from langchain.memory import ConversationTokenBufferMemory
from langchain.prompts import PromptTemplate, ChatPromptTemplate, HumanMessagePromptTemplate
from langchain.llms import OpenAI
from langchain.chat_models import ChatOpenAI

from langchain.output_parsers import PydanticOutputParser
from pydantic import BaseModel, Field, validator
from typing import List

from flask import Flask, request, jsonify


app = Flask(__name__)
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
    resp = resp.replace("<|im_end|>", "")
    return resp


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5555)
