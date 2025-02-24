from ariadne import QueryType
from api.utils.utils import sdk
from flask import session

query = QueryType()

@query.field("getUsers")
def resolve_get_users(*args):
    organization_id = session["auth_state"]["org_id"]
    users_list = sdk.users.list(organization_id=[organization_id])
    users = []
    for user in users_list:
        users.append({
            "id": user.id,
            "firstName": user.first_name,
            "lastName": user.last_name,
            "imageUrl": user.image_url,
            "email": user.email_addresses[0].email_address,
        })
    return users

resolvers = [query]