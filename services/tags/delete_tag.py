from models import Tags
from models.base import Session
import uuid

def delete_tag(input):
    session = Session()
    try:
        tag = session.query(Tags).filter(Tags.id == uuid.UUID(input["id"])).first()
        if not tag:
            raise Exception("Tag not found.")
        
        session.delete(tag)
        session.commit()
        return True
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to delete tag.")
    finally:
        session.close()
