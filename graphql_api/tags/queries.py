from ariadne import QueryType
from utils.utils import has_permission
from services.tags import get_tags

query = QueryType()

@query.field("getTags")
@has_permission("org:board:read")
def resolve_get_tags(*_):
    return get_tags()

resolvers = [query]