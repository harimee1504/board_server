import os
from ariadne import graphql_sync
from api.graphql.main import create_schema
from flask import Flask, jsonify, request
from api.utils.utils import token_required
from flask_socketio import SocketIO

from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")
socketio = SocketIO(app, cors_allowed_origins="*")

schema = create_schema()

@app.route("/graphql", methods=["POST"])
@token_required
def graphql_server():
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

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT")) 