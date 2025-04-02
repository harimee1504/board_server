import os
from flask_cors import CORS
from ariadne import graphql_sync
from api.graphql.main import create_schema
from flask import Flask, jsonify, request
from api.utils.utils import token_required
from flask_socketio import SocketIO

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

# Configure CORS with more permissive settings for development
CORS(app, 
     resources={
         r"/*": {
             "origins": ["http://localhost:3003"],
             "methods": ["GET", "POST", "OPTIONS"],
             "allow_headers": ["Content-Type", "Authorization", "Accept"],
             "expose_headers": ["Content-Type", "Authorization"],
             "supports_credentials": True,
             "max_age": 3600
         }
     },
     supports_credentials=True)

socketio = SocketIO(app, cors_allowed_origins="*")

schema = create_schema()

@app.route("/graphql", methods=["POST", "OPTIONS"])
def graphql_server():
    if request.method == "OPTIONS":
        response = jsonify({"message": "OK"})
        response.headers.add('Access-Control-Allow-Origin', 'http://localhost:3003')
        response.headers.add('Access-Control-Allow-Headers', 'Content-Type,Authorization,Accept')
        response.headers.add('Access-Control-Allow-Methods', 'POST,OPTIONS')
        response.headers.add('Access-Control-Allow-Credentials', 'true')
        return response

    # Apply token check only for POST requests
    @token_required
    def handle_post():
        data = request.get_json()
        _, result = graphql_sync(
            schema,
            data,
            context_value=request,
            debug=app.debug
        )

        if "errors" in result:
            error = result["errors"][0]
            return jsonify({
                "data": result["data"],
                "error": error["message"]
            })
        return jsonify(result)

    return handle_post()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT")) 