from api.models import Tags
from flask import session as flask_session
from api.models.base import session

def get_tags():
    org_id = flask_session["auth_state"]["org_id"]
    try:
        tags = session.query(Tags).filter(Tags.org_id == org_id).all()
        return tags
    except Exception as e:
        print(e)
        raise Exception("Failed to get tags.")
