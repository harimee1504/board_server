from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer
import uuid

from models.base import Base, UUIDType

class Sprints(Base):
    __tablename__ = 'sprints'
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    title = Column(String(128), nullable=False)
    description = Column(String(255), nullable=True)
    created_by = Column(String(50), nullable=False)
    updated_by = Column(String(50), nullable=False)
    current = Column(Boolean, default=False, nullable=False)
    org_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    iteration = Column(Integer, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "createdBy": self.created_by,
            "updatedBy": self.updated_by,
            "orgId": self.org_id,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "iteration": self.iteration
        }