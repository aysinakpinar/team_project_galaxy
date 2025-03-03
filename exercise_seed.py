from datetime import datetime
from extension import db
from app import create_app
from models.exercise import ExerciseModel

def seed_exercises():
    # Sample exercises data
    exercises = [
        {
            "name": "Push-ups",
            "description": "Basic upper body exercise targeting chest, shoulders, and triceps",
            "intensity": "Medium",
            "duration": "30 seconds",
            "picture_path": "/static/images/exercises/pushups.jpg",
        },
        {
            "name": "Squats",
            "description": "Lower body exercise targeting quads, hamstrings, and glutes",
            "intensity": "Medium",
            "duration": "45 seconds",
            "picture_path": "/static/images/exercises/squats.jpg",
        },
        {
            "name": "Plank",
            "description": "Core exercise engaging abdominal muscles and lower back",
            "intensity": "Low",
            "duration": "60 seconds",
            "picture_path": "/static/images/exercises/plank.jpg",
        },
        {
            "name": "Jumping Jacks",
            "description": "Full body cardio exercise",
            "intensity": "High",
            "duration": "30 seconds",
            "picture_path": "/static/images/exercises/jumpingjacks.jpg",
        },
        {
            "name": "Lunges",
            "description": "Lower body exercise targeting quads and glutes",
            "intensity": "Medium",
            "duration": "40 seconds",
            "picture_path": "/static/images/exercises/lunges.jpg",
        }
    ]

    # Create application context
    app = create_app()

    with app.app_context():
        db.session.commit()

        # Add new exercises
        for exercise_data in exercises:
            exercise = ExerciseModel(
                name=exercise_data["name"],
                description=exercise_data["description"],
                intensity=exercise_data["intensity"],
                duration=exercise_data["duration"],
                picture_path=exercise_data["picture_path"],
                created_at=datetime.now(),
                updated_at=datetime.now()
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