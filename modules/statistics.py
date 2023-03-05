"""

Table name example : date20220101

ID, video_id, count

"""

import sqlite3
import calendar
from datetime import datetime, timedelta

from modules.setting import Setting

class Statistics:
    def __init__(self):
        self.statisticsdb = StatisticsDb()
    
    def get_week(self) -> list[tuple[str, int]]:
        """ 이번주의 통계를 가져옵니다 """
        week_data = {}
        for day in range(7): # 0 ~ 6
            # 타깃 날짜 설정
            target_date = datetime.today() - timedelta(days=day)
            table_name = f"date{target_date.strftime('%Y%m%d')}"

            # 해당 날짜의 데이터 가져오기
            videos_data = self.statisticsdb.get_all(table_name)
            if videos_data is not None:
                for data in videos_data:
                    _, video_id, count = data
                    if week_data.get(video_id) is None:
                        week_data[video_id] = count
                    else:
                        week_data[video_id] += count

        # Sort
        week_data = sorted(week_data.items(), key = lambda item: item[1], reverse = True)
        return week_data

    def get_month(self) -> list[tuple[str, int]]:
        """ 이번달의 통계를 가져옵니다 """
        month_data = {}
        for day in range(1, 31): # 1 ~ 30
            # 타깃 날짜 설정
            target_date = datetime.today() - timedelta(days=day)
            table_name = f"date{target_date.strftime('%Y%m%d')}"

            # 해당 날짜의 데이터 가져오기
            videos_data = self.statisticsdb.get_all(table_name)
            if videos_data is not None:
                for data in videos_data:
                    _, video_id, count = data
                    if month_data.get(video_id) is None:
                        month_data[video_id] = count
                    else:
                        month_data[video_id] += count

        # Sort
        month_data = sorted(month_data.items(), key = lambda item: item[1], reverse = True)
        return month_data
    
    def get_year(self, year: int = datetime.now().year) -> list[tuple[str, int]]:
        """ 해당하는 년도의 통계를 가져옵니다 """
        year_data = {}

        now = datetime.now()

        # 시작 날짜 설정
        start_date = datetime.strptime(f"{year}-01-01", '%Y-%m-%d')

        # 해당 연도의 마지막 날을 설정
        end_date = datetime.strptime(f"{year}-12-{calendar.monthrange(now.year, now.month)[1]}", '%Y-%m-%d')

        # 올해일 경우 마지막 날짜를 어제로 설정
        if now.year == year:
            end_date = now - timedelta(days=1)

        target_date = start_date
        while True:
            if target_date > end_date:
                break

            # 타깃 날짜 설정
            target_date += timedelta(days=1)
            table_name = f"date{target_date.strftime('%Y%m%d')}"

            # 해당 날짜의 데이터 가져오기
            videos_data = self.statisticsdb.get_all(table_name)
            if videos_data is not None:
                for data in videos_data:
                    _, video_id, count = data
                    if year_data.get(video_id) is None:
                        year_data[video_id] = count
                    else:
                        year_data[video_id] += count

        # Sort
        year_data = sorted(year_data.items(), key = lambda item: item[1], reverse = True)
        return year_data

class StatisticsDb:
    def __init__(self):
        pass

    def get(self, table_name: str, video_id: str) -> tuple[int, str, int] | None:
        """ 비디오 아이디로 데이터를 가져옴 """
        path = Setting().get_path()
        if path is None:
            return None
        conn = sqlite3.connect(path + "/statistics.db", isolation_level=None)
        c = conn.cursor()
        try:
            c.execute(f"SELECT * FROM {table_name} WHERE video_id=:video_id", {"video_id": video_id})
        except sqlite3.OperationalError:
            conn.close()
            return None
        temp = c.fetchone()
        conn.close()
        return temp

    def get_all(self, table_name: str) -> list[tuple[int, str, int]] | None:
        """ 테이블의 모든 데이터를 가져옴 """
        path = Setting().get_path()
        if path is None:
            return None
        conn = sqlite3.connect(path + "/statistics.db", isolation_level=None)
        c = conn.cursor()
        # 내림차순으로 정렬
        try:
            c.execute(f"SELECT * FROM {table_name} ORDER BY count DESC")
        except sqlite3.OperationalError:
            return None
        temp = c.fetchall()
        conn.close()
        return temp