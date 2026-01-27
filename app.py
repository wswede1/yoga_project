from flask import Flask, request, jsonify, render_template
from flask_cors import CORS, cross_origin
from logging.config import dictConfig

from db.mysql_repository import MySQLRepository
from model.yoga_service import YogaService
from model.llm_client import LLMClientError

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

# Initialize the Flask app
app = Flask(__name__)
# CORS is only needed for the /pose API endpoint (kept for backward compatibility)
cors = CORS(app, resources={r"/pose": {"origins": "http://localhost:port"}})

# Initialize the repository and service
repository = MySQLRepository()
yoga_service = YogaService(repository)


@app.route('/', methods=['GET'])
def index():
    # Get body_part from query string (form submission)
    raw_body_part = request.args.get('body-part', '')
    custom_body_part = request.args.get('custom-body-part', '').strip()
    
    # Use custom input if provided, otherwise use dropdown selection
    body_part_input = custom_body_part if custom_body_part else raw_body_part
    body_part = body_part_input.strip().lower()
    
    poses = []
    error_message = None
    
    # If a search was performed, query the database
    if body_part:
        app.logger.info(f"Search request for body part: {body_part}")
        try:
            poses = yoga_service.get_poses_by_body_part(body_part)
            if poses:
                app.logger.info(f"Found {len(poses)} poses for body part: {body_part}")
            else:
                error_message = "No poses found for this body part. Try another focus area."
                app.logger.info(f"No poses found for body part: {body_part}")
        except Exception as exc:
            app.logger.exception("Unhandled error retrieving poses")
            error_message = "An error occurred while searching for poses. Please try again."
    else:
        # On initial page load, show sample results for "hips"
        try:
            poses = yoga_service.get_poses_by_body_part("hips")
            app.logger.info(f"Initial page load - showing {len(poses)} sample poses for 'hips'")
        except Exception as exc:
            app.logger.exception("Error loading initial sample poses")
    
    return render_template("index.html", 
                         poses=poses, 
                         selected_body_part=raw_body_part,
                         custom_body_part=custom_body_part,
                         error_message=error_message)


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


@app.route("/routine", methods=["POST"])
@cross_origin(origin='localhost', headers=['Content-Type', 'Authorization'])
def generate_routine():
    """
    Generate a yoga routine using LLM.
    
    Request JSON:
        {
            "body_parts": ["hips", "shoulders"],
            "duration_minutes": 15,
            "difficulty": "beginner"
        }
    
    Response JSON:
        {
            "segments": [{"text": "...", "weight": 2}, ...],
            "total_seconds": 900
        }
    """
    data = request.get_json()
    
    if not data:
        return jsonify({"error": "Request body must be JSON"}), 400
    
    body_parts = data.get("body_parts", [])
    duration_minutes = data.get("duration_minutes", 10)
    difficulty = data.get("difficulty", "beginner")
    
    # Validate body_parts is a list
    if not isinstance(body_parts, list):
        body_parts = [str(body_parts)] if body_parts else []
    
    # Validate duration_minutes is a positive integer
    try:
        duration_minutes = int(duration_minutes)
        if duration_minutes < 1:
            duration_minutes = 5
        elif duration_minutes > 120:
            duration_minutes = 120
    except (TypeError, ValueError):
        duration_minutes = 10
    
    # Validate difficulty
    if not isinstance(difficulty, str):
        difficulty = "beginner"
    
    app.logger.info(
        f"/routine - Generating routine: body_parts={body_parts}, "
        f"duration={duration_minutes}min, difficulty={difficulty}"
    )
    
    try:
        result = yoga_service.generate_routine(body_parts, duration_minutes, difficulty)
        app.logger.info(f"/routine - Generated {len(result['segments'])} segments")
        return jsonify(result), 200
    except LLMClientError as e:
        app.logger.error(f"/routine - LLM error: {str(e)}")
        return jsonify({"error": str(e)}), 503
    except Exception as e:
        app.logger.exception("/routine - Unexpected error")
        return jsonify({"error": "An unexpected error occurred"}), 500


if __name__ == "__main__":
    app.logger.info("Starting Flask application...")
    app.run(host='0.0.0.0', debug=True)
