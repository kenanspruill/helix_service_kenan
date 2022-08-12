from typing import Tuple

# noinspection PyPackageRequirements
from ariadne import graphql_sync

# noinspection PyPackageRequirements
from ariadne.constants import PLAYGROUND_HTML

# noinspection PyPackageRequirements
from flask.app import Flask

# noinspection PyPackageRequirements
from flask.globals import request

# noinspection PyPackageRequirements
from flask.json import jsonify

# noinspection PyPackageRequirements
from flask.wrappers import Response
from flask_cors import CORS, cross_origin

# an extension targeted at Gunicorn deployments for prometheus scraping in flask applications
from prometheus_flask_exporter.multiprocess import GunicornInternalPrometheusMetrics

from helix_service_kenan.api_schema import ApiSchema

app = Flask(__name__)

metrics = GunicornInternalPrometheusMetrics(app)
app.config["CORS_HEADERS"] = "Content-Type"
CORS(app, resources={r"/graphql": {"origins": "*"}}, max_age=360)


@app.route("/")
def hello() -> Tuple[str, int]:
    return "Use /graphql endpoint to test", 200


@app.route("/health")
def health() -> Tuple[str, int]:
    return "OK", 200


@app.route("/graphql", methods=["GET"])
@cross_origin(origin="*")
def graphql_playground() -> Tuple[str, int]:
    return PLAYGROUND_HTML, 200


@app.route("/graphql", methods=["POST"])
@cross_origin(origin="*")
def graphql_server() -> Tuple[Response, int]:
    data = request.get_json()
    print(f"API call [{request.remote_addr}] {data!r}")

    success, result = graphql_sync(
        ApiSchema.schema, data, context_value=request, debug=app.debug
    )

    status_code = 200 if success else 400
    return jsonify(result), status_code


if __name__ == "__main__":
    app.config["CORS_HEADERS"] = "Content-Type"
    CORS(app, resources={r"/graphql": {"origins": "*"}})
    app.run()
