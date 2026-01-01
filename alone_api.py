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
    host = "http://{}:{}/".format(get_real_ip(),environ.get("OLLAMA_HOST").split(":")[-1])

app = FastAPI()

# Ollama健康检查
@app.get("/")
async def health():
    async with httpx.AsyncClient() as client:
        data = {
            "status": None,
            "health": None,
            "error": None,
            "host": None
        }
        try:
            r = await client.get(Global.host)
            data["status"] = r.status_code
            data["health"] = 1
            data["error"] = 0
        except Exception as e:
            data["status"] = 404
            data["health"] = 0
            data["error"] = e
        data["host"] = Global.host
        return data

# Ollama可用模型
@app.get("/models")
async def health():
    async with httpx.AsyncClient() as client:
        data = {}
        try:
            r = await client.get(Global.host + "api/tags")
            data["status"] = r.status_code
            data["models"] = []
            for i in r.json()["models"]:
                model = {
                    "name": i["name"],
                    "model": i["model"],
                    "size": i["size"]
                }
                data["models"].append(model)
            data["error"] = 0
        except Exception as e:
            data["status"] = 404
            data["models"] = None
            data["error"] = e
        data["host"] = Global.host
        return data

if __name__ == "__main__":
    # 直接运行 Python 文件时启动服务器
    run("alone_api:app", host="0.0.0.0", port=8080, reload=True)