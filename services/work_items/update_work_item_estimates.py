from datetime import datetime
from models import WorkItems
from models.base import Session
from flask import session as flask_session
from graphql_api.users.queries import get_cached_users_dict
import uuid

from models.work_items.work_items import ItemType, State

class UpdateWorkItemEstimates:
    def __init__(self, input):
        self.input = input
        self.data = {
            "completed_estimate": float(input.get("completed_estimate", 0)),
            "updated_by": flask_session["auth_state"]["sub"],
            "updated_at": datetime.now()
        }

    def validate_estimate(self, completed_estimate: float, original_estimate: float) -> None:
        """Validate the completed estimate against the original estimate."""
        if completed_estimate < 0:
            raise Exception("Completed estimate cannot be negative")
        
        if completed_estimate > original_estimate:
            raise Exception("Completed estimate cannot exceed original estimate")

    def update(self):
        session = Session()
        try:
            # Get work item
            work_item = session.query(WorkItems).filter(
                WorkItems.id == uuid.UUID(self.input['id']),
                WorkItems.org_id == self.input['org_id']
            ).first()
            
            if not work_item:
                raise Exception("WorkItem not found")

            # Validate work item type
            if work_item.type not in [ItemType.TASK.value, ItemType.BUG.value]:
                raise Exception("Estimates can only be updated for tasks and bugs")

            # Validate completed estimate
            original_estimate = work_item.original_estimate or 0
            self.validate_estimate(self.data["completed_estimate"], original_estimate)

            # Update completed estimate
            work_item.completed_estimate = self.data["completed_estimate"]
            
            # Calculate and update remaining estimate
            completed_estimate = work_item.completed_estimate or 0
            work_item.remaining_estimate = max(0, original_estimate - completed_estimate)
            
            # Update metadata
            work_item.updated_by = self.data["updated_by"]
            work_item.updated_at = self.data["updated_at"]

            session.commit()
            result = work_item.to_dict()
            result["parent"] = result["parent"] if result["parent"] is None else session.query(WorkItems).filter(WorkItems.id == result["parent"]).first().to_dict()
            result["createdBy"] = get_cached_users_dict(self.input["org_id"])[result["createdBy"]]
            result["assignedTo"] = get_cached_users_dict(self.input["org_id"])[result["assignedTo"]]
            result["updatedBy"] = get_cached_users_dict(self.input["org_id"])[result["updatedBy"]]
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close() 