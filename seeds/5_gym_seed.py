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
            "picture_path": "https://www.primalstrength.com/cdn/shop/files/gymdesign_render_Two_collumn_grid_cb1b5850-fa8e-4a7b-a2b3-190c2e45facd.jpg?v=1680719688&width=1500",
            "user_id": 1,
            "location": "Liverpool",
            "lat": "53.373454",
            "lng": "-2.938456",
        },
        {
            "name": "Big Bang Gym",
            "picture_path": "https://www.city.ac.uk/__data/assets/image/0005/639815/varieties/breakpoint-max.jpg",
            "user_id": 9,
            "location": "Bristol",
            "lat": "51.454082",
            "lng": "-2.577701",
        },
        {
            "name": "Milky Way",
            "picture_path": "https://i.pinimg.com/1200x/d7/f0/45/d7f045fcf5b29b5408e0335e06609dd4.jpg",
            "user_id": 10,
            "location": "Birmingham",
            "lat": "52.480859",
            "lng": "-1.902460",
        },
        
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