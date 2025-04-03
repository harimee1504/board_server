from ariadne import QueryType
from utils.utils import sdk
from flask import session
from functools import lru_cache
from datetime import datetime, timedelta

query = QueryType()

def should_refresh_cache():
    """Check if cache needs refresh (every 5 minutes)"""
    now = datetime.now()
    if not hasattr(should_refresh_cache, 'last_refresh'):
        should_refresh_cache.last_refresh = now
        return True
    
    if now - should_refresh_cache.last_refresh > timedelta(minutes=5):
        should_refresh_cache.last_refresh = now
        return True
    return False

@lru_cache(maxsize=128)
def get_cached_users(org_id):
    """Get users list with caching"""
    organization_id = org_id
    users_list = sdk.organization_memberships.list(organization_id=organization_id)
    users = []
    for user in users_list.data:
        users.append({
            "id": user.public_user_data.user_id,
            "firstName": user.public_user_data.first_name,
            "lastName": user.public_user_data.last_name,
            "imageUrl": user.public_user_data.image_url,
            "email": user.public_user_data.identifier,
        })
    return users

@lru_cache(maxsize=128)
def get_cached_users_dict(org_id):
    """Get users list with caching"""
    organization_id = session["auth_state"]["org_id"]
    users_list = sdk.organization_memberships.list(organization_id=organization_id)
    users = {}
    for user in users_list.data:
        users[user.public_user_data.user_id] = {
            "id": user.public_user_data.user_id,
            "firstName": user.public_user_data.first_name,
            "lastName": user.public_user_data.last_name,
            "imageUrl": user.public_user_data.image_url,
            "email": user.public_user_data.identifier,
        }
    return users

@query.field("getUsers") 
def resolve_get_users(*args):
    organization_id = session["auth_state"]["org_id"]
    
    if should_refresh_cache():
        get_cached_users.cache_clear()
        
    return get_cached_users(organization_id)

resolvers = [query]