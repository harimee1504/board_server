import uuid
from sqlalchemy import Column, Date, UUID

from api.models.base import Base

class LeavePeriod(Base):
    __tablename__ = 'leave_period'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)

    def to_dict(self):
        return {
            "id": self.id,
            "startDate": self.start_date,
            "endDate": self.end_date
        }