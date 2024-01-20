import gradio as gr
import requests
import json

url = "https://api.baichuan-ai.com/v1/chat/completions"
api_key = "sk-e5e338e255c747133853259b46b45d76"


def analyze_documentation(documentation):
    data = {
        "model": "Baichuan2-Turbo",
        "messages": [
            {
                "role": "user",
                "content": f'''
# Role
Interface Testing Expert

## Profile
- Language: Chinese

## Skills
- Business Experience: As an interface testing expert, possesses rich experience in interface testing and understands the purpose of interface testing.
- Professional Abilities: Familiar with the approach to testing analysis, able to comprehensively consider all test verification points of a single interface during analysis.

## Rules
1. 接口连通性验证：Basic validation, mainly checking if the server-side interface is properly started and if the client can establish a connection and send requests to the server.
2. 单字段验证：This level of validation is focused on each input parameter, checking its existence, correct type, and whether its length is within the expected range.
3. 字段间规则验证：This level of validation is about checking the logical relationships between multiple fields, such as dependencies and constraints.
4. Interface Definition Format:
"""
请求报文：
\n{documentation}
"""
5. Output Format, ignore newline characters:
"""
{{"test_points":[{{"category": "连通性验证", "content": "xxxx"}},{{"category": "单字段验证", "content": "字段abc，xxxx"}},{{"category": "单字段验证", "content": "字段efg，xxxx"}},{{"category": "字段间规则验证", "content": "字段a、字段b、和字段c，xxxx"}},...]}}
"""
6. The category can only be"连通性验证""单字段验证", or"字段间规则验证"
7. The content in the validation must only involve parameters defined in the interface.
8. Never use newline characters like "\\n"

## Workflow
1. Analyze the test points for connectivity verification.
2. For each parameter of the interface, analyze the single field verification test points.
3. Identify which parameters are interrelated and analyze all possible test points for these relationships.
4. Output in the Output Format difined in Roles.

## Goals
1. The test requirements for single field verification should cover all fields defined in the interface documentation.
2. The test requirements for inter-field rule verification should cover all the rules between fields.
                    '''
            }
        ],
        "stream": False
    }
    json_data = json.dumps(data)
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + api_key
    }

    response = requests.post(url, data=json_data, headers=headers, timeout=60)

    if response.status_code == 200:
        print(response)
        response.text
    else:
        print("请求失败，状态码:", response.status_code)
        print("请求失败，body:", response.text)
        return "请求失败，X-BC-Request-Id:", response.headers.get("X-BC-Request-Id")

with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            documentation_input = gr.TextArea(label="输入接口文档")
            analyze_button = gr.Button("开始分析")
        with gr.Column():
            analysis_output = gr.TextArea(label="测试需求点", interactive=True)
            generate_button = gr.Button("生成用例")
        with gr.Column():
            test_cases_output = gr.TextArea(label="测试用例结果")

    analyze_button.click(analyze_documentation, inputs=documentation_input, outputs=analysis_output)
    # generate_button.click(generate_test_cases, inputs=analysis_output, outputs=test_cases_output)
    # generate_button.click(generate_test_cases, inputs="验证custNbr、crdAcNbr、idNbr至少有一个必填的逻辑实现", outputs=test_cases_output)

demo.launch()
