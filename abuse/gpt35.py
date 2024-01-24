import gradio as gr
import openai
from openai import OpenAI

client = OpenAI(api_key='sk-')


async def analyze_documentation(documentation):
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": f"\n{documentation}"}
            ]
        )
        return response.choices[0].message
    except Exception as e:
        print(f"An error occurred: {e}")
        return str(e)


async def generate_test_cases(analysis):
    try:
        response = openai.Completion.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": "Hello!"}
            ]
        )
        return response.choices[0].text.strip()
    except Exception as e:
        return str(e)


with gr.Blocks() as demo:
    with gr.Row():
        with gr.Column():
            documentation_input = gr.TextArea(label="输入接口文档")
            analyze_button = gr.Button("分析")
        with gr.Column():
            analysis_output = gr.TextArea(label="测试需求点", interactive=True)
            generate_button = gr.Button("生成用例")
        with gr.Column():
            test_cases_output = gr.TextArea(label="测试用例结果")

    analyze_button.click(analyze_documentation, inputs=documentation_input, outputs=analysis_output)
    generate_button.click(generate_test_cases, inputs=analysis_output, outputs=test_cases_output)

demo.launch()
