from fastapi import FastAPI
from fastapi.responses import FileResponse

app = FastAPI()

@app.get('/img_query/{id}')
async def img_query(id: int):
    return FileResponse(f'pokemon/{id}.png')
    # return {'a': 'hello'}