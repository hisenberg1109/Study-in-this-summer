from fastapi import FastAPI
from fastapi.responses import HTMLResponse

app = FastAPI()

@app.get('/fef')
def root():
    return HTMLResponse('<h1>hello world</h1>')

