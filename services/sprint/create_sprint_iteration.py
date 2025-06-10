from datetime import datetime, timedelta, date
from models import Sprints
from models.base import Session
from uuid import UUID
from flask import session as flask_session
from graphql_api.users.queries import get_cached_users_dict

def create_sprint_iteration(input):
    user_id = flask_session["auth_state"]["sub"]
    org_id = flask_session["auth_state"]["org_id"]

    session = Session()
    try:
        # Get the previous sprint
        previous_sprint = session.query(Sprints).filter(
            Sprints.id == UUID(input["previousSprintId"]),
            Sprints.org_id == org_id
        ).first()
        
        if not previous_sprint:
            raise Exception("Previous sprint not found")

        # Calculate new iteration number
        iteration = int(previous_sprint.iteration) + 1

        # Calculate new start and end dates
        start_date = date.today()
        end_date = start_date + timedelta(days=input["duration"])

        # Set previous sprint as not current
        previous_sprint.current = False
        previous_sprint.updated_by = user_id
        previous_sprint.updated_at = datetime.now()

        # Create new sprint iteration
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
            iteration=str(iteration),
            start_date=start_date,
            end_date=end_date
        )
        
        session.add(new_sprint)
        session.commit()

        # Get user information for response
        result = new_sprint.to_dict()
        result["createdBy"] = get_cached_users_dict(org_id)[result["createdBy"]]
        result["updatedBy"] = get_cached_users_dict(org_id)[result["updatedBy"]]
        return result
    except Exception as e:
        print(e)
        session.rollback()
        raise Exception("Failed to create sprint iteration.")
    finally:
        session.close() 