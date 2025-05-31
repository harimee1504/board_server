from datetime import datetime, timedelta, date
from models import Sprints, WorkItems
from models.base import Session
from uuid import UUID
from flask import session as flask_session
from models.work_items.work_items import ItemType

def create_sprint(input):
    user_id = flask_session["auth_state"]["sub"]
    org_id = flask_session["auth_state"]["org_id"]

    session = Session()
    try:
        current_sprint = session.query(Sprints).filter(Sprints.current == True, Sprints.org_id == org_id).first()

        if not current_sprint:
            iteration = 1
            start_date = date.today()
            end_date = start_date + timedelta(days=14)
        else:
            iteration = current_sprint.iteration + 1
            if current_sprint.end_date < date.today():
                current_sprint.current = False
                start_date = date.today()
                end_date = start_date + timedelta(days=14)
            else:
                raise Exception("Current sprint is not completed.")

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
        return new_sprint.to_dict()
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to create sprint.")
    finally:
        session.close()
