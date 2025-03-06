import os
from datetime import datetime
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extension import db
from models.workout import WorkoutModel
from models.user import UserModel  # Assuming you have a UserModel for users
from app import create_app 

def seed_workouts():
    # Define the workout list with categories
    workouts = [
        {"name": "Chest", "estimated_time": 45, "category": "Upper Body"},
        {"name": "Shoulders", "estimated_time": 40, "category": "Upper Body"},
        {"name": "Back", "estimated_time": 50, "category": "Upper Body"},
        {"name": "Arms", "estimated_time": 40, "category": "Upper Body"},
        {"name": "Legs", "estimated_time": 60, "category": "Lower Body"},
        {"name": "Core", "estimated_time": 30, "category": "Core"},
        {"name": "Cardio", "estimated_time": 35, "category": "Cardio"},
        {"name": "Flexibility", "estimated_time": 25, "category": "Flexibility"},
        {"name": "Chest & Shoulders", "estimated_time": 50, "category": "Upper Body"},
        {"name": "Back & Arms", "estimated_time": 55, "category": "Upper Body"},
        {"name": "Legs & Core", "estimated_time": 70, "category": "Full Body"},
        {"name": "Full Body", "estimated_time": 75, "category": "Full Body"},
        {"name": "Upper Body", "estimated_time": 60, "category": "Upper Body"},
        {"name": "Lower Body", "estimated_time": 60, "category": "Lower Body"},
    ]
    
    # Manually assign workouts to specific user IDs and other fields
    user_workouts = [
        {
            "user_id": 1,  # Assign to user with ID 1
            "workouts": [
                {"name": "Chest", "estimated_time": 45, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Shoulders", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs", "estimated_time": 60, "category": "Lower Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Cardio", "estimated_time": 35, "category": "Cardio", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 2,  # Assign to user with ID 2
            "workouts": [
                {"name": "Back", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Arms", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Core", "estimated_time": 30, "category": "Core", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Flexibility", "estimated_time": 25, "category": "Flexibility", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 3,  # Assign to user with ID 3
            "workouts": [
                {"name": "Chest & Shoulders", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Back & Arms", "estimated_time": 55, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs & Core", "estimated_time": 70, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Full Body", "estimated_time": 75, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 4,  # Assign to user with ID 4
            "workouts": [
                {"name": "Chest", "estimated_time": 45, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Arms", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs", "estimated_time": 60, "category": "Lower Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Flexibility", "estimated_time": 25, "category": "Flexibility", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 5,  # Assign to user with ID 5
            "workouts": [
                {"name": "Shoulders", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Back", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Core", "estimated_time": 30, "category": "Core", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Cardio", "estimated_time": 35, "category": "Cardio", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 6,  # Assign to user with ID 6
            "workouts": [
                {"name": "Back & Arms", "estimated_time": 55, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs & Core", "estimated_time": 70, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Full Body", "estimated_time": 75, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Upper Body", "estimated_time": 60, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 7,  # Assign to user with ID 7
            "workouts": [
                {"name": "Chest", "estimated_time": 45, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Shoulders", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs", "estimated_time": 60, "category": "Lower Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Flexibility", "estimated_time": 25, "category": "Flexibility", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 8,  # Assign to user with ID 8
            "workouts": [
                {"name": "Back", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Arms", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Core", "estimated_time": 30, "category": "Core", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Cardio", "estimated_time": 35, "category": "Cardio", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 9,  # Assign to user with ID 9
            "workouts": [
                {"name": "Chest & Shoulders", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Back & Arms", "estimated_time": 55, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs & Core", "estimated_time": 70, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Full Body", "estimated_time": 75, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 10,  # Assign to user with ID 10
            "workouts": [
                {"name": "Chest", "estimated_time": 45, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Shoulders", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs", "estimated_time": 60, "category": "Lower Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Cardio", "estimated_time": 35, "category": "Cardio", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 11,  # Assign to user with ID 11
            "workouts": [
                {"name": "Back", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Arms", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Core", "estimated_time": 30, "category": "Core", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Flexibility", "estimated_time": 25, "category": "Flexibility", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 12,  # Assign to user with ID 12
            "workouts": [
                {"name": "Chest & Shoulders", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Back & Arms", "estimated_time": 55, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs & Core", "estimated_time": 70, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Full Body", "estimated_time": 75, "category": "Full Body", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 13,  # Assign to user with ID 13
            "workouts": [
                {"name": "Upper Body", "estimated_time": 60, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Lower Body", "estimated_time": 60, "category": "Lower Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Legs", "estimated_time": 60, "category": "Lower Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Core", "estimated_time": 30, "category": "Core", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        },
        {
            "user_id": 14,  # Assign to user with ID 14
            "workouts": [
                {"name": "Chest", "estimated_time": 45, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Shoulders", "estimated_time": 40, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Back", "estimated_time": 50, "category": "Upper Body", "created_at": datetime.now(), "updated_at": datetime.now()},
                {"name": "Flexibility", "estimated_time": 25, "category": "Flexibility", "created_at": datetime.now(), "updated_at": datetime.now()}
            ]
        }
    ]
    
    app = create_app()

    with app.app_context():
        db.session.commit()

        # Loop through each user and manually assign the workouts
        for user_data in user_workouts:
            user_id = user_data["user_id"]
            workouts = user_data["workouts"]
            
            # Fetch the user by user_id
            user = UserModel.query.get(user_id)

            if user:
                for workout_data in workouts:
                    workout = WorkoutModel(
                        name=workout_data["name"],
                        estimated_time=workout_data["estimated_time"],
                        user_id=user.id,  # Assign workout to user
                        created_at=workout_data["created_at"],
                        updated_at=workout_data["updated_at"]
                    )
                    db.session.add(workout)

        try:
            db.session.commit()
            print("Successfully seeded workouts!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding workouts: {str(e)}")

if __name__ == "__main__":
    seed_workouts()
