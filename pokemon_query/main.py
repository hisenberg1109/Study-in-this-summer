import json
from fastapi import FastAPI, Form, Request, Query
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse, FileResponse
from fastapi.templating import Jinja2Templates

with open('pokemon.json', 'r', encoding='utf-8') as f:
    pokemon_data = json.load(f)

app = FastAPI(title='Pokemon查询器')
app.mount('/pokemon', StaticFiles(directory='pokemon'), 
          name='pokemon')

templates = Jinja2Templates(
    directory='templates'
)

users = [{
    'username':'admin',
    'password': '123456'
}
]

@app.get('/index.html')
async def index(request: Request,
                login_form: str = Query(''),
                register_form: str = Query('')):
    
    print(login_form)
    print('hello')
    return templates.TemplateResponse(
        'index.html',
        {
            'request': request,
            'login_form': login_form,
            'register_form': register_form
        }
    )

@app.post('/pokemon')
async def pokemon(
    request: Request,
    id: int = Form(ge=1, le=898)
):  
    return templates.TemplateResponse(
        'pokemon.html', {
            'request':request,
            'pokemon_img_path': f'/pokemon/{id}.png',
            'pokemon':pokemon_data[id-1],
        }
    )