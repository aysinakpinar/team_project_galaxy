from datetime import datetime
from extension import db
from app import create_app  # Replace 'your_app' with your actual Flask app name
from models.exercise import ExerciseModel

def seed_exercises():
    # Sample exercises data
    users = [
        {
            "username": "IronMike",
            "password": "Strength training enthusiast focusing on powerlifting.",
            "email": "heavy_lifter@example.com",
            "profile_picture": "",
            "location": "New York",
            "age": 28,
            "weight": 90,
            "height": "5'10\"",
            "fitness_level": "advanced",
            "favourite_exercise": "deadlifts",
        },
        {
            "username": "FlexiGirl",
            "password": "Yoga lover working on flexibility and core strength.",
            "email": "flexygirl@example.com",
            "profile_picture": "",
            "location": "Sydney",
            "age": 25,
            "weight": 60,
            "height": "5'5\"",
            "fitness_level": "intermediate",
            "favourite_exercise": "yoga",
        },
        {
            "username": "BeastMode",
            "password": "Full-body HIIT workouts for endurance and strength.",
            "email": "beastmode@example.com",
            "profile_picture": "",
            "location": "Chicago",
            "age": 35,
            "weight": 85,
            "height": "6'1\"",
            "fitness_level": "advanced",
            "favourite_exercise": "burpees",
        },
        {
            "username": "RunnerX",
            "password": "Long-distance runner training for marathons.",
            "email": "runnerx@example.com",
            "profile_picture": "",
            "location": "Boston",
            "age": 29,
            "weight": 70,
            "height": "5'9\"",
            "fitness_level": "intermediate",
            "favourite_exercise": "treadmill sprints",
        },
        {
            "username": "ZenMaster",
            "password": "Meditation and bodyweight training enthusiast.",
            "email": "zenmaster@example.com",
            "profile_picture": "",
            "location": "Tokyo",
            "age": 40,
            "weight": 65,
            "height": "5'7\"",
            "fitness_level": "beginner",
            "favourite_exercise": "tai chi",
        },
        {
            "username": "SwimKing",
            "password": "Professional swimmer training for competitions.",
            "email": "swimking@example.com",
            "profile_picture": "",
            "location": "Miami",
            "age": 23,
            "weight": 78,
            "height": "6'2\"",
            "fitness_level": "advanced",
            "favourite_exercise": "freestyle swimming",
        },
        {
            "username": "FitMom",
            "password": "Mom of two balancing fitness with family life.",
            "email": "fitmom@example.com",
            "profile_picture": "",
            "location": "Los Angeles",
            "age": 34,
            "weight": 68,
            "height": "5'6\"",
            "fitness_level": "intermediate",
            "favourite_exercise": "pilates",
        },
        {
            "username": "GainsBro",
            "password": "Bodybuilder focused on muscle gain and aesthetics.",
            "email": "gainsbro@example.com",
            "profile_picture": "",
            "location": "Las Vegas",
            "age": 27,
            "weight": 100,
            "height": "5'11\"",
            "fitness_level": "advanced",
            "favourite_exercise": "bench press",
        },
        {
            "username": "CardioQueen",
            "password": "Loves cardio workouts and dance-based fitness.",
            "email": "cardioqueen@example.com",
            "profile_picture": "",
            "location": "Paris",
            "age": 31,
            "weight": 58,
            "height": "5'4\"",
            "fitness_level": "beginner",
            "favourite_exercise": "Zumba",
        },
        {
            "username": "HikingManiac",
            "password": "Outdoor enthusiast who loves mountain hikes.",
            "email": "hikingmaniac@example.com",
            "profile_picture": "",
            "location": "Denver",
            "age": 37,
            "weight": 80,
            "height": "5'10\"",
            "fitness_level": "intermediate",
            "favourite_exercise": "trail running",
        }
]

    # Create application context
    app = create_app()

    with app.app_context():
        # Clear existing exercises (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new exercises
        for user_data in users:
            user = ExerciseModel(
                username=user_data["username"],
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
            print("Successfully seeded exercises!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding exercises: {str(e)}")

if __name__ == "__main__":
    seed_exercises()