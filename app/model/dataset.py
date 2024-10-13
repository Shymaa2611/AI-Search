import requests
import os
from datasets import load_dataset

def Load_dataset():
   ds = load_dataset("Falah/arxiv-research-paper")
   data=[]
   for paper in ds["train"]:
       data.append({'title':paper['title'],'id':paper['id']})
   return data


def get_content_paper(paper_id):
    pdf_url = f'https://arxiv.org/pdf/{paper_id}.pdf'
    response = requests.get(pdf_url)
    documents_folder = os.path.join(os.getcwd(), "documents")
    if not os.path.exists(documents_folder):
        os.makedirs(documents_folder) 
    pdf_path = os.path.join(documents_folder, f'{paper_id}.pdf')
    if response.status_code == 200:
        with open(pdf_path, 'wb') as f:
            f.write(response.content)
        print(f'Paper {paper_id}.pdf downloaded successfully and saved to {pdf_path}!')
    else:
        print(f'Failed to download paper. Status code: {response.status_code}')


def get_content_papers(data):
    for index in range(len(data)):
      get_content_paper(data[index]['id'])
