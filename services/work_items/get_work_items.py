from models import WorkItems
from flask import session as flask_session
from models.base import Session
from graphql_api.users.queries import get_cached_users_dict
from models.work_items.work_items import ItemType, State, Priority, StoryPoints

class GetWorkItems:
    def __init__(self):
        self.org_id = flask_session["auth_state"]["org_id"]
                
    def get(self):
        session = Session()
        try:
            work_items = session.query(WorkItems).filter(WorkItems.org_id == self.org_id).all()
            new_work_items = []
            for work_item in work_items:
                temp = work_item.to_dict()
                temp["createdBy"] = get_cached_users_dict(self.org_id)[temp["createdBy"]]
                temp["updatedBy"] = get_cached_users_dict(self.org_id)[temp["updatedBy"]]
                temp["assignedTo"] = get_cached_users_dict(self.org_id)[temp["assignedTo"]]
                temp["type"] = ItemType(temp["type"]).value if temp.get("type") else None
                temp["state"] = State(temp["state"]).value if temp.get("state") else None
                temp["priority"] = Priority(temp["priority"]).value if temp.get("priority") else None
                temp["storyPoints"] = StoryPoints(temp["storyPoints"]).value if temp.get("storyPoints") else None
                temp["parent"] = temp["parent"] if temp["parent"] is None else session.query(WorkItems).filter(WorkItems.id == temp["parent"]).first().to_dict()
                new_work_items.append(temp)
            session.commit()
            return new_work_items
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception("Failed to get work_items.")
        finally:
            session.close()