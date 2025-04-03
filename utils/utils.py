import os
from functools import wraps
from clerk_backend_api import Clerk
from flask import make_response, jsonify, request, session
from clerk_backend_api.jwks_helpers.authenticaterequest import AuthenticateRequestOptions
import httpx

sdk = Clerk(bearer_auth=os.getenv("CLERK_SECRET_KEY"))

def token_required(f):
    @wraps(f)
    def decorator(*args, **kwargs):
        token = None
        
        if 'Authorization' in request.headers and request.headers['Authorization'].startswith('Bearer '):
            token = request.headers['Authorization'].split(" ")[1]
        if not token:
            return make_response(jsonify({"message": "A valid token is missing!"}), 401)

        try:
            httpx_request = httpx.Request(
                method=request.method,
                url=str(request.url),
                headers=dict(request.headers),
            )
            auth_state = sdk.authenticate_request(
                httpx_request,
                AuthenticateRequestOptions(
                    audience=["convex","postmanToken"]
                )
            )
            if not auth_state.is_signed_in:
                return make_response(jsonify({"message": "Unauthorized - not signed in!"}), 401)
        except Exception as e:
            return make_response(jsonify({"message": f"Unauthorized - {str(e)}"}), 401)

        session["auth_state"] = auth_state.payload

        if "user_permissions" not in session:
            user_id = auth_state.payload["sub"]
            user_info = sdk.users.get(user_id=user_id)
            if "permissions" in user_info.private_metadata:
                session["user_permissions"] = user_info.private_metadata["permissions"]
            else:
                session["user_permissions"] = []
        return f(*args, **kwargs)
    return decorator

def has_permission(permission):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if permission not in session.get("user_permissions", []):
                raise Exception("User does not have permission or Forbidden!")
            return func(*args, **kwargs)
        return wrapper
    return decorator