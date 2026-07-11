from flask import Blueprint, request, jsonify
from analysis.analysis import analyze_performance
from database.db import save_report, get_student_by_name

api_bp = Blueprint('api', __name__)

@api_bp.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Extract values safely
        name = data.get('name', 'Unknown')
        cgpa = float(data.get('cgpa', 0.0))
        experience = int(data.get('coding_experience', 0))
        level = data.get('coding_level', 'Beginner')
        goal = data.get('career_goal', 'Not specified')

        # Run logic and get results
        results = analyze_performance(cgpa, experience, level)

        # Save to SQLite database
        save_report(
            name=name, 
            cgpa=cgpa, 
            experience=experience, 
            level=level, 
            goal=goal, 
            score=results['overall_score'], 
            category=results['category']
        )
        
        return jsonify(results), 200

    except Exception as e:
        print(f"Error in predict route: {e}")
        return jsonify({"error": "Internal server error"}), 500


@api_bp.route('/search/<name>', methods=['GET'])
def search_student(name):
    try:
        record = get_student_by_name(name)
        if record:
            return jsonify(record), 200
        else:
            return jsonify({"error": "Student not found"}), 404

    except Exception as e:
        print(f"Error in search route: {e}")
        return jsonify({"error": "Internal server error"}), 500