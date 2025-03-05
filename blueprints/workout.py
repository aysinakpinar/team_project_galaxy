from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from forms.add_exercise import AddExerciseForm
from extension import db
from models.exercise import ExerciseModel
from models.workout import WorkoutModel
from models.user import UserModel
from models.associations import WorkoutExercise

# 🏋️‍♂️ Create a new workout
workout = Blueprint("workout", __name__, url_prefix="/workout")

# Suggested exercises based on the user's profile
exercise_categories = {
    'chest': ["Push-ups", "Bench Press", "Dumbbell Fly"],
    'shoulders': ["Shoulder Press", "Lateral Raises"],
    'back': ["Pull-ups", "Deadlifts"],
    'arms': ["Bicep Curls", "Hammer Curls", "Tricep Dips"],
    'legs': ["Squats", "Lunges", "Step-ups", "Romanian Deadlifts", "Glute Bridges", "Hip Thrusts", "Bulgarian Split Squats", "Standing Calf Raises", "Seated Calf Raises"],
    'core': ["Plank", "Bicycle Crunches", "Russian Twists", "Side Planks", "Hanging Leg Raises"],
    'cardio': ["Jumping Jacks", "Burpees", "Mountain Climbers"],
    'flexibility': ["Yoga Stretch", "Cat-Cow Pose"]
}

def get_suggested_exercises():
    suggested_exercises = []

    # Retrieve the user_id from session
    user_id = session.get("user_id")

    if not user_id:
        raise ValueError("User not found in session.")

    # Fetch the current user from the database using the user_id
    current_user = UserModel.query.get(user_id)

    if not current_user:
        raise ValueError(f"No user found with ID: {user_id}")

    # Retrieve user's past workouts
    user_workouts = current_user.workouts

    # Fetch exercises associated with the user's past workouts
    past_exercises = db.session.query(ExerciseModel).join(WorkoutExercise).filter(
        WorkoutExercise.workout_id.in_([workout.id for workout in user_workouts])
    ).all()

    # Add these past exercises to the suggested list
    for exercise in past_exercises:
        if exercise not in suggested_exercises:
            suggested_exercises.append(exercise)

    # Add user's favorite exercises to the suggestions (if any)
    if current_user.favourite_exercise:
        favorite_exercises = ExerciseModel.query.filter(
            ExerciseModel.name.in_(current_user.favourite_exercise.split(','))
        ).all()
        for exercise in favorite_exercises:
            if exercise not in suggested_exercises:
                suggested_exercises.append(exercise)

    # If there are no past or favorite exercises, add exercises from predefined categories
    if not suggested_exercises:
        for category, exercises in exercise_categories.items():
            for exercise_name in exercises:
                # Avoid duplicates in the suggested list
                if exercise_name not in [exercise.name for exercise in suggested_exercises]:
                    exercise = ExerciseModel.query.filter_by(name=exercise_name).first()
                    if exercise and exercise not in suggested_exercises:
                        suggested_exercises.append(exercise)

    # Limit the suggested exercises to 3
    suggested_exercises = suggested_exercises[:3]

    print(f"Suggested exercises based on user profile: {suggested_exercises}")
    return suggested_exercises




@workout.route("/create", methods=["GET", "POST"])
def create_workout():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to create a workout.", "danger")
        return redirect(url_for("auth.login"))
    if request.method == "POST":
        # Get data from form
        workout_name = request.form.get("workout_name")
        estimated_time = request.form.get("estimated_time", "30 min")

        if not workout_name:
            flash("Workout name is required!", "warning")
            return redirect(url_for("workout.create_workout"))

        # Create and save new workout
        new_workout = WorkoutModel(name=workout_name, estimated_time=estimated_time, user_id=user_id)
        db.session.add(new_workout)
        db.session.commit()

        session["workout_id"] = new_workout.id  # Store in session for later use
        flash(f'Workout "{workout_name}" created successfully! Now add exercises.', "success")
        
        return redirect(url_for("workout.create_workout"))
    current_user = UserModel.query.get(user_id)
    user_workouts = current_user.workouts if current_user else []
    return render_template("create_workout.html", user=current_user, user_workouts=user_workouts)  # Render form on GET request

