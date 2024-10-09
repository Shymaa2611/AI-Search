from fastapi import FastAPI
from fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.staticfiles import StaticFiles
from model.search import get_most_relevant_documents  # You need to implement this function

app = FastAPI()


templates = Jinja2Templates(directory="templates")

def get_most_relevant_documents(query):

    content = """This is the content of the first document.
It contains multiple lines.
Here is the third line.
This line will not be included in the snippet.
This is the content of the first document.
It contains multiple lines.
Here is the third line.
This line will not be included in the snippet.
This is the content of the first document.
It contains multiple lines.
Here is the third line.
This line will not be included in the snippet.
"""
    title = " ".join(query.split()[:10]) 
    snippet_lines = content.splitlines()[:5]
    snippet = " ".join(snippet_lines).strip()  
    relevant_documents = [
        {"id": 1, "title": title, "snippet": snippet},
        {"id": 2, "title": title, "snippet": snippet},
        {"id": 3, "title": title, "snippet": snippet},
    ]
    return  relevant_documents
    


@app.get('/')
def main(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.get('/search/')
def search(query: str):
    results = get_most_relevant_documents(query)
    response = {
        "relevant_documents": results
    }
    return response


@app.get("/document/{doc_id}")
def get_document(doc_id: int, request: Request):
    document = {
        "id": doc_id,
        "title": f"Document {doc_id}",
        "content": f"This is the content of Document {doc_id}. It includes more details about the document."
    }
    return templates.TemplateResponse("document.html", {"request": request, "document": document})

if __name__ == "__main__":
    query = "The mind of Osbert was torn by the most cruel conflict"
    response = search(query)    
    print("response:", response)
