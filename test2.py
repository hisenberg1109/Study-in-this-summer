from fastapi import FastAPI
from fastapi.responses import HTMLResponse


app=FastAPI()
@app.get('/index',response_class=HTMLResponse)
def index():
    html = 
    return 
    "<h1>暑期训练营签到系统<h1>"