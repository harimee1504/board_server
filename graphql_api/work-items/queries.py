from ariadne import QueryType
from utils.utils import has_permission
from services.work_items import GetWorkItems, GetActiveUserStories, GetSprintUserStories

query = QueryType()

@query.field("getWorkItems")
@has_permission("org:board:read")
def resolve_get_work_items(*args):
    obj = GetWorkItems()
    return obj.get()

@query.field("getActiveUserStories")
@has_permission("org:board:read")
def resolve_get_active_user_stories(*args):
    obj = GetActiveUserStories()
    return obj.get()

@query.field("getSprintUserStories")
@has_permission("org:board:read")
def resolve_get_sprint_user_stories(_, info, sprintId):
    obj = GetSprintUserStories(sprintId)
    return obj.get()

resolvers = [query]