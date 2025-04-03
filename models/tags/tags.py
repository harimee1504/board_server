import uuid
from sqlalchemy import Column, String, DateTime
from models.base import Base, UUIDType

class Tags(Base):
    __tablename__ = 'tags'
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    tag = Column(String(30), nullable=False)
    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)
    org_id = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "tag": self.tag,
            "orgId": self.org_id,
            "createdBy": self.created_by,
            "updatedBy": self.updated_by,
            "updatedAt": self.updated_at,
            "createdAt": self.created_at
        }