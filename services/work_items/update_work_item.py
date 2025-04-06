from datetime import datetime
from models import WorkItems
from models.base import Session
from flask import session as flask_session
from graphql_api.users.queries import get_cached_users_dict
import uuid

from models.work_items.work_items import ItemType, State, Priority, StoryPoints

class UpdateWorkItem:
    def __init__(self, input):
        self.input = input
        self.data = {}
        
        # Only include fields that are provided in the input
        if self.input.get("title"):
            self.data["title"] = self.input.get("title")
        if self.input.get("description"):
            self.data["description"] = self.input.get("description")
        if self.input.get("assignedTo"):
            self.data["assigned_to"] = self.input.get("assignedTo")
        
        # Always update the updated_by field
        self.data["updated_by"] = flask_session["auth_state"]["sub"]
        
        # Always update the updated_at field
        self.data["updated_at"] = datetime.now()
        
    def is_valid(self, value, enum):
        return value in [e.value for e in enum]

    def initiative(self):
        data = self.data.copy()
        
        # Handle priority if provided
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            data["priority"] = Priority(self.input.get("priority")).value
        
        # Handle state if provided
        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            data["state"] = State(self.input.get("state")).value
        
        # Set the type
        data["type"] = ItemType.INITIATIVE.value
            
        return data

    def feature(self):
        data = self.data.copy()
        
        # Handle priority if provided
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            data["priority"] = Priority(self.input.get("priority")).value
        
        # Handle state if provided
        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            data["state"] = State(self.input.get("state")).value
        
        # Handle parent if provided
        if self.input.get("parent"):
            feature = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
            
            if not feature:
                raise Exception("Feature not found")
            
            if feature.type != ItemType.INITIATIVE.value:
                raise Exception("Parent must be an initiative")
            
            data["parent"] = feature.id
        
        # Set the type
        data["type"] = ItemType.FEATURE.value
        
        return data

    def epic(self):
        data = self.data.copy()
        
        # Handle priority if provided
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            data["priority"] = Priority(self.input.get("priority")).value
        
        # Handle state if provided
        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            data["state"] = State(self.input.get("state")).value
        
        # Handle parent if provided
        if self.input.get("parent"):
            feature = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
            
            if not feature:
                raise Exception("Feature not found")
            
            if feature.type != ItemType.FEATURE.value:
                raise Exception("Parent must be a feature")
            
            data["parent"] = feature.id
        
        # Set the type
        data["type"] = ItemType.EPIC.value
        
        return data

    def user_story(self):
        data = self.data.copy()
        
        # Handle priority if provided
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            data["priority"] = Priority(self.input.get("priority")).value
        
        # Handle state if provided
        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            data["state"] = State(self.input.get("state")).value
        
        # Handle story points if provided
        if self.input.get("storyPoints"):
            if not self.is_valid(self.input.get("storyPoints"), StoryPoints):
                raise Exception("Invalid story points")
            data["story_points"] = StoryPoints(self.input.get("storyPoints")).value
        
        # Handle parent if provided
        if self.input.get("parent"):
            epic = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
            
            if not epic:
                raise Exception("Epic not found")
            
            if epic.type != ItemType.EPIC.value:
                raise Exception("Parent must be an epic")
            
            data["parent"] = epic.id
        
        # Set the type
        data["type"] = ItemType.USER_STORY.value
        
        return data

    def task(self):
        data = self.data.copy()
        
        # Handle priority if provided
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            data["priority"] = Priority(self.input.get("priority")).value
        
        # Handle state if provided
        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            data["state"] = State(self.input.get("state")).value
        
        # Handle original estimate if provided
        if self.input.get("original_estimate"):
            data["original_estimate"] = self.input.get("original_estimate")
        
        # Handle parent if provided
        if self.input.get("parent"):
            user_story = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
            
            if not user_story:
                raise Exception("UserStory not found")
            
            if user_story.type != ItemType.USER_STORY.value:
                raise Exception("Parent must be a user story")
            
            data["parent"] = user_story.id
        
        # Set the type
        data["type"] = ItemType.TASK.value
        
        return data

    def bug(self):
        data = self.data.copy()
        
        # Handle priority if provided
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            data["priority"] = Priority(self.input.get("priority")).value
        
        # Handle state if provided
        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            data["state"] = State(self.input.get("state")).value
        
        # Handle original estimate if provided
        if self.input.get("original_estimate"):
            data["original_estimate"] = self.input.get("original_estimate")
        
        # Handle parent if provided
        if self.input.get("parent"):
            user_story = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
            
            if not user_story:
                raise Exception("UserStory not found")
            
            if user_story.type != ItemType.USER_STORY.value:
                raise Exception("Parent must be a user story")
            
            data["parent"] = user_story.id
        
        # Set the type
        data["type"] = ItemType.BUG.value
        
        return data

    def get_data(self):
        type = self.input.get("type")
        if not type:
            raise Exception("WorkItem type is required")
        match type:
            case ItemType.INITIATIVE.value:
                return self.initiative()
            case ItemType.EPIC.value:
                return self.epic()
            case ItemType.FEATURE.value:
                return self.feature()
            case ItemType.USER_STORY.value:
                return self.user_story()
            case ItemType.TASK.value:
                return self.task()
            case ItemType.BUG.value:
                return self.bug()
            case _:
                raise Exception("Invalid WorkItem type")
                
    def update(self):
        session = Session()
        try:
            data = self.get_data()
            work_item = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input['id'])).first()
            if not work_item:
                raise Exception("Work Item not found.")
            
            # Only update fields that are provided in the data
            for key, value in data.items():
                setattr(work_item, key, value)
            
            session.commit()
            result = work_item.to_dict()
            result["parent"] = result["parent"] if result["parent"] is None else session.query(WorkItems).filter(WorkItems.id == result["parent"]).first().to_dict()
            result["createdBy"] = get_cached_users_dict(flask_session["auth_state"]["org_id"])[result["createdBy"]]
            result["assignedTo"] = get_cached_users_dict(flask_session["auth_state"]["org_id"])[result["assignedTo"]]
            result["updatedBy"] = get_cached_users_dict(flask_session["auth_state"]["org_id"])[result["updatedBy"]]
            return result
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception("Failed to update work_item.")
        finally:
            session.close()