from flask import jsonify, session
from app.api import api_bp

@api_bp.route('/info', methods=['GET'])
def info():
    if 'loggedin' not in session or 'level' not in session:
        return jsonify({
            "success": False,
            "error": "Unauthorized or level not available"
        }), 401

    username = session.get('username', '')
    level = session.get('level', 1)

    return jsonify({
        "success": True,
        "username": username,
        "level": level
    })
