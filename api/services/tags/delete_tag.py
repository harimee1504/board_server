from api.models import Tags
from api.models.base import session
import uuid

def delete_tag(input):
    try:
        tag = session.query(Tags).filter(Tags.id == uuid.UUID(input["id"])).first()
        if not tag:
            raise Exception("Tag not found.")
        session.query(Tags).filter(Tags.id == uuid.UUID(input["id"])).delete()
        session.commit()
        return {
            "deleted": True
        }
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to update tag.")
