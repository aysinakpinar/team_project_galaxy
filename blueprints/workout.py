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
import re
import requests

workout = Blueprint("workout", __name__, url_prefix="/workout")

def get_suggested_exercises(workout_id):
    suggested_exercises = []
    user_id = session.get("user_id")
    if not user_id:
        raise ValueError("User not found in session.")
    current_user = UserModel.query.get(user_id)
    if not current_user:
        raise ValueError(f"No user found with ID: {user_id}")
    current_workout = WorkoutModel.query.get(workout_id)
    workout_exercises = db.session.query(WorkoutExercise).filter_by(workout_id=workout_id).all()
    existing_exercise_ids = [entry.exercise_id for entry in workout_exercises]
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
    workout_name = current_workout.name.lower()
    category_exercises = []
    if workout_name in exercise_categories:
        category_exercises = exercise_categories[workout_name]
    user_workouts = current_user.workouts
    past_exercises = db.session.query(ExerciseModel).join(WorkoutExercise).filter(
        WorkoutExercise.workout_id.in_([workout.id for workout in user_workouts])
    ).all()
    for exercise in past_exercises:
        if exercise.name in category_exercises and exercise.id not in existing_exercise_ids and exercise not in suggested_exercises:
            suggested_exercises.append(exercise)
    if current_user.favourite_exercise:
        favorite_exercises = ExerciseModel.query.filter(
            ExerciseModel.name.in_(current_user.favourite_exercise.split(','))
        ).all()
        for exercise in favorite_exercises:
            if exercise.name in category_exercises and exercise.id not in existing_exercise_ids and exercise not in suggested_exercises:
                suggested_exercises.append(exercise)
    if not suggested_exercises and category_exercises:
        for exercise_name in category_exercises:
            if exercise_name not in [exercise.name for exercise in suggested_exercises]:
                exercise = ExerciseModel.query.filter_by(name=exercise_name).first()
                if exercise and exercise.id not in existing_exercise_ids and exercise not in suggested_exercises:
                    suggested_exercises.append(exercise)
    if not category_exercises:
        for exercise in past_exercises:
            if exercise.id not in existing_exercise_ids and exercise not in suggested_exercises:
                suggested_exercises.append(exercise)
        if current_user.favourite_exercise:
            favorite_exercises = ExerciseModel.query.filter(
                ExerciseModel.name.in_(current_user.favourite_exercise.split(','))
            ).all()
            for exercise in favorite_exercises:
                if exercise.id not in existing_exercise_ids and exercise not in suggested_exercises:
                    suggested_exercises.append(exercise)
    suggested_exercises = suggested_exercises[:3]
    return suggested_exercises

@workout.route("/create", methods=["GET", "POST"])
def create_workout():
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to create a workout.", "danger")
        return redirect(url_for("auth.login"))

    if request.method == "POST":
        workout_name = request.form.get("workout_name")
        estimated_time = request.form.get("estimated_time", "10")  # Default value to '30' if not provided
        
        # Check if the estimated_time is a valid integer
        if not estimated_time.isdigit():  # Check if the value contains only digits
            flash("Estimated time must be a valid number.", "danger")
            return redirect(url_for("workout.create_workout"))
        
        estimated_time = int(estimated_time)  # Convert the string to an integer

        if not workout_name:
            flash("Workout name is required!", "warning")
            return redirect(url_for("workout.create_workout"))
        
        # Create the new workout
        new_workout = WorkoutModel(name=workout_name, estimated_time=estimated_time, user_id=user_id)
        db.session.add(new_workout)
        db.session.commit()

        session["workout_id"] = new_workout.id
        flash(f'Workout "{workout_name}" created successfully! Now add exercises.', "success")
        return redirect(url_for("workout.create_workout"))

    current_user = UserModel.query.get(user_id)
    user_workouts = current_user.workouts if current_user else []
    return render_template("create_workout.html", user=current_user, user_workouts=user_workouts)

@workout.route('/manage_workout/<int:workout_id>', methods=['GET', 'POST'])
def manage_workout(workout_id):
    form = AddExerciseForm()
    form.name.choices = [(exercise.id, exercise.name) for exercise in ExerciseModel.query.all()]

    current_workout = WorkoutModel.query.get_or_404(workout_id)
    current_user = UserModel.query.get(session.get("user_id"))
    suggested_exercises = get_suggested_exercises(workout_id)
    if form.validate_on_submit():
        selected_exercise = ExerciseModel.query.get(form.name.data)
        if not selected_exercise:
            flash("Selected exercise not found.", "danger")
            return redirect(url_for('workout.manage_workout', workout_id=workout_id))

        existing_entry = WorkoutExercise.query.filter_by(
            workout_id=workout_id, exercise_id=selected_exercise.id
        ).first()
        if not existing_entry:
            new_entry = WorkoutExercise(workout_id=workout_id, exercise_id=selected_exercise.id)
            db.session.add(new_entry)
            db.session.commit()
            flash(f'Added "{selected_exercise.name}" to "{current_workout.name}"!', 'success')
        else:
            flash("Exercise already exists in the workout!", "warning")
        return redirect(url_for('workout.manage_workout', workout_id=workout_id))
    workout_exercises = (
        db.session.query(WorkoutExercise)
        .join(ExerciseModel, WorkoutExercise.exercise_id == ExerciseModel.id)
        .filter(WorkoutExercise.workout_id == current_workout.id)
        .all()
    )
    return render_template(
        'manage_workout.html',
        form=form,
        workout=current_workout,
        workout_exercises=workout_exercises,
        suggested_exercises=suggested_exercises
    )

