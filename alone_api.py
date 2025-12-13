from os import environ
from fastapi import FastAPI
import uvicorn

# 全局变量
class Global:
    url = "http://{}/api/chat".format(environ.get("OLLAMA_HOST"))

print(Global.url)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "q": q}

if __name__ == "__main__":
    # 直接运行 Python 文件时启动服务器
    uvicorn.run("alone_api:app", host="127.0.0.1", port=8080, reload=True)