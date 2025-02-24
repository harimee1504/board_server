import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Date, UUID, ForeignKey, INTEGER, Enum

from api.models.base import Base

class LeaveType(PyEnum):
    PLANNED = "planned"
    CASUAL = "casual"
    UNPLANNED = "unplanned"
    SICK = "sick"
    HALF_DAY = "half_day"
    MANDATORY = "mandatory"
    OPTIONAL = "optional"

class Status(PyEnum):
    PENDING = "pending"
    APPROVED = "approved"
    REJECTED = "rejected"

class LeaveApprover(Base):
    __tablename__ = 'leave_approver'

    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(50), nullable=False)
    approver_id = Column(String(50), nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)
    
    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "approverId": self.approver_id,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at
        }