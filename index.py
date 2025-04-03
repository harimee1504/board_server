import os
from flask_cors import CORS
from ariadne import graphql_sync
from graphql_api.main import create_schema
from flask import Flask, jsonify, request
from utils.utils import token_required
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
             "max_age": 3600,
             "allow_credentials": True
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
        response.headers.add('Access-Control-Max-Age', '3600')
        return response

    # Apply token check only for POST requests
    @token_required
    def handle_post():
        try:
            data = request.get_json()
            success, result = graphql_sync(
                schema,
                data,
                context_value=request,
                debug=app.debug
            )

            if not success:
                return jsonify({
                    "errors": result
                }), 400

            if "errors" in result:
                return jsonify({
                    "errors": result["errors"]
                }), 400

            return jsonify(result)
        except Exception as e:
            return jsonify({
                "errors": [{"message": str(e)}]
            }), 500

    return handle_post()

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT")) 