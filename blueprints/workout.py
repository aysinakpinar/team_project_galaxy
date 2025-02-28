from flask import Blueprint, render_template, redirect, url_for, flash, request, session
from forms.add_exercise import AddExerciseForm
from extension import db
from models.exercise import ExerciseModel
from models.workout import WorkoutModel
from models.user import UserModel


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

    # Fetch all exercises from the database for dropdown
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

    if form.validate_on_submit():
        selected_exercise = ExerciseModel.query.get(form.name.data)

        if selected_exercise and selected_exercise not in current_workout.exercises:
            current_workout.exercises.append(selected_exercise)
            db.session.commit()

            flash(f'Added {selected_exercise.name} to "{current_workout.name}"!', 'success')
        else:
            flash(f'Exercise already exists in the workout!', 'warning')

        return redirect(url_for('workout.manage_workout'))  # Stay on the page to refresh list

    # Fetch list of added exercises
    workout_exercises = current_workout.exercises  # ORM relationship

    return render_template('manage_workout.html', form=form, workout=current_workout, workout_exercises=workout_exercises)
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

    # Find the exercise in the workout
    exercise_to_remove = ExerciseModel.query.get(exercise_id)

    if exercise_to_remove and exercise_to_remove in current_workout.exercises:
        current_workout.exercises.remove(exercise_to_remove)
        db.session.commit()
        flash(f'Removed {exercise_to_remove.name} from "{current_workout.name}"!', 'success')
    else:
        flash("Exercise not found in workout.", "warning")

    return redirect(url_for('workout.manage_workout'))