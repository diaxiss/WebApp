import os
from fastapi import APIRouter, Request
from fastapi.responses import FileResponse, Response

router = APIRouter()

@router.get("/images/{filename}")
@router.get("/user_images/{filename}")
@router.get("/set_logo/{filename}")
@router.get("/set_symbol/{filename}")
def serve_file(filename: str, request: Request):

    path = f'./data/{request.url.path}'

    if not os.path.exists(path):
        match request.url.path.split('/')[1]:
            case 'images':
                return FileResponse(f'./data/placeholder.webp')
            case _:
                return FileResponse(f'./data/placeholder_set.png')

    return FileResponse(path)