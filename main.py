import os

# 全局变量
class Global:
    url = "http://{}/api/chat".format(os.environ.get("OLLAMA_HOST"))

print(Global.url)