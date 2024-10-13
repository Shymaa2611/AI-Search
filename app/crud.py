from sqlalchemy.orm import Session
import models

def create_document(db: Session, title: str, content: str):
    db_document = models.Document(title=title, content=content)
    db.add(db_document)
    db.commit()
    db.refresh(db_document)
    return db_document

