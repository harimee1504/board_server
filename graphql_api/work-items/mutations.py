from ariadne import MutationType
from utils.utils import has_permission

from services.work_items import CreateWorkItem, UpdateWorkItem, DeleteWorkItem, UpdateWorkItemState

mutation = MutationType()

@mutation.field("createWorkItem")
@has_permission("org:board:create")
def resolve_create_work_item(_, __, input):
    obj = CreateWorkItem(input=input)
    return obj.create()

@mutation.field("updateWorkItem")
@has_permission("org:board:update")
def resolve_update_work_item(_, __, input):
    obj = UpdateWorkItem(input=input)
    return obj.update()

@mutation.field("deleteWorkItem")
@has_permission("org:board:delete")
def resolve_delete_work_item(_, __, input):
    obj = DeleteWorkItem(input=input)
    return obj.delete()

@mutation.field("updateWorkItemState")
@has_permission("org:board:update")
def resolve_update_work_item_state(_, __, input):
    obj = UpdateWorkItemState(input=input)
    return obj.update()
    
resolvers = [mutation]