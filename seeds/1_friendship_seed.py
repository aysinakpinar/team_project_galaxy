from datetime import datetime
import sys, os


# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extension import db
from models.friendship import FriendshipModel
from app import create_app  

def seed_friendships():
    # Sample exercises data
    friendships = [
        {
            "user_id": 1,
            "friend_id": 2,
            "status": "approved"
        },
        {
            "user_id": 1,
            "friend_id": 3,
            "status": "approved"
        },
        {
            "user_id": 1,
            "friend_id": 4,
            "status": "pending"
        },
        {
            "user_id": 1,
            "friend_id": 5,
            "status": "pending"
        },
        {
            "user_id": 1,
            "friend_id": 6,
            "status": "approved"
        },
        {
            "user_id": 1,
            "friend_id": 7,
            "status": "pending"
        },
        {
            "user_id": 1,
            "friend_id": 8,
            "status": "approved"
        },
        {
            "user_id": 2,
            "friend_id": 8,
            "status": "pending"
        },
        {
            "user_id": 2,
            "friend_id": 9,
            "status": "pending"
        },
        {
            "user_id": 2,
            "friend_id": 10,
            "status": "pending"
        },
        {
            "user_id": 2,
            "friend_id": 11,
            "status": "approved"
        },
        {
            "user_id": 3,
            "friend_id": 13,
            "status": "approved"
        },
        {
            "user_id": 3,
            "friend_id": 4,
            "status": "pending"
        },
        {
            "user_id": 3,
            "friend_id": 6,
            "status": "pending"
        },
        {
            "user_id": 3,
            "friend_id": 8,
            "status": "approved"
        },
        {
            "user_id": 3,
            "friend_id": 10,
            "status": "pending"
        },
        {
            "user_id": 4,
            "friend_id": 5,
            "status": "pending"
        },
        {
            "user_id": 4,
            "friend_id": 8,
            "status": "approved"
        },
        {
            "user_id": 4,
            "friend_id": 13,
            "status": "approved"
        },
        {
            "user_id": 4,
            "friend_id": 14,
            "status": "approved"
        },
        {
            "user_id": 5,
            "friend_id": 11,
            "status": "pending"
        },
        {
            "user_id": 5,
            "friend_id": 13,
            "status": "pending"
        },
        {
            "user_id": 5,
            "friend_id": 14,
            "status": "pending"
        },
        {
            "user_id": 6,
            "friend_id": 8,
            "status": "pending"
        },
        {
            "user_id": 6,
            "friend_id": 10,
            "status": "approved"
        },
        {
            "user_id": 6,
            "friend_id": 13,
            "status": "pending"
        },
        {
            "user_id": 6,
            "friend_id": 14,
            "status": "approved"
        },
        {
            "user_id": 7,
            "friend_id": 8,
            "status": "pending"
        },
        {
            "user_id": 7,
            "friend_id": 9,
            "status": "pending"
        },
        {
            "user_id": 7,
            "friend_id": 13,
            "status": "pending"
        }
]

    # Create application context
    app = create_app()

    with app.app_context():
        # Clear existing exercises (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new exercises
        for friendship_data in friendships:
            friendship = FriendshipModel(
                user_id=friendship_data["user_id"],
                friend_id=friendship_data["friend_id"],
                status=friendship_data["status"],
                created_at=datetime.now(),
            )
            db.session.add(friendship)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded users!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding users: {str(e)}")

if __name__ == "__main__":
    seed_friendships()