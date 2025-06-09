from models import WorkItems
from flask import session as flask_session
from models.base import Session
from graphql_api.users.queries import get_cached_users_dict
from models.work_items.work_items import ItemType, State, Priority, StoryPoints
import uuid

class GetSprintUserStories:
    def __init__(self, sprint_id):
        self.org_id = flask_session["auth_state"]["org_id"]
        self.sprint_id = uuid.UUID(sprint_id)
                
    def get(self):
        session = Session()
        try:
            # Get all work items for the organization that belong to the specified sprint
            work_items = session.query(WorkItems).filter(
                WorkItems.org_id == self.org_id,
                WorkItems.current_sprint == self.sprint_id
            ).all()
            
            # Filter for user stories and their children
            user_stories = []
            for work_item in work_items:
                temp = work_item.to_dict()
                
                # Add user information
                temp["createdBy"] = get_cached_users_dict(self.org_id)[temp["createdBy"]]
                temp["updatedBy"] = get_cached_users_dict(self.org_id)[temp["updatedBy"]]
                temp["assignedTo"] = get_cached_users_dict(self.org_id)[temp["assignedTo"]]
                
                # Convert enums to values
                temp["type"] = ItemType(temp["type"]).value if temp.get("type") else None
                temp["state"] = State(temp["state"]).value if temp.get("state") else None
                temp["priority"] = Priority(temp["priority"]).value if temp.get("priority") else None
                temp["storyPoints"] = StoryPoints(temp["storyPoints"]).value if temp.get("storyPoints") else None
                
                # Add parent information if it exists
                temp["parent"] = temp["parent"] if temp["parent"] is None else session.query(WorkItems).filter(WorkItems.id == temp["parent"]).first().to_dict()
                
                # Add tags
                temp["tags"] = [work_item_tag.tag.to_dict() for work_item_tag in work_item.tags] if work_item.tags else []
                
                # Add mentions
                temp["mentions"] = [get_cached_users_dict(self.org_id)[mention] for mention in temp.get("mentions", [])]
                
                user_stories.append(temp)
                
            session.commit()
            return user_stories
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception("Failed to get sprint user stories.")
        finally:
            session.close() 