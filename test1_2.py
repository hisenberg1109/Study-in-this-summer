from fastapi import FastAPI, Form
from fastapi.responses import HTMLResponse
app = FastAPI()
student_info = []
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
    student_info.append({'name':name, 'student_id':student_id})
    
    html_head = f"""
    <!DOCTYPE html>
    <html lang="zh-CN">
    <head>
        <meta charset="UTF-8">
        <title>签到名单</title>
        <style>
            table {{ width: 600px; margin: 40px auto; border-collapse: collapse; }}
            th,td {{ border:1px solid #999; padding:10px; text-align:center; }}
            th {{ background: #f0f7ff; }}
            h2 {{ text-align:center; margin-top:30px; }}
            .tip {{ text-align:center; font-size:14px; color:#666; }}
            a {{ display:block; text-align:center; margin-top:20px; font-size:16px; }}
        </style>
    </head>
    <body>
        <h2>已签到学生名单（共{len(student_info)}人）</h2>
        <p class="tip">本机已签到，无法再次提交</p>
        <table>
            <tr>
                <th>序号</th>
                <th>姓名</th>
                <th>学号</th>
            </tr>
    """

    html_body = ""
    for idx, stu in enumerate(student_info, start=1):
        html_body += f"""
        <tr>
            <td>{idx}</td>
            <td>{stu['name']}</td>
            <td>{stu['student_id']}</td>
        </tr>
        """

    html_end = """
        </table>
        
    </body>
    </html>
    """
    full_html = html_head + html_body + html_end
    return full_html
