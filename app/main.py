from fastapi import FastAPI, Depends, HTTPException
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from sqlalchemy.orm import Session
import crud
import models
from database import SessionLocal, engine
from model.search import get_most_relevant_documents
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
templates = Jinja2Templates(directory="templates")

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get('/')
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


def save_relevant_documents(query: str, db: Session = Depends(get_db)):
    docs = get_most_relevant_documents(query)
    saved_documents = []
    for doc in docs:
        title = query 
        content = doc
        existing_doc = db.query(models.Document).filter(models.Document.content == content).first()
        
        if not existing_doc: 
            db_document = crud.create_document(db, title=title, content=content)
            saved_documents.append(db_document)
        else:
            saved_documents.append(existing_doc)  
    return saved_documents


@app.get('/search/')
def search(query: str, db: Session = Depends(get_db)):
    saved_documents = save_relevant_documents(query, db)
    
    response = {
        "relevant_documents": [
            {
                "id": doc.id,
                "title": doc.title,
                "snippet": "\n".join(doc.content.splitlines()[:3])  
            } for doc in saved_documents
        ]
    }
    return response


@app.get("/document/{doc_id}")
def get_document(doc_id: int, request: Request, db: Session = Depends(get_db)):
    document = db.query(models.Document).filter(models.Document.id == doc_id).first()
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    return templates.TemplateResponse("document.html", {"request": request, "document": document})
