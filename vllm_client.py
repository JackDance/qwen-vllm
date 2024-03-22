import requests
import json

def clear_lines():
    print('\033[2J')
        
history=[]

# 流式输出
while True:
    query=input('问题:')

    # 调用api_server
    response=requests.post(
        url='http://localhost:6006/chat', json={
            'query': query,
            'stream': True,
            'history': history,
        }, stream=True
    )
    # response = requests.post(
    #     url='https://u24421-96e6-506251e3.westc.gpuhub.com:8443/chat', json={
    #         'query': query,
    #         'stream': True,
    #         'history': history,
    #     }, stream=True
    # )

    # 流式读取http response body, 按\0分割(server端在实现时专门手工设计了一个\0，所以在client端要按照\0这个分隔符进行分割。
    content = ""
    text_len = 0
    for chunk in response.iter_lines(chunk_size=8192,decode_unicode=False,delimiter=b"\0"):
        if chunk:
            data=json.loads(chunk.decode('utf-8'))
            text=data["text"].rstrip('\r\n') # 确保末尾无换行
            content = text[text_len:]
            # 打印最新内容
            print(content,end="", flush=True)
            text_len = len(text)
    print("\n")
    # 添加对话历史
    history.append((query,text))
    history=history[-5:]

# 非流式输出
# while True:
#     query=input('问题:')
#     response = requests.post(
#         url='https://u24421-96e6-506251e3.westc.gpuhub.com:8443/chat', json={
#             'query': query,
#             'stream': False,
#             'history': history,
#         }
#     )
#     text = json.loads(response.text)["text"]
#     print(text)
#
#     # 对话历史
#     history.append((query,text))
#     history=history[-5:]