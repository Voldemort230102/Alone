from os import environ
from fastapi import FastAPI
from uvicorn import run
import httpx
import socket

# 获取本机ip
def get_real_ip():
    try:
        # 建立一个 UDP 连接到外部地址（不会真的发数据）
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        s.connect(("8.8.8.8", 80))  # Google DNS，只用来探测路由
        ip = s.getsockname()[0]
        s.close()
        return ip
    except Exception:
        return "127.0.0.1"  # 回退到本地回环地址
# 全局变量
class Global:
    # Ollama服务地址
    host = "http://{}:{}".format(get_real_ip(),environ.get("OLLAMA_HOST").split(":")[-1])
print(Global.host)

app = FastAPI()

# Ollama健康检查
@app.get("/")
async def read_root():
    async with httpx.AsyncClient() as client:
        r = await client.get(Global.host)
        return r.content

if __name__ == "__main__":
    # 直接运行 Python 文件时启动服务器
    run("alone_api:app", host="0.0.0.0", port=8080, reload=True)