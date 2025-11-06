#------------------
# STDLIB libraries
#------------------
import sys
import requests

#-----------------------
# Third party libraries
#-----------------------
from typing import Annotated
from fastapi import FastAPI, Depends, Cookie
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles

#-------------------------
# Local packages
#-------------------------
from routers import users, wishlist, collection, items

#---------------------
# App setup
#---------------------
app = FastAPI()

#serve images
app.mount('/images', StaticFiles(directory='./data/images'), name = 'images')
app.mount('/user_images', StaticFiles(directory='./data/user_images'), name = 'user_images')
app.mount('/set_logo', StaticFiles(directory='./data/set_logo'), name = 'set_logo')
app.mount('/set_symbol', StaticFiles(directory='./data/set_symbol'), name = 'set_symbol')
# Allow requests from frontend
origins = [
    "http://localhost:5173",  # Vite dev server
    "http://127.0.0.1:5173",
    "http://192.168.5.16:5173",
    "http://192.168.18.46:5173",
    "https://frontend-0ev7.onrender.com"
]

# CORS setup
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

#---------------
# Routers
#---------------
app.include_router(users.router)
app.include_router(wishlist.router)
app.include_router(collection.router)
app.include_router(items.router)

