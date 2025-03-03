from datetime import datetime
import sys, os


# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extension import db
from models.user import UserModel
from app import create_app  

def seed_users():
    # Sample exercises data
    users = [
        {
            "username": "IronMike",
            "description": "Strength training enthusiast focusing on powerlifting.",
            "password": "Galaxy7!",
            "email": "heavy_lifter@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344e7acb7fb9001e44ae0b.png",
            "location": "Liverpool",
            "age": 28,
            "weight": 90,
            "height": 5.10,
            "fitness_level": "advanced",
            "favourite_exercise": "deadlifts",
        },
        {
            "username": "SpartanRunner",
            "description": "Obstacle course racing and endurance training.",
            "password": "Galaxy7!",
            "email": "spartan_champ@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344c856c473c001d68c10b.png",
            "location": "London",
            "age": 26,
            "weight": 75,
            "height": 5.8,
            "fitness_level": "intermediate",
            "favourite_exercise": "rope climbs",
        },
        {
            "username": "BeastMode",
            "description": "Full-body HIIT workouts for endurance and strength.",
            "password": "Galaxy7!",
            "email": "beastmode@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344c856c473c001d68c10d.png",
            "location": "Manchester",
            "age": 35,
            "weight": 85,
            "height": 6.1,
            "fitness_level": "advanced",
            "favourite_exercise": "burpees",
        },
        {
            "username": "RunnerX",
            "description": "Long-distance runner training for marathons.",
            "password": "Galaxy7!",
            "email": "runnerx@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344c866c473c001d68c111.png",
            "location": "Boston",
            "age": 29,
            "weight": 70,
            "height": 5.9,
            "fitness_level": "intermediate",
            "favourite_exercise": "treadmill sprints",
        },
        {
            "username": "ZenMaster",
            "description": "Meditation and bodyweight training enthusiast.",
            "password": "Galaxy7!",
            "email": "zenmaster@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344c876c473c001d68c125.png",
            "location": "Liverpool",
            "age": 40,
            "weight": 65,
            "height": 5.7,
            "fitness_level": "beginner",
            "favourite_exercise": "tai chi",
        },
        {
            "username": "SwimKing",
            "description": "Professional swimmer training for competitions.",
            "password": "Galaxy7!",
            "email": "swimking@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344c876c473c001d68c126.png",
            "location": "London",
            "age": 23,
            "weight": 78,
            "height": 6.2,
            "fitness_level": "advanced",
            "favourite_exercise": "freestyle swimming",
        },
        {
            "username": "FitMom",
            "description": "Mom of two balancing fitness with family life.",
            "password": "Galaxy7!",
            "email": "fitmom@example.com",
            "profile_picture": "https://imgcdn.stablediffusionweb.com/2024/3/31/a07c234b-ab97-4ad4-96b1-e1e88ec45e45.jpg",
            "location": "Manchester",
            "age": 34,
            "weight": 68,
            "height": 5.6,
            "fitness_level": "intermediate",
            "favourite_exercise": "pilates",
        },
        {
            "username": "GainsBro",
            "description": "Bodybuilder focused on muscle gain and aesthetics.",
            "password": "Galaxy7!",
            "email": "gainsbro@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344e7acb7fb9001e44ae09.png",
            "location": "London",
            "age": 27,
            "weight": 100,
            "height": 5.11,
            "fitness_level": "advanced",
            "favourite_exercise": "bench press",
        },
        {
            "username": "CardioQueen",
            "description": "Loves cardio workouts and dance-based fitness.",
            "password": "Galaxy7!",
            "email": "cardioqueen@example.com",
            "profile_picture": "https://img.freepik.com/free-vector/happy-woman-with-blonde-hair_1308-171996.jpg?ga=GA1.1.1106893757.1741035910&semt=ais_hybrid",
            "location": "Bristol",
            "age": 31,
            "weight": 58,
            "height": 5.4,
            "fitness_level": "beginner",
            "favourite_exercise": "Zumba",
        },
        {
            "username": "HikingManiac",
            "description": "Outdoor enthusiast who loves mountain hikes.",
            "password": "Galaxy7!",
            "email": "hikingmaniac@example.com",
            "profile_picture": "https://img.freepik.com/free-vector/smiling-young-man-vector-illustration_1308-176659.jpg?ga=GA1.1.1106893757.1741035910&semt=ais_hybrid",
            "location": "Birmingham",
            "age": 37,
            "weight": 80,
            "height": 5.10,
            "fitness_level": "intermediate",
            "favourite_exercise": "trail running",
        },
        {
            "username": "CalisthenicsKing",
            "description": "Bodyweight exercises are the way to go.",
            "password": "Galaxy7!",
            "email": "calisthenics_pro@example.com",
            "profile_picture": "https://img.freepik.com/free-photo/portrait-man-cartoon-style_23-2151134022.jpg?ga=GA1.1.1106893757.1741035910&semt=ais_hybrid",
            "location": "Liverpool",
            "age": 31,
            "weight": 80,
            "height": 5.10,
            "fitness_level": "advanced",
            "favourite_exercise": "muscle-ups",
        },
        {
            "username": "MartialArtist",
            "description": "Mastering combat sports for fitness and self-defense.",
            "password": "Galaxy7!",
            "email": "karate_kid@example.com",
            "profile_picture": "https://res.cloudinary.com/jerrick/image/upload/d_642250b563292b35f27461a7.png,f_jpg,q_auto,w_720/67344c866c473c001d68c115.png",
            "location": "London",
            "age": 33,
            "weight": 85,
            "height": 5.11,
            "fitness_level": "advanced",
            "favourite_exercise": "kickboxing",
        },
        {
            "username": "StreetWorkout",
            "description": "Urban fitness and park workouts.",
            "password": "Galaxy7!",
            "email": "street_fit@example.com",
            "profile_picture": "https://img.freepik.com/free-photo/portrait-man-cartoon-style_23-2151134033.jpg?ga=GA1.1.1106893757.1741035910&semt=ais_hybrid",
            "location": "Birmingham",
            "age": 27,
            "weight": 78,
            "height": 5.9,
            "fitness_level": "intermediate",
            "favourite_exercise": "pull-ups",
        },
        {
            "username": "SpeedCyclist",
            "description": "Pushing limits on two wheels.",
            "password": "Galaxy7!",
            "email": "fast_cyclist@example.com",
            "profile_picture": "https://img.freepik.com/free-photo/funny-old-man-orange-jacket-glasses-3d-illustration_1057-45774.jpg?ga=GA1.1.1106893757.1741035910&semt=ais_hybrid",
            "location": "Liverpool",
            "age": 34,
            "weight": 74,
            "height": 5.10,
            "fitness_level": "intermediate",
            "favourite_exercise": "hill climbs",
        }
]

    # Create application context
    app = create_app()

    with app.app_context():
        # Clear existing exercises (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new exercises
        for user_data in users:
            user = UserModel(
                username=user_data["username"],
                description=user_data["description"],
                password=user_data["password"],
                email=user_data["email"],
                profile_picture=user_data["profile_picture"],
                location=user_data["location"],
                age=user_data["age"],
                weight=user_data["weight"],
                height=user_data["height"],
                fitness_level=user_data["fitness_level"],
                favourite_exercise=user_data["favourite_exercise"],
                created_at=datetime.now(),
            )
            db.session.add(user)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded users!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding users: {str(e)}")

if __name__ == "__main__":
    seed_users()