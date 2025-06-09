from datetime import datetime, timedelta, date
from models import Sprints, WorkItems
from models.base import Session
from uuid import UUID
from flask import session as flask_session
from models.work_items.work_items import ItemType
from graphql_api.users.queries import get_cached_users_dict

def create_sprint(input):
    user_id = flask_session["auth_state"]["sub"]
    org_id = flask_session["auth_state"]["org_id"]

    session = Session()
    try:
        # Check if sprint with same name exists
        existing_sprint = session.query(Sprints).filter(
            Sprints.title.ilike(input["title"]),
            Sprints.org_id == org_id
        ).first()
        
        if existing_sprint:
            raise Exception("A sprint with this name already exists")

        iteration = 1
        start_date = date.today()
        end_date = start_date + timedelta(days=input["duration"])

        ts = datetime.now()
        new_sprint = Sprints(
            title=input["title"], 
            description=input["description"], 
            created_by=user_id,
            updated_by=user_id,
            current=True,
            org_id=org_id,
            created_at=ts,
            updated_at=ts,
            iteration=iteration,
            start_date=start_date,
            end_date=end_date
        )
        session.add(new_sprint)
        session.commit()
        result = new_sprint.to_dict()
        result["createdBy"] = get_cached_users_dict(org_id)[result["createdBy"]]
        result["updatedBy"] = get_cached_users_dict(org_id)[result["updatedBy"]]
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to create sprint.")
    finally:
        session.close()
