from datetime import datetime
import sys, os


# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extension import db
from models.user_point import UserPointModel
from app import create_app  

def seed_user_points():
    # Sample exercises data
    friendships = [
        {
            "weekly_points": 35,
            "monthly_points": 120,
            "yearly_points": 1000,
            "user_id": 1
        },
        {
            "weekly_points": 25,
            "monthly_points": 100,
            "yearly_points": 800,
            "user_id": 2
        },
        {
            "weekly_points": 15,
            "monthly_points": 50,
            "yearly_points": 500,
            "user_id": 3
        },
        {
            "weekly_points": 50,
            "monthly_points": 50,
            "yearly_points": 1500,
            "user_id": 4
        },
        {
            "weekly_points": 40,
            "monthly_points": 80,
            "yearly_points": 120,
            "user_id": 5
        },
        {
            "weekly_points": 5,
            "monthly_points": 15,
            "yearly_points": 300,
            "user_id": 6
        },
        {
            "weekly_points": 30,
            "monthly_points": 110,
            "yearly_points": 750,
            "user_id": 7
        },
        {
            "weekly_points": 35,
            "monthly_points": 120,
            "yearly_points": 900,
            "user_id": 8
        },
        {
            "weekly_points": 60,
            "monthly_points": 100,
            "yearly_points": 1000,
            "user_id": 9
        },
        {
            "weekly_points": 30,
            "monthly_points": 30,
            "yearly_points": 30,
            "user_id": 10
        },
        {
            "weekly_points": 25,
            "monthly_points": 50,
            "yearly_points": 50,
            "user_id": 11
        },
        {
            "weekly_points": 10,
            "monthly_points": 30,
            "yearly_points": 80,
            "user_id": 12
        },
        {
            "weekly_points": 5,
            "monthly_points": 10,
            "yearly_points": 20,
            "user_id": 13
        },
        {
            "weekly_points": 0,
            "monthly_points": 0,
            "yearly_points": 5,
            "user_id": 14
        },
    
]

    # Create application context
    app = create_app()

    with app.app_context():
        # Clear existing exercises (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new exercises
        for user_point_data in friendships:
            user_point = UserPointModel(
                weekly_points=user_point_data["weekly_points"],
                monthly_points=user_point_data["monthly_points"],
                yearly_points=user_point_data["yearly_points"],
                user_id= user_point_data["user_id"]
            )
            db.session.add(user_point)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded users!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding users: {str(e)}")

if __name__ == "__main__":
    seed_user_points()