from datetime import datetime
from models import Tags
from models.base import session
from sqlalchemy import func
from flask import session as flask_session

def create_tag(input):
    ts = datetime.now()
    user_id = flask_session["auth_state"]["sub"]
    org_id = flask_session["auth_state"]["org_id"]
    if not input["tag"]:
        raise Exception("Tag is required.")
    
    get_tag = session.query(Tags).filter(Tags.org_id == org_id, func.lower(Tags.tag) == input["tag"].lower()).first()
    if get_tag:
        raise Exception("Tag already exists.")
    try:
        new_tag = Tags(
            tag=input["tag"], 
            org_id=org_id,
            created_at=ts,
            updated_at=ts,
            created_by=user_id,
            updated_by=user_id
        )
        session.add(new_tag)
        session.commit()
        return new_tag.to_dict()
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to create tag.")
