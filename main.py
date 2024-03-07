#uvicorn main:app --reload
import json
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi_utilities import repeat_every
import os 
import threading

app = FastAPI()

origins = [
    "http://localhost",
    "http://localhost:8080",
    "http://localhost:5173",
    "http://localhost:5174",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Cron job for rss scrapping
@app.on_event("startup")
@repeat_every(seconds=60 * 30) #30 minutes
def startup_event():
    threading.Thread(target=do_work, daemon=True).start() 

def do_work():
    os.system('python rss.py')

# Routing
@app.get("/nwsfx")
async def root(skip: int = 0, limit: int = 50):
    with open('json/nwsfx.json') as j:
        j = json.load(j)
        return j[skip : skip + limit]

@app.get("/ai")
async def ai(skip: int = 0, limit: int = 50):
    with open('json/ai.json') as j:
        j = json.load(j)
        return j[skip : skip + limit]

@app.get("/world")
async def world(skip: int = 0, limit: int = 50):
    with open('json/world.json') as j:
        j = json.load(j)
        return j[skip : skip + limit]
    
@app.get("/tech")
async def tech(skip: int = 0, limit: int = 50):
    with open('json/tech.json') as j:
        j = json.load(j)
        return j[skip : skip + limit]
    
@app.get("/business")
async def biz(skip: int = 0, limit: int = 50):
    with open('json/business.json') as j:
        j = json.load(j)
        return j[skip : skip + limit]
    
@app.get("/science")
async def sci(skip: int = 0, limit: int = 50):
    with open('json/science.json') as j:
        j = json.load(j)
        return j[skip : skip + limit]