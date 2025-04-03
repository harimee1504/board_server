from models import WorkItems
from models.base import session
from uuid import UUID

from models.work_items.work_items import ItemType

class DeleteWorkItem:
    def __init__(self, input):
        self.input = input
        self.error_message = {
            ItemType.INITIATIVE: "Initiative cannot be deleted because it contains associated child epic",
            ItemType.EPIC: "Epic cannot be deleted because it contains associated child feature",
            ItemType.FEATURE: "Feature cannot be deleted because it contains associated child user story",
            ItemType.USER_STORY: "User Story cannot be deleted because it contains associated child task or bug"
        }
                
    def delete(self):
        data = self.input
        
        try:
            work_item = session.query(WorkItems).filter(WorkItems.id == UUID(data['id'])).first()
            if not work_item:
                raise Exception("Work Item not found.")
            
            hasChildren = session.query(WorkItems).filter(WorkItems.parent == work_item.id).first()
            if hasChildren:
                raise Exception(self.error_message[work_item.type])
            
            if work_item:
                session.delete(work_item)
                session.commit()
                return {"deleted": True}
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception(str(e))