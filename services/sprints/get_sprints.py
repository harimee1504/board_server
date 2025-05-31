from models.sprints.sprints import Sprints
from flask import session as flask_session
from models.base import Session
from graphql_api.users.queries import get_cached_users_dict

class GetSprints:
    def __init__(self):
        self.org_id = flask_session["auth_state"]["org_id"]
                
    def get(self, filter_input=None):
        session = Session()
        try:
            query = session.query(Sprints).filter(Sprints.org_id == self.org_id)
            
            # Apply filters if provided
            if filter_input and filter_input.get('by'):
                if filter_input['by'] == 'title' and filter_input.get('options', {}).get('title'):
                    query = query.filter(Sprints.title.ilike(f"%{filter_input['options']['title']}%"))
                elif filter_input['by'] == 'description' and filter_input.get('options', {}).get('description'):
                    query = query.filter(Sprints.description.ilike(f"%{filter_input['options']['description']}%"))
            
            sprints = query.all()
            new_sprints = []
            
            for sprint in sprints:
                temp = sprint.to_dict()
                # Get user information
                users_dict = get_cached_users_dict(self.org_id)
                temp["createdBy"] = users_dict.get(temp["createdBy"], {})
                temp["updatedBy"] = users_dict.get(temp["updatedBy"], {})
                
                # Add any missing fields required by the schema
                temp["orgId"] = sprint.org_id
                temp["initiative"] = None  # Add this if you have initiative data
                
                new_sprints.append(temp)
            session.commit()
            return new_sprints
        except Exception as e:
            print(f"Error in GetSprints: {str(e)}")
            session.rollback()
            raise Exception("Failed to get sprints.")
        finally:
            session.close() 