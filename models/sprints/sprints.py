from sqlalchemy import Column, String, DateTime, Boolean, ForeignKey, Integer, Date
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
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    initiative = Column(UUIDType, ForeignKey('work_items.id'), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "createdBy": self.created_by,
            "updatedBy": self.updated_by,
            "org_id": self.description,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "startDate": self.start_date,
            "endDate": self.end_date,
            "iteration": self.iteration,
            "initiative": self.initiative
        }