import uuid
from sqlalchemy import Column, ForeignKey, DateTime, String
from sqlalchemy.orm import relationship
from models.base import Base, UUIDType

class WorkItemTags(Base):
    __tablename__ = 'work_item_tags'
    
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    work_item_id = Column(UUIDType, ForeignKey('work_items.id', ondelete='CASCADE'), nullable=False, index=True)
    tag_id = Column(UUIDType, ForeignKey('tags.id', ondelete='CASCADE'), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    # Relationships
    work_item = relationship("WorkItems", back_populates="tags")
    tag = relationship("Tags", back_populates="work_items")

    def to_dict(self):
        return {
            "id": self.id,
            "workItemId": self.work_item_id,
            "tagId": self.tag_id,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        } 