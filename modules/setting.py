import os
import sqlite3

class Setting:
    def __init__(self):
        self.path = "setting.db"
    
    def set_path(self, path: str) -> bool:
        """ 음악봇 경로 설정 """
        if os.path.exists(path) is False:
            return False
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        cur.execute("CREATE TABLE IF NOT EXISTS path (id int PRIMARY KEY, path text)")

        cur.execute(f"SELECT * FROM path WHERE id=:id", {"id": 1})
        db_shuffle = cur.fetchone()
        if db_shuffle is None:
            # add path
            cur.execute(f"INSERT INTO path VALUES(?, ?)", (1, path))
        else:
            # modify path
            cur.execute(f"UPDATE path SET path=:path WHERE id=:id", {"path": path, 'id': 1})
        con.close()

        return True
    
    def get_path(self) -> str | None:
        """ 음악봇 경로 가져오기 """
        con = sqlite3.connect(self.path, isolation_level=None)
        cur = con.cursor()
        cur.execute(f"SELECT * FROM path WHERE id=:id", {"id": 1})
        temp = cur.fetchone()

        con.close()

        return temp[1]