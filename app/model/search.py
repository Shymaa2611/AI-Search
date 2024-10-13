from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain.document_loaders import PyPDFLoader
from preprocessing import clean

def get_page_content(docs):
    data=[]
    for index in range(len(docs)):
        doc=clean(docs[index].page_content)
        data.append(doc)
    return data

def load_dataset():
    folder_path = r'documents'
    mixed_loader = DirectoryLoader(
        path=folder_path,
        glob='*.pdf',
        loader_cls=PyPDFLoader  
    )
    docs = mixed_loader.load()
    docs=get_page_content(docs)
    return docs

def split_documents_into_chunks():
     docs=load_dataset()
     text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
     chunks= text_splitter.split_documents(docs)
     return chunks

def store_index_chunks():
     chunks=split_documents_into_chunks()
     encoder = HuggingFaceEmbeddings()
     db = FAISS.from_documents(documents=chunks, embedding=encoder)
     retriever = db.as_retriever(search_kwargs={"k": 10})
     return retriever

def get_most_relevant_documents(query):
   docs_content=[]
   retriever=store_index_chunks()
   documents = retriever.get_relevant_documents(query)
   for doc in documents:
      docs_content.append(doc.page_content)
   return docs_content 




