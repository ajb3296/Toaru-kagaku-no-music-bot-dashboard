import json
import uvicorn
import requests

from fastapi import FastAPI, Request
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from modules.statistics import Statistics
from modules.model import GetPath, StatisticsYear
from modules.setting import Setting
from modules.title import YTData

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

@app.get("/")
async def read_item(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})

@app.post("/statistics/year")
async def get_year(item: StatisticsYear) -> list[tuple[str, str, str, int]]:
    dict_item = dict(item)
    data = Statistics().get_year(dict_item["year"])[0:100]
    return_data = []
    header = {'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Trident/7.0; rv:11.0) like Gecko'}
    for video in data:
        video_id, video_count = video
        print(video_id, video_count)
        _, title, author = YTData().get(video_id)
        return_data.append((
            video_id,
            title,
            author,
            video_count
        ))
    return return_data

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