import uuid
from sqlalchemy import Column, String, DateTime
from models.base import Base, UUIDType

class Boards(Base):
    __tablename__ = 'boards'
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    title = Column(String(50), nullable=False)
    description = Column(String(255), nullable=True)
    org_id = Column(String(50), nullable=False)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    created_by = Column(String(50), nullable=False)
    updated_by = Column(String(50), nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "org_id": self.org_id,
            "description": self.description,
            "createdBy": self.created_by,
            "updatedBy": self.updated_by,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }