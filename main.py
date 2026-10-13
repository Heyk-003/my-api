#引入 FastAPI 和 JSON 工具。
from fastapi import FastAPI
import json

app = FastAPI()

with open("data.json", encoding="utf-8") as f:  #with:自动管理文件。代码块结束后，会自动关闭文件
    students = json.load(f)    #**从文件对象 f 读取 JSON 文本，自动转换成 Python 字典 / 列表**。

@app.get("/")   #表示当客户端用 GET 方法访问根路径 / 时，执行下面的 home 函数。
def home():
    return {"message": "学生 API 已启动"}

@app.get("/students")  #获取所有学生接口
def get_students():
    return students

@app.get("/students/{student_id}")   #按学生 id 查询接口
def get_student(student_id: int):
    for s in students:
        if s["id"] == student_id:
            return s
    return {"error": "没有这个学生"}

@app.get("/search")   #按城市查询接口
def search(city: str = ""):
    if city == "":
        return students
    result = [s for s in students if s["city"] == city]
    return result