from datetime import datetime
from models import WorkItems, Tags, WorkItemTags
from models.base import Session
from flask import session as flask_session
import uuid

from models.work_items.work_items import ItemType, State, Priority, StoryPoints
from graphql_api.users.queries import get_cached_users_dict

class CreateWorkItem:
    def __init__(self, input):
        self.input = input
        self.data = {
            "title": input.get("title"),
            "description": input.get("description"),
            "assigned_to": input.get("assignedTo"),
            "created_by": flask_session["auth_state"]["sub"],
            "updated_by": flask_session["auth_state"]["sub"],
            "org_id": flask_session["auth_state"]["org_id"],
            "state": State.NEW.value
        }
        self.tags = input.get("tags", [])
    def is_valid(self, value, enum):
        return value in [e.value for e in enum]

    def initiative(self):
        if not self.input.get("assignedTo"):
            raise Exception("Initiative must have an assignee")
        
        data = self.data

        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            else:
                data["priority"] = Priority(self.input.get("priority")).value
        
        ts = datetime.now()
        
        data["created_at"] = ts
        data["updated_at"] = ts
        data["type"] = ItemType.INITIATIVE.value
            
        return data

    def epic(self):
        session = Session()
        if not self.input.get("assignedTo"):
            raise Exception("Epic must have an assignee")

        data = self.data
        
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            else:
                data["priority"] = Priority(self.input.get("priority")).value

        if not self.input.get("parent"):
            raise Exception("Epic must have a parent initiative")
        
        initiative = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
        
        if not initiative:
            raise Exception("Initiative not found")
        
        if initiative.type != ItemType.INITIATIVE.value:
            raise Exception("Parent must be an initiative")
        
        ts = datetime.now()
        
        data["created_at"] = ts
        data["updated_at"] = ts
        data["type"] = ItemType.EPIC.value
        data["parent"] = initiative.id
        session.close()
        return data

    def feature(self):
        session = Session()
        if not self.input.get("assignedTo"):
            raise Exception("Feature must have an assignee")
    
        data = self.data

        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            else:
                data["priority"] = Priority(self.input.get("priority")).value

        if not self.input.get("parent"):
            raise Exception("Feature must have a parent epic")
        
        epic = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
        
        if not epic:
            raise Exception("Epic not found")
        
        if epic.type != ItemType.EPIC.value:
            raise Exception("Parent must be an epic")
        
        ts = datetime.now()
        
        data["created_at"] = ts
        data["updated_at"] = ts
        data["type"] = ItemType.FEATURE.value
        data["parent"] = epic.id
        session.close()
        return data

    def user_story(self):
        session = Session()
        data = self.data

        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            else:
                data["priority"] = Priority(self.input.get("priority")).value

        if self.input.get("state") and not self.is_valid(self.input.get("state"), State):
            raise Exception("Invalid state")

        if not self.input.get("parent"):
            raise Exception("UserStory must have a parent feature")
        
        
        if self.input.get("storyPoints"):
            if not self.is_valid(self.input.get("storyPoints"), StoryPoints):
                raise Exception("Invalid story points") 
            if not self.input.get("assignedTo"):
                raise Exception("UserStory must have a assignee if story points are provided")
            if not self.input.get("sprint"):
                raise Exception("UserStory must be assigned to sprint if story points are provided")
            data["story_points"] = StoryPoints(self.input.get("storyPoints")).value
        else:    
            if self.input.get("state") and self.input.get("state") != State.BACKLOG.value:
                raise Exception("UserStory must have story points if not in backlog")
            data["state"] = State.BACKLOG.value
        
        feature = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
        
        if not feature:
            raise Exception("Feature not found")
        
        if feature.type != ItemType.FEATURE.value:
            raise Exception("Parent must be an feature")
        
        ts = datetime.now()
        
        data["created_at"] = ts
        data["updated_at"] = ts
        data["type"] = ItemType.USER_STORY.value
        data["parent"] = feature.id
        session.close()
        return data

    def task(self):
        session = Session()
        data = self.data

        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            else:
                data["priority"] = Priority(self.input.get("priority")).value

        if self.input.get("state"): 
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            else:
                data["state"] = State(self.input.get("state")).value

        if not self.input.get("parent"):
            raise Exception("Task must have a parent user story")
        

        if not self.input.get("original_estimate"):
            raise Exception("Task must have an estimate hours")
        else:
            data["original_estimate"] = self.input.get("original_estimate")
        
        user_story = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
        
        if not user_story:
            raise Exception("UserStory not found")
        
        if user_story.type != ItemType.USER_STORY.value:
            raise Exception("Parent must be an user story")
        
        ts = datetime.now()
        
        data["created_at"] = ts
        data["updated_at"] = ts
        data["type"] = ItemType.TASK.value
        data["parent"] = user_story.id
        session.close()
        return data

    def bug(self):
        session = Session()
        data = self.data
        if self.input.get("priority"):
            if not self.is_valid(self.input.get("priority"), Priority):
                raise Exception("Invalid priority")
            else:
                data["priority"] = Priority(self.input.get("priority")).value

        if self.input.get("state"):
            if not self.is_valid(self.input.get("state"), State):
                raise Exception("Invalid state")
            else:
                data["state"] = State(self.input.get("state")).value

        if not self.input.get("parent"):
            raise Exception("Bug must have a parent user story")
        

        if not self.input.get("original_estimate"):
            raise Exception("Bug must have an estimate hours")
        else:
            data["original_estimate"] = self.input.get("original_estimate")
        
        user_story = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input.get("parent"))).first()
        
        if not user_story:
            raise Exception("UserStory not found")
        
        if user_story.type != ItemType.USER_STORY.value:
            raise Exception("Parent must be an user story")
        
        ts = datetime.now()
        
        data["created_at"] = ts
        data["updated_at"] = ts
        data["type"] = ItemType.BUG.value
        data["parent"] = user_story.id
        session.close()
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
                
    def create(self):
        session = Session()
        try:
            data = self.get_data()
            work_item = WorkItems(**data)
            session.add(work_item)
            session.flush()  # Flush to get the work_item.id

            # Handle tags if provided
            if self.tags:
                ts = datetime.now()
                for tag_id in self.tags:
                    tag = session.query(Tags).filter(Tags.id == uuid.UUID(tag_id)).first()
                    if not tag:
                        raise Exception(f"Tag with id {tag_id} not found")
                    
                    work_item_tag = WorkItemTags(
                        work_item_id=work_item.id,
                        tag_id=tag.id,
                        created_at=ts,
                        updated_at=ts
                    )
                    session.add(work_item_tag)

            session.commit()
            result = work_item.to_dict()
            result["parent"] = result["parent"] if result["parent"] is None else session.query(WorkItems).filter(WorkItems.id == result["parent"]).first().to_dict()
            result["createdBy"] = get_cached_users_dict(data["org_id"])[result["createdBy"]]
            result["assignedTo"] = get_cached_users_dict(data["org_id"])[result["assignedTo"]]
            result["updatedBy"] = get_cached_users_dict(data["org_id"])[result["updatedBy"]]
            return result
        except Exception as e:
            session.rollback()
            raise e
        finally:
            session.close()