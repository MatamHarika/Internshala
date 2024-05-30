

from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Union
from pymongo import MongoClient
app=FastAPI()
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")
conn=MongoClient("mongodb+srv://harika:sastra123@cluster0.eynurrq.mongodb.net/notes")

@app.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs=conn.notes.notes.find({})
    newdocs=[]
    for doc in docs:
        newdocs.append({
            "id":doc["_id"],
            "note":doc["note"]
        })
    return templates.TemplateResponse( "index.html",{"request":request,"newdocs":newdocs}
    )

@app.get("/items/{items_id}")
def read_item(item_id:int, q: Union[str,None]=None):
    return {"item_id":item_id,"q":q}