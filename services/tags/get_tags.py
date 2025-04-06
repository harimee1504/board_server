from models import Tags
from flask import session as flask_session
from models.base import Session

def get_tags():
    org_id = flask_session["auth_state"]["org_id"]
    session = Session()
    try:
        tags = session.query(Tags).filter(Tags.org_id == org_id).all()
        result = [tag.to_dict() for tag in tags]
        session.commit()
        return result
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to get tags.")
    finally:
        session.close()
