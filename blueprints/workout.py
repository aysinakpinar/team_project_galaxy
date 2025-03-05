from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from sqlalchemy import func
from forms.add_exercise import AddExerciseForm
from datetime import datetime, timezone
from extension import db
from models.exercise import ExerciseModel
from models.workout import WorkoutModel
from models.user import UserModel
from models.associations import WorkoutExercise
from models.exercise_analytics import ExerciseAnalyticsModel


# 🏋️‍♂️ Create a new workout
workout = Blueprint("workout", __name__, url_prefix="/workout")

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

    # Fetch all exercises for the dropdown menu
    form.name.choices = [(exercise.id, exercise.name) for exercise in ExerciseModel.query.all()]

    # Retrieve the workout ID from session
    workout_id = request.args.get("workout_id")

    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current workout
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

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

    # ✅ Fetch list of added exercises WITH WorkoutExercise objects
    workout_exercises = (
        db.session.query(WorkoutExercise)
        .join(ExerciseModel, WorkoutExercise.exercise_id == ExerciseModel.id)
        .filter(WorkoutExercise.workout_id == workout_id)
        .all()
    )

    # Debugging: Print fetched exercises
    print("Fetched exercises for workout:", [entry.exercise.name for entry in workout_exercises])

    return render_template(
        'manage_workout.html',
        form=form,
        workout=current_workout,
        workout_exercises=workout_exercises  # Now contains WorkoutExercise objects
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

@workout.route('/exercise_done/<int:exercise_id>/<int:workout_id>', methods=['POST'])
def mark_done(exercise_id, workout_id):
    # Retrieve the workout ID from session

    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))

    # Fetch the current workout
    current_workout = WorkoutModel.query.get(workout_id)

    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    # Find the exercise in the workout
    # exercise_entry = WorkoutExercise.query.filter(
    # WorkoutModel.id==current_workout.id,
    # ExerciseModel.id==exercise_id).first()
    exercise_entry = WorkoutExercise.query.filter_by(
    workout_id=current_workout.id, 
    exercise_id=exercise_id  
    ).first()

    if not exercise_entry:
        flash("Exercise not found in workout.", "warning")
        return redirect(url_for("workout.manage_workout"))

    # Toggle exercise completion status
    exercise_entry.done = not exercise_entry.done  

    db.session.commit()

    status = "done" if exercise_entry.done else "undone"
    flash(f"Exercise marked as {status}!", "success")

    # ------ ANALYTICS ----- | Michal |

    now = datetime.now(timezone.utc)
    print("-----------------------exercise id")
    print(exercise_entry.id)
    print("-----------------------exercise id")
    today_date = now.date()
    exercise_details = exercise_entry.exercise
    workout_details = exercise_entry.workout
    exercise_analytics = ExerciseAnalyticsModel(
        id=None, 
        completed_at=datetime.now(timezone.utc), 
        exercise_name=exercise_details.name, 
        intensity=exercise_details.intensity, 
        status="Done", 
        user_id = workout_details.user_id,
        workout_id=workout_details.id,
        workout_exercise_id=exercise_entry.id
    )

    # check if there's an exercise with today's date, same name and workout id
    exercise_in_database = ExerciseAnalyticsModel.query.filter(
        ExerciseAnalyticsModel.exercise_name == exercise_details.name,
        func.date(ExerciseAnalyticsModel.completed_at) == today_date,  # Extract date from completed_at
        ExerciseAnalyticsModel.workout_id == workout_details.id
    ).first()
    # if there's an exercise, remove it (when the user presses undone)

    if exercise_in_database:
        db.session.delete(exercise_in_database)
        db.session.commit()
    # else add the exercise (the user presses done)
    else:
        db.session.add(exercise_analytics)
        db.session.commit()

    return redirect(url_for("workout.manage_workout"))