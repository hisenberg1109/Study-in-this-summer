import json
from fastapi import FastAPI,Form,Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse,FileResponse
from fastapi.templating import Jinja2Templates

with open('pokemon.json','w')as f:
    pokemon_data  = json.load(f)

app = FastAPI(title='poken_search')
app.mount('/pokemon',StaticFiles)

templates = Jinja2Templates(
    directory='templates'

)


@app.get('/index.html', response_class=HTMLResponse)#github提交
def index(request: Request):
    return templates.TemplateResponse(
        'index.html', {
            'request':request
        }
    )


@app.post('/pokemon', response_class=HTMLResponse)
def pokemon(
    id: int = Form(ge=1, le=898)
):  
    
    # html1 = f'<img src=/pokemon/{id}.png></img>'
    # html2 = f'<p>名字:{pokemon_data[id]["name"]}</p>'
    # html3 = f'<p>描述:{pokemon_data[id]["desc"]}</p>'
    # html = html1 + html2 + html3
    return ''
@app.get('/main',response_class=FileResponse)
def main_py():
    return FileResponse('mian.py')


