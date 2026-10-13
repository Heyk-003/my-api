# 引入 FastAPI 和 JSON 工具
from fastapi import FastAPI, HTTPException   # ← 修改1：多导入 HTTPException
import json

app = FastAPI()

with open("data.json", encoding="utf-8") as f:
    people = json.load(f)

    # ← 修改2：f1["class"] 改成 f1.get("class")，防止字段缺失报错
    brother1 = [f1 for f1 in people if f1.get("class") == "brother"]
    friend1 = [f1 for f1 in people if f1.get("class") == "friend"]


@app.get("/")  # 访问根路径时执行 home
def home():
    return {"message": "访问已启动"}


@app.get("/brother")
def get_brothers():          # ← 修改3：原来叫 def brother()，避免和下面函数重名
    return brother1


@app.get("/friend")
def get_friends():           # ← 修改4：原来叫 def friend()，避免和下面函数重名
    return friend1


@app.get("/friend/{friend_id}")
def get_friend_by_id(friend_id: int):   # ← 修改5：原来叫 def friend(...)，避免重名
    for ff in friend1:
        if ff["id"] == friend_id:
            return ff
    # ← 修改6：原来 return {"error": "没有这个朋友"}
    raise HTTPException(status_code=404, detail="没有这个朋友")


@app.get("/brother/{brother_id}")
def get_brother_by_id(brother_id: int):  # ← 修改7：原来叫 def brother(...)，避免重名
    for bb in brother1:
        if bb["id"] == brother_id:
            return bb
    # ← 修改8：原来 return {"error": "没有这个兄弟"}
    raise HTTPException(status_code=404, detail="没有这个兄弟")


@app.get("/search")  # 按城市查询接口
def search(city: str = ""):
    if city == "":
        return people
    # ← 修改9：s["city"] 改成 s.get("city")
    result = [s for s in people if s.get("city") == city]
    return result

##安装：uvicorn main2:app --reload
#调用说明：http://127.0.0.1:8000/brother
#按号查询：http://127.0.0.1:8000/friend/2
#按地方：http://127.0.0.1:8000/search?city=北京
#自动生成的测试页面：http://127.0.0.1:8000/docs