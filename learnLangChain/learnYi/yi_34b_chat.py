# coding: utf-8

from langchain_openai import ChatOpenAI
import conf

YI_34B = ChatOpenAI(
    base_url=conf.LLM_URL_BASE,
    api_key="testme",
    max_tokens=4096,
    temperature=0.0,
    # streaming=True,
)
