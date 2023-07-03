import os
import openai
import gradio as gr

openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxx"

start_sequence = "\nAI:"
restart_sequence = "\nHuman: "

prompt_txt = "输入你的问题"
prompt_img = "输入你的图像提示词"

messages = [
    {"role": "system", "content": "you are a very useful assistant"},
]

def openai_create(input):
    user_message = {"role": "user", "content": input}
    messages.append(user_message)
    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo-16k",
        messages=messages,
    )
    completion = completion.choices[0].message.content
    messages.append({"role": "assistant", "content": completion})

    return completion

def chatgpt_image(input, image_size, history,image_input):
    completion = openai.Image.create(
        prompt=input,
        n=1,
        size=image_size
    )
    return completion.data[0]['url'], history, ""

def chatgpt_chat(input, history,input_text):
    history = history or []
    output = openai_create(input)
    history.append((input, output))
    return history, history, ""

def clear(input,output):
    history = []
    input = ''
    output = ''
    return "","",""

block = gr.Blocks()

with gr.Blocks() as block:
    gr.Markdown("""<h1><center>ChatGPT Bot</center></h1>""")
    
    with gr.Tab("聊天"):
        chatbot = gr.Chatbot()
        text_input  = gr.Textbox(placeholder=prompt_txt)
        state = gr.State()
        with gr.Row():
            text_button = gr.Button("发送")
            clear_button = gr.Button("清空")
        
    with gr.Tab("图像"):
        image_output = gr.Image(width=512, height=512)
        image_input  = gr.Textbox(placeholder=prompt_img)
        image_size = gr.Radio(["256x256", "512x512", "1024x1024"],value="256x256",label="图片尺寸", info="选择生成的图片尺寸")
        state = gr.State()
        image_button = gr.Button("生成")
        
    text_button.click(chatgpt_chat, inputs=[text_input, state], outputs=[chatbot, state, text_input])
    clear_button.click(clear, inputs=[text_input,state], outputs=[chatbot,state,text_input])
    image_button.click(chatgpt_image, inputs=[image_input, image_size, state], outputs=[image_output, state, image_input])

block.launch(debug=True, server_name="0.0.0.0", server_port=8000, share=True)
