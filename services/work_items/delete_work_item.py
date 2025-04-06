from models import WorkItems
from models.base import Session
import uuid

from models.work_items.work_items import ItemType

class DeleteWorkItem:
    def __init__(self, input):
        self.input = input
        self.error_message = {
            ItemType.INITIATIVE.value: "Initiative cannot be deleted because it contains associated child epic",
            ItemType.EPIC.value: "Epic cannot be deleted because it contains associated child feature",
            ItemType.FEATURE.value: "Feature cannot be deleted because it contains associated child user story",
            ItemType.USER_STORY.value: "User Story cannot be deleted because it contains associated child task or bug"
        }
                
    def delete(self):
        session = Session()
        try:
            work_item = session.query(WorkItems).filter(WorkItems.id == uuid.UUID(self.input['id'])).first()
            if not work_item:
                raise Exception("Work item not found.")
            
            hasChildren = session.query(WorkItems).filter(WorkItems.parent == work_item.id).first()
            if hasChildren:
                raise Exception(self.error_message[work_item.type])
            
            session.delete(work_item)
            session.commit()
            return {"deleted": True}
        except Exception as e:
            print(e)
            session.rollback()
            raise Exception("Failed to delete work item.")
        finally:
            session.close()