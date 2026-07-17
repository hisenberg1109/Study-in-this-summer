from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/index', response_class=HTMLResponse)
def index():
    html = '''
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>暑期训练营签到系统</title>
        <style>
            .box { width: 400px; margin: 80px auto; padding: 30px; border: 1px solid #eee; border-radius: 8px; }
            .item { margin: 15px 0; }
            label { display: block; margin-bottom: 6px; font-weight: bold; }
            input { width: 100%; padding: 10px; box-sizing: border-box; border: 1px solid #ccc; border-radius: 4px; }
            button { width: 100%; padding: 12px; background: #0088ff; color: white; border: none; border-radius:4px; font-size:16px; cursor:pointer; }
            button:hover { background: #0066cc; }
        </style>
    </head>
    <body>
        <div class="box">
            <h2 style="text-align:center">暑期训练营签到系统</h2>
            <form action="/sign" method="post">
                <div class="item">
                    <label>姓名</label>
                    <input type="text" name="name" required placeholder="请输入姓名">
                </div>
                <div class="item">
                    <label>学号</label>
                    <input type="text" name="student_id" required placeholder="请输入学号">
                </div>
                <button type="submit">提交签到</button>
            </form>
        </div>
    </body>
    </html>
    '''
    return html

@app.post('/sign', response_class=HTMLResponse)
def sign(
    name: str = Form(), 
    student_id: str = Form()
):
    return f'姓名:{name}, 学号:{student_id}'
