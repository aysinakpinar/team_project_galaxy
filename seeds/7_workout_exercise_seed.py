import sys, os
from datetime import datetime

# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from extension import db
from models.associations import WorkoutExercise
from app import create_app  

def seed_workout_exercises():
    # Workout and Exercise IDs
    workout_exercise_data = workout_exercise_data = [
    # Workout 1 - Legs
    (1, 11), (1, 12), (1, 13), (1, 14), (1, 15),
    # Workout 2 - Shoulders
    (2, 4), (2, 5), (2, 6), (2, 7), (2, 8),
    # Workout 3 - Back
    (3, 6), (3, 7), (3, 8), (3, 9), (3, 10),
    # Workout 4 - Arms
    (4, 9), (4, 8), (4, 17), (4, 18), (4, 19),
    # Workout 5 - Legs
    (5, 11), (5, 12), (5, 13), (5, 14), (5, 15),
    # Workout 6 - Core
    (6, 20), (6, 21), (6, 22), (6, 23), (6, 24),
    # Workout 7 - Cardio
    (7, 25), (7, 26), (7, 27),
    # Workout 8 - Flexibility
    (8, 28), (8, 29),
    # Workout 9 - Chest & Shoulders
    (9, 1), (9, 2), (9, 4), (9, 5), (9, 6),
    # Workout 10 - Back & Arms
    (10, 6), (10, 9), (10, 7), (10, 8),
    # Workout 11 - Legs & Core
    (11, 11), (11, 12), (11, 20), (11, 21), (11, 22),
    # Workout 12 - Full Body
    (12, 25), (12, 26), (12, 27), (12, 11), (12, 12),
    # Workout 13 - Upper Body
    (13, 1), (13, 2), (13, 4), (13, 5), (13, 6),
    # Workout 14 - Lower Body
    (14, 11), (14, 12), (14, 13), (14, 14),
    # Workout 15 - Chest
    (15, 1), (15, 2), (15, 3), (15, 4), (15, 5),
    # Workout 16 - Chest
    (16, 1), (16, 2), (16, 3), (16, 4), (16, 5),
    # Workout 17 - Shoulders
    (17, 4), (17, 5), (17, 6),
    # Workout 18 - Legs
    (18, 11), (18, 12), (18, 13),
    # Workout 19 - Cardio
    (19, 25), (19, 26), (19, 27),
    # Workout 20 - Back
    (20, 6), (20, 7), (20, 8),
    # Workout 21 - Arms
    (21, 9), (21, 8), (21, 10),
    # Workout 22 - Core
    (22, 20), (22, 21), (22, 22),
    # Workout 23 - Flexibility
    (23, 28), (23, 29),
    # Workout 24 - Chest & Shoulders
    (24, 1), (24, 2), (24, 4), (24, 5),
    # Workout 25 - Back & Arms
    (25, 6), (25, 9), (25, 7), (25, 8),
    # Workout 26 - Legs & Core
    (26, 11), (26, 12), (26, 20), (26, 21),
    # Workout 27 - Full Body
    (27, 25), (27, 26), (27, 27), (27, 11), (27, 12),
    # Workout 28 - Chest
    (28, 1), (28, 2), (28, 3),
    # Workout 29 - Shoulders
    (29, 4), (29, 5), (29, 6),
    # Workout 30 - Legs
    (30, 11), (30, 12), (30, 13),
    # Workout 31 - Flexibility
    (31, 28), (31, 29),
    # Workout 32 - Shoulders
    (32, 4), (32, 5),
    # Workout 33 - Back
    (33, 6), (33, 7),
    # Workout 34 - Core
    (34, 20), (34, 21),
    # Workout 35 - Cardio
    (35, 25), (35, 26),
    # Workout 36 - Back & Arms
    (36, 6), (36, 9), (36, 7), (36, 8),
    # Workout 37 - Legs & Core
    (37, 11), (37, 12), (37, 20), (37, 21),
    # Workout 38 - Full Body
    (38, 25), (38, 26), (38, 27), (38, 11), (38, 12),
    # Workout 39 - Upper Body
    (39, 1), (39, 2), (39, 4), (39, 5), (39, 6),
    # Workout 40 - Chest
    (40, 1), (40, 2), (40, 3),
    # Workout 41 - Shoulders
    (41, 4), (41, 5),
    # Workout 42 - Legs
    (42, 11), (42, 12),
    # Workout 43 - Flexibility
    (43, 28), (43, 29),
    # Workout 44 - Back
    (44, 6), (44, 7),
    # Workout 45 - Arms
    (45, 9), (45, 8),
    # Workout 46 - Core
    (46, 20), (46, 21),
    # Workout 47 - Cardio
    (47, 25), (47, 26),
    # Workout 48 - Chest & Shoulders
    (48, 1), (48, 2), (48, 4),
    # Workout 49 - Back & Arms
    (49, 6), (49, 9),
    # Workout 50 - Legs & Core
    (50, 11), (50, 12), (50, 20),
    # Workout 51 - Full Body
    (51, 25), (51, 26), (51, 27), (51, 11), (51, 12),
    # Workout 52 - Chest
    (52, 1), (52, 2), (52, 3),
    # Workout 53 - Shoulders
    (53, 4), (53, 5),
    # Workout 54 - Legs
    (54, 11), (54, 12),
    # Workout 55 - Cardio
    (55, 25), (55, 26),
    # Workout 56 - Back
    (56, 6), (56, 7),
    # Workout 57 - Arms
    (57, 9), (57, 8),
    # Workout 58 - Core
    (58, 20), (58, 21),
    # Workout 59 - Flexibility
    (59, 28), (59, 29),
    # Workout 60 - Chest & Shoulders
    (60, 1), (60, 2), (60, 4),
    # Workout 61 - Back & Arms
    (61, 6), (61, 9),
    # Workout 62 - Legs & Core
    (62, 11), (62, 12), (62, 20),
    # Workout 63 - Full Body
    (63, 25), (63, 26), (63, 27), (63, 11), (63, 12),
    # Workout 64 - Upper Body
    (64, 1), (64, 2), (64, 4), (64, 5),
    # Workout 65 - Lower Body
    (65, 11), (65, 12),
    # Workout 66 - Legs
    (66, 11), (66, 12),
    # Workout 67 - Core
    (67, 20), (67, 21),
    # Workout 68 - Chest
    (68, 1), (68, 2),
    # Workout 69 - Shoulders
    (69, 4), (69, 5),
    # Workout 70 - Back
    (70, 6), (70, 7),
    # Workout 71 - Flexibility
    (71, 28), (71, 29)
]

    
    # Create application context
    app = create_app()

    with app.app_context():
        # Clear existing workout exercises (optional)
        db.session.commit()

        # Insert the relationships into the WorkoutExercise table
        for workout_id, exercise_id in workout_exercise_data:
            workout_exercise_entry = WorkoutExercise(
                workout_id=workout_id,
                exercise_id=exercise_id,
                done=False  # Default value for 'done' is False
            )
            db.session.add(workout_exercise_entry)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded workout exercises!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding workout exercises: {str(e)}")

if __name__ == "__main__":
    seed_workout_exercises()
