import os
import uvicorn

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.statistics import Statistics
from modules.model import GetPath
from modules.setting import Setting

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.get("/statistics/year")
async def get_year(request: Request):
    data = Statistics().get_year()
    return data[0:100]

@app.get("/statistics/month")
async def get_month(request: Request):
    data = Statistics().get_month()
    return data[0:100]

@app.get("/statistics/week")
async def get_week(request: Request):
    data = Statistics().get_week()
    return data[1:100]

@app.post("/path")
async def get_path(item: GetPath):
    """ 음악봇 경로 설정 """
    status = Setting().set_path(item.path)
    return status

if __name__ == "__main__":
    # 공유기 포트포워딩 설정에서 내부 8000번 포트를 외부 80번 포트로 포워딩
    # 80번 포트로 열면 권한 문제가 발생할 수 있음
    uvicorn.run("main:app", host="0.0.0.0", port=8000, workers=4, log_level="info")