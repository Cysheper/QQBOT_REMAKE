import json
from database.database import database 
from Modules.core import Status

class Image:
    def __init__(self):
        self.db: database = database("./Images/images")

    def addImage(self,repo: str, img: str) -> str:
        try:
            with open("./Images/images.json", "r", encoding="UTF-8") as f:
                data = json.load(f)

            if repo not in data:
                data[repo] = []

            if img in data[repo]:
                return "图片已存在"

            data[repo].append(img)

            with open("./Images/images.json", "w", encoding="UTF-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)

            return "图片添加成功"

        except Exception as e:
            return "添加图片错误"

    def getRandomImage(self, repo: str) -> Status:
        try:
            return Status(code="ok", message=self.db.random(repo))

        except Exception as e:
            return Status(code="error", message="获取图片错误")

    
    def getImageList(self) -> Status:
        try:
            data = self.db.getAll()

            info = "图片列表: \n"
            lst = []
            for repo in data.keys():
                lst.append((repo, len(data[repo])))

            lst.sort(key=lambda x: x[1], reverse=True)

            for repo, count in lst:
                info += f"[{repo}]: {count}\n"

            return Status(code="ok", message=info.strip())

        except Exception as e:
            return Status(code="error", message="获取图片列表错误")

        
        