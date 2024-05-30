from fastapi import APIRouter
from models.note import Note
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, RedirectResponse 
from config.db import conn
from schemas.note import noteEntity,notesEntity
from fastapi.templating import Jinja2Templates
from typing import Union
from bson import ObjectId 
note=APIRouter()
templates = Jinja2Templates(directory="templates")

@note.get("/", response_class=HTMLResponse)
async def read_item(request: Request):
    docs=conn.notes.notes.find({})
    newdocs=[]
    for doc in docs:
        newdocs.append({
            "id":doc["_id"],
            "title":doc["title"],
            "desc":doc["desc"],
            "important":doc["important"]
        })
    return templates.TemplateResponse( "index.html",{"request":request,"newdocs":newdocs})



@note.post("/",response_class=HTMLResponse)
async def create_item(request:Request ):
    form=await request.form()
    formDict=dict(form)
    formDict["important"]=True if formDict.get("important")=="on" else False
    note=conn.notes.notes.insert_one(formDict)
    docs=conn.notes.notes.find({})
    newdocs=[]
    for doc in docs:
        newdocs.append({
            "id":doc["_id"],
            "title":doc["title"],
            "desc":doc["desc"],
            "important":doc["important"]
        })
    return templates.TemplateResponse( "index.html",{"request":request,"newdocs":newdocs})



@note.post('/delete/{id}', response_class=HTMLResponse)
async def delete_user(id: str,request:Request ):
    dnote=noteEntity(conn.notes.notes.find_one_and_delete({"_id":ObjectId(id)}))
    return RedirectResponse( "/next",status_code=303)

@note.get('/next', response_class=HTMLResponse)
async def next_page(request: Request):
    docs=conn.notes.notes.find({})
    newdocs=[]
    for doc in docs:
        newdocs.append({
            "id":doc["_id"],
            "title":doc["title"],
            "desc":doc["desc"],
            "important":doc["important"]
        })
    return templates.TemplateResponse("next.html", {"request": request,"newdocs":newdocs})