@workout.route('/remove_workout/<int:workout_id>', methods=['POST'])
def remove_workout(workout_id):
    user_id = session.get("user_id")
    if not user_id:
        flash("You must be logged in to create a workout.", "danger")
        return redirect(url_for("auth.login"))
    current_user = UserModel.query.get(user_id)
    if not current_user:
        flash("You should log in.", "danger")
        return redirect(url_for("auth.login"))
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

@workout.route('/remove_exercise/<int:workout_id>/<int:exercise_id>', methods=['POST'])
def remove_exercise(workout_id, exercise_id):
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))
    exercise_to_remove = WorkoutExercise.query.filter_by(
        workout_id=workout_id, 
        exercise_id=exercise_id).first()
    if exercise_to_remove:
        exercise_name = exercise_to_remove.exercise.name
        db.session.delete(exercise_to_remove)
        db.session.commit()
        flash(f'Removed {exercise_name} from "{current_workout.name}"!', 'success')
    else:
        flash("Exercise not found in workout.", "warning")
    return redirect(url_for('workout.manage_workout', workout_id=workout_id))


@workout.route('/exercise_done/<int:workout_id>/<int:exercise_id>', methods=['POST'])
def mark_done(workout_id, exercise_id):
    current_workout = WorkoutModel.query.get(workout_id)

    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))

    exercise_entry = WorkoutExercise.query.filter_by(
        workout_id=workout_id,
        exercise_id=exercise_id).first()

    if not exercise_entry:
        flash("Exercise not found in workout.", "warning")
        return redirect(url_for("workout.manage_workout", workout_id=workout_id))
    exercise_entry.done = not exercise_entry.done  

    db.session.commit()
    status = "done" if exercise_entry.done else "undone"
    flash(f"Exercise marked as {status}!", "success")
    


    # ------ ANALYTICS ----- | Michal |

    now = datetime.now(timezone.utc)
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
    print(00000)
    print(exercise_in_database)
    if exercise_in_database:
        db.session.delete(exercise_in_database)
        db.session.commit()
    # else add the exercise (the user presses done)
    else:
        db.session.add(exercise_analytics)
        db.session.commit()

    return redirect(url_for("workout.manage_workout", workout_id=workout_id))

@workout.route('/add_suggested_exercise', methods=['POST'])
def add_suggested_exercise():
    workout_id = request.form.get('workout_id')
    if not workout_id:
        flash("No workout selected. Please create a workout first.", "warning")
        return redirect(url_for("workout.create_workout"))
    current_workout = WorkoutModel.query.get(workout_id)
    if not current_workout:
        flash("Workout not found.", "danger")
        return redirect(url_for("workout.create_workout"))
    exercise_id = request.form.get('suggested_exercise_id')
    if not exercise_id:
        flash("No exercise selected.", "danger")
        return redirect(url_for("workout.manage_workout", workout_id=workout_id))
    selected_exercise = ExerciseModel.query.get(exercise_id)
    if not selected_exercise:
        flash("Exercise not found.", "danger")
        return redirect(url_for("workout.manage_workout", workout_id=workout_id))
    existing_entry = WorkoutExercise.query.filter_by(
        workout_id=workout_id, exercise_id=selected_exercise.id
    ).first()
    if existing_entry:
        flash("Exercise already exists in the workout!", "warning")
    else:
        new_entry = WorkoutExercise(workout_id=workout_id, exercise_id=selected_exercise.id)
        db.session.add(new_entry)
        db.session.commit()
        flash(f'Added AI suggested exercise "{selected_exercise.name}" to the workout!', 'success')
    return redirect(url_for('workout.manage_workout', workout_id=workout_id))

@workout.route('/exercise/tutorial/<int:exercise_id>', methods=['GET'])
def exercise_tutorial(exercise_id):
    exercise = ExerciseModel.query.get_or_404(exercise_id)
    
    # Assuming WorkoutExercise has a foreign key to Workout
    workout_exercise = WorkoutExercise.query.filter_by(exercise_id=exercise.id).first()
    
    # Get the workout related to this exercise
    workout = workout_exercise.workout if workout_exercise else None

    # Extract the video URL from the tutorial text
    tutorial_text = exercise.tutorial
    video_url = None
    video_data = None

    if tutorial_text:
        # Try to find a YouTube URL using regex
        match = re.search(r'https?://(?:www\.)?(?:youtube|vimeo)\.com/[^\s]+', tutorial_text)
        if match:
            url = match.group(0)
            
            # For YouTube URLs, convert them to embed format and fetch video metadata via oEmbed API
            if "youtube.com" in url:
                video_url = url.replace("https://www.youtube.com/watch?v=", "https://www.youtube.com/embed/").rstrip(')')

                # Use YouTube oEmbed API to get video details
                video_id = url.split('v=')[-1]
                oembed_url = f"https://www.youtube.com/oembed?url=https://www.youtube.com/watch?v={video_id}&format=json"
                try:
                    response = requests.get(oembed_url)
                    # Ensure the request was successful
                    if response.status_code == 200:
                        video_data = response.json()  # This contains video title, thumbnail, etc.
                    else:
                        print(f"Error fetching oEmbed data: {response.status_code}")
                except Exception as e:
                    print(f"Error while making request: {e}")

    # Pass the exercise, workout, and video data to the template
    return render_template('exercise_tutorial.html', exercise=exercise, workout=workout, video_url=video_url, video_data=video_data)


