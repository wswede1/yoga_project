from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from logging.config import dictConfig

from db.mysql_repository import MySQLRepository
from model.yoga_service import YogaService

# Logging configuration
dictConfig({
    'version': 1,
    'formatters': {'default': {
        'format': '[%(asctime)s] %(levelname)s in %(module)s: %(message)s',
    }},
    'handlers': {'wsgi': {
        'class': 'logging.StreamHandler',
        'stream': 'ext://flask.logging.wsgi_errors_stream',
        'formatter': 'default'
    }},
    'root': {
        'level': 'INFO',
        'handlers': ['wsgi']
    }
})

# Initialize the Flask app and configure CORS
app = Flask(__name__)
app.config['CORS_HEADERS'] = 'Content-Type'
cors = CORS(app, resources={r"/pose": {"origins": "http://localhost:port"}})

# Initialize the repository and service
repository = MySQLRepository()
yoga_service = YogaService(repository)


@app.route('/')
def doc() -> str:
    app.logger.info("doc - Got request")
    return render_template("index.html")


@app.route("/pose", methods=["GET"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def get_pose():
    raw_body_part = request.args.get('body_part', '')
    body_part = raw_body_part.strip().lower()
    app.logger.info(f"/pose - Got request for body part: {raw_body_part}")

    if not body_part:
        return jsonify({"error": "Body part is required"}), 400

    try:
        poses = yoga_service.get_poses_by_body_part(body_part)
    except Exception as exc:  # pragma: no cover - log unexpected failures
        app.logger.exception("Unhandled error retrieving poses")
        return jsonify({"error": "Unexpected error retrieving poses"}), 500

    if poses:
        app.logger.info(f"/pose - Found {len(poses)} poses for body part: {body_part}")
        return jsonify({"poses": poses}), 200

    app.logger.info(f"/pose - No poses found for body part: {body_part}")
    return jsonify({"message": "No poses found for this body part."}), 404


if __name__ == "__main__":
    app.logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', debug=True)
