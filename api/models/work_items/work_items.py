import uuid
from enum import Enum as PyEnum
from sqlalchemy import Column, String, DateTime, UUID, BIGINT, Enum, ForeignKey, Boolean, INTEGER, TEXT

from api.models.base import Base

class State(PyEnum):
    BACKLOG = "backlog"
    NEW = "new"
    ACTIVE = "active"
    ON_HOLD = "on_hold"
    IN_TEST = "in_test"
    ACCEPTED = "accepted"
    REJECTED = "rejected"
    CLOSED = "closed"

class ItemType(PyEnum):
    INITIATIVE = "initiative"
    EPIC = "epic"
    FEATURE = "feature"
    USER_STORY = "user_story"
    TASK = "task"
    BUG = "bug"

class StoryPoints(PyEnum):
    ONE = 1
    TWO = 2
    THREE = 3
    FIVE = 5
    EIGHT = 8
    THIRTEEN = 13

class Priority(PyEnum):
    P1 = "p1"
    P2 = "p2"
    P3 = "p3"
    P4 = "p4"
    P5 = "p5"

class WorkItems(Base):
    __tablename__ = 'work_items'
    id = Column(UUID, primary_key=True, default=uuid.uuid4)
    u_id = Column(BIGINT, nullable=False, unique=True, autoincrement=True)
    title = Column(String(30), nullable=False)
    description = Column(String(255), nullable=True)
    state = Column(Enum(State), nullable=True)
    type = Column(Enum(ItemType), nullable=False, index=True)
    created_by = Column(String(100), nullable=False)
    updated_by = Column(String(100), nullable=False)
    assigned_to = Column(String(100), nullable=False)
    org_id = Column(String(100), nullable=False, index=True)
    created_at = Column(DateTime, nullable=False)
    updated_at = Column(DateTime, nullable=False)
    spillover = Column(Boolean, default=False, nullable=False)
    initial_sprint = Column(UUID, ForeignKey('sprints.id'), nullable=True)
    current_sprint = Column(UUID, ForeignKey('sprints.id'), nullable=True)
    priority = Column(Enum(Priority), nullable=True)
    story_points = Column(Enum(StoryPoints), nullable=True)
    original_estimate = Column(INTEGER, nullable=True)
    remaining_estimate = Column(INTEGER, nullable=True)
    completed_estimate = Column(INTEGER, nullable=True)
    acceptance_criteria = Column(TEXT, nullable=True)
    definition_of_done = Column(TEXT, nullable=True)
    parent = Column(UUID, ForeignKey('work_items.id'), nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "u_id": self.u_id,
            "title": self.title,
            "description": self.description,
            "state": self.state.value if self.state else None,
            "type": self.type.value if self.type else None,
            "createdBy": self.created_by,
            "updatedBy": self.updated_by,
            "assignedTo": self.assigned_to,
            "org_id": self.org_id,
            "createdAt": self.created_at,
            "updatedAt": self.updated_at,
            "spillover": self.spillover,
            "initial_sprint": self.initial_sprint,
            "current_sprint": self.current_sprint,
            "priority": self.priority.value if self.priority else None,
            "story_points": self.story_points.value if self.story_points else None,
            "original_estimate": self.original_estimate,
            "remaining_estimate": self.remaining_estimate,
            "completed_estimate": self.completed_estimate,
            "acceptance_criteria": self.acceptance_criteria,
            "definition_of_done": self.definition_of_done,
            "parent": self.parent
        }