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
from routers import users, wishlist, collection, items, files
from env import LOCAL_IP, DEPLOY_URL

#---------------------
# App setup
#---------------------
app = FastAPI()

# Allow requests from frontend
origins = [
    LOCAL_IP, 
    "http://localhost:5173",
    DEPLOY_URL
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
app.include_router(files.router)

