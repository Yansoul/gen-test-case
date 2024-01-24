import requests
from langchain.chains import ConversationChain
from langchain_openai import ChatOpenAI
from langchain_community.chat_models import QianfanChatEndpoint
from langchain_core.messages import HumanMessage

API_KEY = ""
SECRET_KEY = ""
url = "https://aip.baidubce.com/rpc/2.0/ai_custom/v1/wenxinworkshop/chat/yi_34b_chat?access_token="


def get_access_token():
    """
    使用 AK，SK 生成鉴权签名（Access Token）
    :return: access_token，或是None(如果错误)
    """
    url = "https://aip.baidubce.com/oauth/2.0/token"
    params = {"grant_type": "client_credentials", "client_id": API_KEY, "client_secret": SECRET_KEY}
    return str(requests.post(url, params=params).json().get("access_token"))


def get_yi_url():
    return url + get_access_token()


LLM_URL_BASE = get_yi_url()
# print(LLM_URL_BASE)

YI_34B = QianfanChatEndpoint(
    model="Yi-34B-Chat",
    qianfan_ak=API_KEY,
    qianfan_sk=SECRET_KEY
)

# YI_34B = ChatOpenAI(
#     base_url="http://10.34.21.33:8080/v1",
#     api_key="testme",
#     max_tokens=4096,
#     temperature=0.0,
#     # streaming=True,
# )

# 连通性测试
# conversation = ConversationChain(llm=YI_34B)
# resp = conversation.invoke("hello world!")
# print("resp:", resp)
# resp = resp["response"]
# print("resp:", resp)
