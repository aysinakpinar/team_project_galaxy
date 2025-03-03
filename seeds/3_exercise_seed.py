import sys
import os
from datetime import datetime
# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extension import db
from models.exercise import ExerciseModel
from app import create_app 

def seed_exercises():
    exercises = [
        # **Chest**
        {"name": "Push-ups", "description": "Targets chest, shoulders, and triceps", "intensity": "Medium", "sets": 3, "reps": 15, "picture_path": "/static/images/exercises/pushups.jpg"},
        {"name": "Bench Press", "description": "Strengthens chest and triceps", "intensity": "High", "sets": 4, "reps": 10, "picture_path": "/static/images/exercises/benchpress.jpg"},
        {"name": "Dumbbell Fly", "description": "Chest isolation exercise", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/dumbbellfly.jpg"},

        # **Shoulders**
        {"name": "Shoulder Press", "description": "Targets shoulders and triceps", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/shoulderpress.jpg"},
        {"name": "Lateral Raises", "description": "Works lateral deltoids", "intensity": "Low", "sets": 3, "reps": 15, "picture_path": "/static/images/exercises/lateralraises.jpg"},

        # **Back**
        {"name": "Pull-ups", "description": "Builds upper body strength", "intensity": "High", "sets": 4, "reps": 8, "picture_path": "/static/images/exercises/pullups.jpg"},
        {"name": "Deadlifts", "description": "Full-body exercise for posterior chain", "intensity": "High", "sets": 4, "reps": 6, "picture_path": "/static/images/exercises/deadlifts.jpg"},

        # **Arms**
        {"name": "Bicep Curls", "description": "Strengthens biceps", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/bicepcurls.jpg"},
        {"name": "Hammer Curls", "description": "Targets biceps and forearms", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/hammercurls.jpg"},
        {"name": "Tricep Dips", "description": "Targets triceps", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/tricepdips.jpg"},

        # **Legs (Quads, Hamstrings, Glutes, Calves)**
        {"name": "Squats", "description": "Targets quads, hamstrings, and glutes", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/squats.jpg"},
        {"name": "Lunges", "description": "Strengthens quads and glutes", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/lunges.jpg"},
        {"name": "Step-ups", "description": "Improves leg strength and balance", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/stepups.jpg"},
        {"name": "Romanian Deadlifts", "description": "Hamstring-focused movement", "intensity": "High", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/romaniandeadlifts.jpg"},
        {"name": "Glute Bridges", "description": "Strengthens glutes and hamstrings", "intensity": "Low", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/glutebridges.jpg"},
        {"name": "Hip Thrusts", "description": "Glute activation exercise", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/hipthrusts.jpg"},
        {"name": "Bulgarian Split Squats", "description": "Unilateral leg exercise", "intensity": "High", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/bulgariansplitsquats.jpg"},
        {"name": "Standing Calf Raises", "description": "Strengthens calves", "intensity": "Low", "sets": 3, "reps": 15, "picture_path": "/static/images/exercises/calfraises.jpg"},
        {"name": "Seated Calf Raises", "description": "Isolates the calf muscles", "intensity": "Low", "sets": 3, "reps": 15, "picture_path": "/static/images/exercises/seatedcalfraises.jpg"},

        # **Core**
        {"name": "Plank", "description": "Engages core and lower back", "intensity": "Low", "sets": 3, "reps": 1, "picture_path": "/static/images/exercises/plank.jpg"},
        {"name": "Bicycle Crunches", "description": "Targets abs and obliques", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/bicyclecrunches.jpg"},
        {"name": "Russian Twists", "description": "Works core and obliques", "intensity": "Medium", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/russiantwists.jpg"},
        {"name": "Side Planks", "description": "Builds oblique strength", "intensity": "Low", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/sideplanks.jpg"},
        {"name": "Hanging Leg Raises", "description": "Develops lower abs", "intensity": "High", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/hanginglegraises.jpg"},

        # **Cardio**
        {"name": "Jumping Jacks", "description": "Full-body cardio exercise", "intensity": "High", "sets": 3, "reps": 20, "picture_path": "/static/images/exercises/jumpingjacks.jpg"},
        {"name": "Burpees", "description": "High-intensity cardio and strength", "intensity": "High", "sets": 3, "reps": 12, "picture_path": "/static/images/exercises/burpees.jpg"},
        {"name": "Mountain Climbers", "description": "Cardio and core endurance", "intensity": "High", "sets": 3, "reps": 15, "picture_path": "/static/images/exercises/mountainclimbers.jpg"},

       # **Flexibility & Mobility**
        {"name": "Yoga Stretch", "description": "Improves flexibility", "intensity": "Low", "sets": 2, "reps": 1, "picture_path": "/static/images/exercises/yogastretch.jpg"},
        {"name": "Cat-Cow Pose", "description": "Spinal mobility exercise", "intensity": "Low", "sets": 3, "reps": 10, "picture_path": "/static/images/exercises/catcow.jpg"},
    ]
    app = create_app()

    with app.app_context():
        # Clear existing exercises (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new exercises
        for exercise_data in exercises:
            exercise = ExerciseModel(
                name=exercise_data["name"],
                description=exercise_data["description"],
                intensity=exercise_data["intensity"],
                sets=exercise_data["sets"],
                reps=exercise_data["reps"],
                picture_path=exercise_data["picture_path"],
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.session.add(exercise)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded exercises!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding exercises: {str(e)}")

if __name__ == "__main__":
    seed_exercises()