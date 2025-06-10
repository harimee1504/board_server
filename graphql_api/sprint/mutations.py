from ariadne import MutationType
from utils.utils import has_permission
from services.sprint.create_sprint import create_sprint
from services.sprint.create_sprint_iteration import create_sprint_iteration


mutation = MutationType()

@mutation.field("createSprint")
@has_permission("org:board:create")
def resolve_create_sprint(_, __, input):
    return create_sprint(input)

@mutation.field("createSprintIteration")
@has_permission("org:board:create")
def resolve_create_sprint_iteration(_, __, input):
    return create_sprint_iteration(input)

@mutation.field("updateSprint")
@has_permission("org:board:update")
def resolve_update_sprint(_, __, input):
    return update_sprint(input)

@mutation.field("deleteSprint")
@has_permission("org:board:delete")
def resolve_delete_sprint(_, __, input):
    return delete_sprint(input)
    
resolvers = [mutation]