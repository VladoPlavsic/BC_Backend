from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
app.config.update(TESTING=True, DEBUG=True)
cors = CORS(app, resource={r"*": {"origins": "*"}})

from lib.api import schema
from ariadne import graphql_sync, constants

from flask import request, jsonify

@app.route("/graphql", methods=["GET"])
def graphql_playground():
    return constants.PLAYGROUND_HTML, 200

@app.route("/graphql", methods=["POST"])
def graphql_server():
    data = request.get_json()
    success, result = graphql_sync(
        schema,
        data,
        context_value=request,
        debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code

