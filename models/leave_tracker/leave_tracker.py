import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, String, Date, ForeignKey, INTEGER, CheckConstraint, text
from models.base import Base, UUIDType

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

class LeaveTracker(Base):
    __tablename__ = 'leave_tracker'

    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    user_id = Column(String(50), nullable=False)
    leave_period_id = Column(UUIDType, ForeignKey('leave_period.id'), nullable=False)
    org_id = Column(String(50), nullable=False)
    leave_date = Column(Date, nullable=False)
    leave_hours = Column(INTEGER, nullable=False)
    leave_type = Column(String(20), nullable=False)
    reason = Column(String(255), nullable=True)
    status = Column(String(20), default=Status.PENDING.value, nullable=False)
    updated_by = Column(String(50), nullable=False)
    created_at = Column(Date, nullable=False)
    updated_at = Column(Date, nullable=False)

    __table_args__ = (
        CheckConstraint(
            "leave_type IN ('planned', 'casual', 'unplanned', 'sick', 'half_day', 'mandatory', 'optional')",
            name='check_leave_type'
        ),
        CheckConstraint(
            "status IN ('pending', 'approved', 'rejected')",
            name='check_status'
        ),
    )
    
    def to_dict(self):
        return {
            "id": self.id,
            "userId": self.user_id,
            "leavePeriodId": self.leave_period_id,
            "orgId": self.org_id,
            "leaveDate": self.leave_date,
            "leaveHours": self.leave_hours,
            "leaveType": self.leave_type,
            "status": self.status,
            "updatedAt": self.updated_at
        }