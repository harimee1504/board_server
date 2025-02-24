from ariadne import QueryType
from api.utils.utils import has_permission
from api.services.tags import get_tags

query = QueryType()

@query.field("getTags")
@has_permission("org:board:read")
def resolve_get_tags(*_):
    return get_tags()

resolvers = [query]