from ariadne import QueryType
from utils.utils import has_permission
from services.work_items import GetWorkItems

query = QueryType()

@query.field("getWorkItems")
@has_permission("org:board:read")
def resolve_get_work_items(*args):
    obj = GetWorkItems()
    return obj.get()

    

resolvers = [query]