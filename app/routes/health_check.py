from flask import Blueprint, jsonify

# This is the equivalent of 'healthCheckRoutes'
health_check_bp = Blueprint('health_check', __name__)

@health_check_bp.route('/healthcheck', methods=['GET'])
def handle_health_check():
    # This is the equivalent of your ApiResponse class structure
    response = {
        "statusCode": 200,
        "data": None,
        "message": "Server is up and running",
        "success": True
    }
    return jsonify(response), 200