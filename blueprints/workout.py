from flask import Blueprint, request, jsonify

workout = Blueprint('exercises', __name__, url_prefix='/workout')

# Mock database (in real app, you'd use a proper database)
exercises = []
workout_plans = {}

# add exercise
@workout.route('/exercise', methods=['POST'])
def add_exercise():
    """Add a new exercise"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Exercise name is required'}), 400
    
    exercise = {
        'id': len(exercises) + 1,
        'name': data['name'],
        'description': data.get('description', '')
    }
    exercises.append(exercise)
    return jsonify({'message': 'Exercise added', 'exercise': exercise}), 201


# find exercise
@workout.route('/exercise/<int:exercise_id>', methods=['GET'])
def find_exercise(exercise_id):
    """Find an exercise by ID"""
    exercise = next((e for e in exercises if e['id'] == exercise_id), None)
    if exercise:
        return jsonify(exercise), 200
    return jsonify({'error': 'Exercise not found'}), 404


# create workout plan
@workout.route('/plan', methods=['POST'])
def create_workout_plan():
    """Create a new workout plan"""
    data = request.get_json()
    if not data or 'name' not in data:
        return jsonify({'error': 'Plan name is required'}), 400
    
    plan_id = len(workout_plans) + 1
    workout_plans[plan_id] = {
        'id': plan_id,
        'name': data['name'],
        'exercises': []
    }
    return jsonify({'message': 'Workout plan created', 'plan': workout_plans[plan_id]}), 201


# add exercise to workout plan
@workout.route('/plan/<int:plan_id>/exercise/<int:exercise_id>', methods=['POST'])
def add_exercise_to_plan(plan_id, exercise_id):
    """Add an exercise to a workout plan"""
    if plan_id not in workout_plans:
        return jsonify({'error': 'Workout plan not found'}), 404
    
    exercise = next((e for e in exercises if e['id'] == exercise_id), None)
    if not exercise:
        return jsonify({'error': 'Exercise not found'}), 404
    
    workout_plans[plan_id]['exercises'].append(exercise)
    return jsonify({
        'message': 'Exercise added to plan',
        'plan': workout_plans[plan_id]
    }), 200


# delete exercise from workout plan
@workout.route('/plan/<int:plan_id>/exercise/<int:exercise_id>', methods=['DELETE'])
def delete_exercise_from_plan(plan_id, exercise_id):
    """Remove an exercise from a workout plan"""
    if plan_id not in workout_plans:
        return jsonify({'error': 'Workout plan not found'}), 404
    
    plan = workout_plans[plan_id]
    initial_length = len(plan['exercises'])
    plan['exercises'] = [e for e in plan['exercises'] if e['id'] != exercise_id]
    
    if len(plan['exercises']) < initial_length:
        return jsonify({
            'message': 'Exercise removed from plan',
            'plan': plan
        }), 200
    return jsonify({'error': 'Exercise not found in plan'}), 404