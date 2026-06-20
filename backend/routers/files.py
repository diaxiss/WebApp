import os
from fastapi import APIRouter
from fastapi.responses import FileResponse, Response

router = APIRouter()

FOLDERS = {
    "images": "./data/images",
    "user_images": "./data/user_images",
    "set_logo": "./data/set_logo",
    "set_symbol": "./data/set_symbol",
}

@router.get("/{folder}/{filename}")
def serve_file(folder: str, filename: str):
    if folder not in FOLDERS:
        return FileResponse(PLACEHOLDER)

    directory = FOLDERS[folder]
    path = os.path.join(directory, filename)

    if not os.path.exists(path):
        return FileResponse(f'./data/placeholder.webp')

    return FileResponse(path)