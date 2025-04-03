import uuid
from sqlalchemy import Column, Date
from models.base import Base, UUIDType

class LeavePeriod(Base):
    __tablename__ = 'leave_period'
    id = Column(UUIDType, primary_key=True, default=uuid.uuid4)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "startDate": self.start_date,
            "endDate": self.end_date
        }