from datetime import datetime
from models import Tags
from models.base import session
from flask import session as flask_session
from sqlalchemy import func
import uuid

def update_tag(input):
    user_id = flask_session["auth_state"]["sub"]
    org_id = flask_session["auth_state"]["org_id"]
    tag = session.query(Tags).filter(Tags.id == uuid.UUID(input["id"])).first()
    if not tag:
        raise Exception("Tag not found.")
    
    get_tag = session.query(Tags).filter(Tags.org_id == org_id, func.lower(Tags.tag) == input["tag"].lower()).first()
    
    if get_tag and get_tag.id != input["id"]:
        raise Exception("Tag already exists.")
    
    ts = datetime.now()
    try:
        updated_tag = session.query(Tags).filter(Tags.id == uuid.UUID(input["id"])).update({
            "tag": input["tag"], 
            "updated_at": ts,
            "updated_by": user_id
        })
        session.commit()
        
        if not updated_tag:
            raise Exception("Failed to update tag.")
        
        return {
            "id": tag.id,
            "tag": tag.tag
        }
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to update tag.")