# 🏋️‍♀️ Manage Workout (Add Exercises + Show Workout List)
@workout.route('/manage_workout', methods=['GET', 'POST'])
def manage_workout():
    form = AddExerciseForm()

    # Fetch all exercises for the dropdown menu (manual addition)
    form.name.choices = [(exercise.id, exercise.name) for exercise in ExerciseModel.query.all()]

    # Retrieve the workout ID from session
    workout_id = session.get("workout_id")

    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current workout
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current user
    current_user = UserModel.query.get(session.get("user_id"))

    # Get suggested exercises based on user's profile
    suggested_exercises = get_suggested_exercises()  # Fetch the exercises from Mistral

    print(f"Suggested exercises from backend: {suggested_exercises}")
    # Process the manual form if it's submitted
    if form.validate_on_submit():
        selected_exercise = ExerciseModel.query.get(form.name.data)

        # Check if exercise already exists in the workout
        existing_entry = WorkoutExercise.query.filter_by(
            workout_id=workout_id, exercise_id=selected_exercise.id
        ).first()

        if not existing_entry:
            new_entry = WorkoutExercise(workout_id=workout_id, exercise_id=selected_exercise.id)
            db.session.add(new_entry)
            db.session.commit()
            flash(f'Added {selected_exercise.name} to "{current_workout.name}"!', 'success')
        else:
            flash("Exercise already exists in the workout!", "warning")

        return redirect(url_for('workout.manage_workout'))

    # Process the AI-suggested exercise if the user clicks 'Add' for any exercise
    if 'add_suggested_exercise' in request.form:
        exercise_id = request.form.get('suggested_exercise_id')
        selected_exercise = ExerciseModel.query.get(exercise_id)

        # Check if the exercise is already in the workout
        existing_entry = WorkoutExercise.query.filter_by(
            workout_id=workout_id, exercise_id=selected_exercise.id
        ).first()

        if not existing_entry:
            new_entry = WorkoutExercise(workout_id=workout_id, exercise_id=selected_exercise.id)
            db.session.add(new_entry)
            db.session.commit()
            flash(f'Added AI suggested exercise "{selected_exercise.name}" to the workout!', 'success')
        else:
            flash("Exercise already exists in the workout!", "warning")

        return redirect(url_for('workout.manage_workout'))

    # Fetch list of added exercises WITH WorkoutExercise objects
    workout_exercises = (
        db.session.query(WorkoutExercise)
        .join(ExerciseModel, WorkoutExercise.exercise_id == ExerciseModel.id)
        .filter(WorkoutExercise.workout_id == current_workout.id)
        .all()
    )
    print(f"Workout Exercises for {current_workout.name}: {workout_exercises}")
    return render_template(
        'manage_workout.html',
        form=form,
        workout=current_workout,
        workout_exercises=workout_exercises,  # Now contains WorkoutExercise objects
        suggested_exercises=suggested_exercises  # Display the suggested exercises
    )

#remove workout
@workout.route('/remove_workout/<int:workout_id>', methods=['POST'])
def remove_workout(workout_id):
    # Retrieve the workout ID from session
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to create a workout.", "danger")
        return redirect(url_for("auth.login"))
    
    current_user = UserModel.query.get(user_id)
    if not current_user:
        flash("You should log in.", "danger")
        return redirect(url_for("auth.login"))

    # Find the exercise in the workout
    workout_to_remove = WorkoutModel.query.get(workout_id)

    if not workout_to_remove:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    if workout_to_remove.user_id is None:
        flash("Workout has no owner and cannot be deleted.", "warning")
        return redirect(url_for("workout.create_workout"))

    if workout_to_remove.user_id != user_id:
        flash("You can only delete your own workouts.", "danger")
        return redirect(url_for("workout.create_workout"))
    
    db.session.delete(workout_to_remove)
    db.session.commit()

    flash("Workout deleted successfully!", "success")

    return redirect(url_for('workout.create_workout'))

@workout.route('/remove_exercise/<int:exercise_id>', methods=['POST'])
def remove_exercise(exercise_id):
    # Retrieve the workout ID from session
    workout_id = session.get("workout_id")

    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current workout
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    # Find the workout-exercise association
    exercise_to_remove = WorkoutExercise.query.filter_by(
        workout_id=workout_id, 
        exercise_id=exercise_id).first()
    exercise_name = exercise_to_remove.exercise.name  

    if exercise_to_remove:
        db.session.delete(exercise_to_remove)  # ✅ Correctly removes the association
        db.session.commit()
        flash(f'Removed {exercise_name} from "{current_workout.name}"!', 'success')
    else:
        flash("Exercise not found in workout.", "warning")

    return redirect(url_for('workout.manage_workout'))

@workout.route('/exercise_done/<int:exercise_id>', methods=['POST'])
def mark_done(exercise_id):
    # Retrieve the workout ID from session
    workout_id = session.get("workout_id")

    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current workout
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    # Find the exercise in the workout
    exercise_entry = WorkoutExercise.query.filter_by(
    workout_id=current_workout.id,
    exercise_id=exercise_id).first()

    if not exercise_entry:
        flash("Exercise not found in workout.", "warning")
        return redirect(url_for("workout.manage_workout"))

    # Toggle exercise completion status
    exercise_entry.done = not exercise_entry.done  
    db.session.commit()

    status = "done" if exercise_entry.done else "undone"
    flash(f"Exercise marked as {status}!", "success")

    return redirect(url_for("workout.manage_workout"))

@workout.route('/add_suggested_exercise', methods=['POST'])
def add_suggested_exercise():
    # Retrieve the workout ID from session
    workout_id = session.get("workout_id")

    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current workout
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    # Get the ID of the suggested exercise to be added
    exercise_id = request.form.get('suggested_exercise_id')
    if not exercise_id:
        flash("No exercise selected.", "danger")
        return redirect(url_for("workout.manage_workout"))

    # Fetch the exercise from the database
    selected_exercise = ExerciseModel.query.get(exercise_id)
    if not selected_exercise:
        flash("Exercise not found.", "danger")
        return redirect(url_for("workout.manage_workout"))

    # Check if the exercise already exists in the workout
    existing_entry = WorkoutExercise.query.filter_by(
        workout_id=workout_id, exercise_id=selected_exercise.id
    ).first()

    if existing_entry:
        flash("Exercise already exists in the workout!", "warning")
    else:
        # Create a new association in the WorkoutExercise table
        new_entry = WorkoutExercise(workout_id=workout_id, exercise_id=selected_exercise.id)
        db.session.add(new_entry)
        db.session.commit()
        flash(f'Added AI suggested exercise "{selected_exercise.name}" to the workout!', 'success')

    # Redirect back to the manage workout page
    return redirect(url_for('workout.manage_workout'))
