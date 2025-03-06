import sys
import os
# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


from flask_sqlalchemy import SQLAlchemy
from extension import db
from models.gym import GymModel
from app import create_app  # Replace 'your_app' with your actual Flask app name

def seed_gyms():
    gyms = [
        {
            "name": "Galaxy Gym",
            "picture_path": "https://media.istockphoto.com/id/654899206/photo/interior-of-modern-gym.jpg?s=612x612&w=0&k=20&c=ceWQahSTwGkGtQOFTpavOYAcAsnbOASjeoRzA6uZWFQ=",
            "user_id": 1,
            "location": "Liverpool",
            "lat": 53.373454,
            "lng": -2.938456,
        },
        {
            "name": "Big Bang Gym",
            "picture_path": "https://media.istockphoto.com/id/512753734/photo/3d-rendering-of-a-gym-interior-design.jpg?s=612x612&w=0&k=20&c=-NqI_14sMalmGfV78wuxRO9IA04c4YT1OjmGUbHMbsc=",
            "user_id": 9,
            "location": "Bristol",
            "lat": 51.454082,
            "lng": -2.577701,
        },
        {
            "name": "Milky Way",
            "picture_path": "https://media.istockphoto.com/id/2076695984/photo/3d-render-gym-fitness-yoga-pilates-studio.jpg?s=612x612&w=0&k=20&c=bc24OK5hHGoHlWg5SO4iOG5MR5hgOJJv-za9_TPomVM=",
            "user_id": 10,
            "location": "Birmingham",
            "lat": 52.480859,
            "lng": -1.902460,
        },
        {
            "name": "Solar Gym",
            "picture_path": "https://media.istockphoto.com/id/515238274/photo/modern-and-big-gym.jpg?s=612x612&w=0&k=20&c=E0sTLMBF5zUX5204SUwwCNf2vcRoAYp5CS60c2LvSKk=",
            "user_id": 5,
            "location": "Liverpool",
            "lat": 53.413580,
            "lng": -2.994577,
        }
    ]
    # Create application contex
    app = create_app()

    with app.app_context():
        # # Clear existing qgyms (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new gyms
        for gym_data in gyms:
            gym = GymModel(
                name = gym_data["name"],
                picture_path = gym_data["picture_path"],
                user_id = gym_data["user_id"],
                location = gym_data["location"],
                lat = gym_data["lat"],
                lng = gym_data["lng"]
            )
            db.session.add(gym)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded gyms!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding gyms: {str(e)}")

if __name__ == "__main__":
    seed_gyms()