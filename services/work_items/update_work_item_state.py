from datetime import datetime
from models import WorkItems
from models.base import Session
from flask import session as flask_session
from graphql_api.users.queries import get_cached_users_dict
import uuid

from models.work_items.work_items import State

class UpdateWorkItemState:
    def __init__(self, input):
        self.input = input
        self.data = {
            "state": input.get("state"),
            "updated_by": flask_session["auth_state"]["sub"],
            "updated_at": datetime.now()
        }

    def is_valid(self, value, enum):
        return value in [e.value for e in enum]

    def update(self):
        session = Session()
        try:
            # Validate state
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")

            # Get work item
            work_item = session.query(WorkItems).filter(
                WorkItems.id == uuid.UUID(self.input['id']),
                WorkItems.org_id == self.input['org_id']
            ).first()
            
            if not work_item:
                raise Exception("WorkItem not found")
            
            # Update work item state
            work_item.state = State(self.input.get("state")).value
            work_item.updated_by = self.data["updated_by"]
            work_item.updated_at = self.data["updated_at"]

            session.commit()
            result = work_item.to_dict()
            result["parent"] = result["parent"] if result["parent"] is None else session.query(WorkItems).filter(WorkItems.id == result["parent"]).first().to_dict()
            result["createdBy"] = get_cached_users_dict(self.input["org_id"])[result["createdBy"]]
            result["assignedTo"] = get_cached_users_dict(self.input["org_id"])[result["assignedTo"]]
            result["updatedBy"] = get_cached_users_dict(self.input["org_id"])[result["updatedBy"]]
            result["tags"] = [work_item_tag.tag.to_dict() for work_item_tag in work_item.tags] if work_item.tags else []
            return result
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception("Failed to update work item state.")
        finally:
            session.close() 