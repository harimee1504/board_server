from ariadne import MutationType
from utils.utils import has_permission
from services.tags import create_tag, update_tag, delete_tag

mutation = MutationType()

@mutation.field("createTag")
@has_permission("org:board:create")
def resolve_create_tag(_, __, input):
    return create_tag(input)

@mutation.field("updateTag")
@has_permission("org:board:update")
def resolve_update_tag(_, __, input):
    return update_tag(input)

@mutation.field("deleteTag")
@has_permission("org:board:delete")
def resolve_delete_tag(_, __, input):
    return delete_tag(input)

resolvers = [mutation]