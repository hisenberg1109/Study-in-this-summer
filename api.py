from fastapi import FastAPI

app = FastAPI()#创建实例

@app.get('/index')
def root():
    return 'hello world'

