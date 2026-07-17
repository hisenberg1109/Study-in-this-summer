from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/image_query/{id}')
def img_query(id:int ):
    return FileResponse(f'/{id}.png')