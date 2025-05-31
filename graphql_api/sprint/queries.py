from ariadne import QueryType
from utils.utils import has_permission
from services.sprints.get_sprints import GetSprints

query = QueryType()

@query.field("getSprints")
@has_permission("org:board:read")
def resolve_get_sprints(_, info, input=None):
    obj = GetSprints()
    return obj.get(input)

resolvers = [query]