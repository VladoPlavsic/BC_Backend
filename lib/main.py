# from web3 import Web3
# 
# w3 = Web3(Web3.HTTPProvider('http://localhost:8545'))
# 
# print(w3.is_connected())
# print(w3.eth.get_block('latest'))


from flask import Flask
from flask_cors import CORS

app = Flask(__name__)
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

