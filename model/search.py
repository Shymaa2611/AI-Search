
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS

def load_dataset():
   folder_path = r'documents'
   text_loader_kwargs = {'autodetect_encoding': True}
   mixed_loader = DirectoryLoader(
    path=folder_path,
    glob='*.txt',
    loader_cls=TextLoader,
    loader_kwargs=text_loader_kwargs
   )
   docs = mixed_loader.load()

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