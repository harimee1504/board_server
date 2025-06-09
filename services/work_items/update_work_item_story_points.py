from datetime import datetime
from models import WorkItems
from models.base import Session
from flask import session as flask_session
from graphql_api.users.queries import get_cached_users_dict
import uuid

from models.work_items.work_items import ItemType, State, StoryPoints

class UpdateWorkItemStoryPoints:
    def __init__(self, input):
        self.input = input
        self.data = {
            "story_points": input.get("story_points"),
            "sprint": input.get("sprint"),
            "updated_by": flask_session["auth_state"]["sub"],
            "updated_at": datetime.now()
        }

    def is_valid_story_points(self, points):
        valid_points = [1, 2, 3, 5, 8, 13]  # Fibonacci sequence
        return points in valid_points

    def update(self):
        session = Session()
        try:
            # Validate story points
            if not self.is_valid_story_points(self.input.get("story_points")):
                raise Exception("Invalid story points. Must be one of: 1, 2, 3, 5, 8, 13")

            # Get work item
            work_item = session.query(WorkItems).filter(
                WorkItems.id == uuid.UUID(self.input['id']),
                WorkItems.org_id == self.input['org_id']
            ).first()
            
            if not work_item:
                raise Exception("WorkItem not found")

            # Validate work item type
            if work_item.type != ItemType.USER_STORY.value:
                raise Exception("Story points can only be set for user stories")

            # Update work item story points and sprint
            work_item.story_points = self.input.get("story_points")
            work_item.current_sprint = uuid.UUID(self.input.get("sprint"))
            
            # Set initial_sprint if it's empty
            if not work_item.initial_sprint:
                work_item.initial_sprint = uuid.UUID(self.input.get("sprint"))
                
            work_item.updated_by = self.data["updated_by"]
            work_item.updated_at = self.data["updated_at"]

            # If the work item is in backlog state, update it to new state
            if work_item.state == State.BACKLOG.value:
                work_item.state = State.NEW.value

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
            raise Exception("Failed to update work item story points.")
        finally:
            session.close() 