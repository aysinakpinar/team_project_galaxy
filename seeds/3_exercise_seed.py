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
        {
            "name": "Push-ups",
            "description": "Targets chest, shoulders, and triceps",
            "intensity": "Medium",
            "sets": 3,
            "reps": 15,
            "picture_path": "/static/images/exercises/pushups.jpg",
            "tutorial": "Start in a plank position with hands shoulder-width apart. Lower your body until your chest nearly touches the floor, keeping elbows at a 45-degree angle. Push back up to the starting position. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=IODxDxX7oi4)"
        },
        {
            "name": "Bench Press",
            "description": "Strengthens chest and triceps",
            "intensity": "High",
            "sets": 4,
            "reps": 10,
            "picture_path": "/static/images/exercises/benchpress.jpg",
            "tutorial": "Lie on a flat bench and grip the barbell slightly wider than shoulder-width. Lower the bar to your chest and press it back up. Maintain control throughout the movement. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=4Y2ZdHCOXok)"
        },
        {
            "name": "Dumbbell Fly",
            "description": "Chest isolation exercise",
            "intensity": "Medium",
            "sets": 3,
            "reps": 12,
            "picture_path": "/static/images/exercises/dumbbellfly.jpg",
            "tutorial": "Lie on a flat bench, hold dumbbells above your chest with slightly bent elbows, and lower them in a wide arc until you feel a stretch in your chest. Bring them back together. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=eozdVDA78K0)"
        },

        # **Shoulders**
        {
            "name": "Shoulder Press",
            "description": "Targets shoulders and triceps",
            "intensity": "Medium",
            "sets": 3,
            "reps": 12,
            "picture_path": "/static/images/exercises/shoulderpress.jpg",
            "tutorial": "Hold a dumbbell in each hand at shoulder height and press them straight overhead. Lower them back with control. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=Q7aSWDnMJkE)"
        },
        {
            "name": "Lateral Raises",
            "description": "Works lateral deltoids",
            "intensity": "Low",
            "sets": 3,
            "reps": 15,
            "picture_path": "/static/images/exercises/lateralraises.jpg",
            "tutorial": "Hold a dumbbell in each hand by your sides and raise your arms until they are parallel to the ground. Lower with control. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=3VcKaXpzqRo)"
        },

        # **Back**
        {
            "name": "Pull-ups",
            "description": "Builds upper body strength",
            "intensity": "High",
            "sets": 4,
            "reps": 8,
            "picture_path": "/static/images/exercises/pullups.jpg",
            "tutorial": "Grip the pull-up bar with palms facing away. Pull your body up until your chin is above the bar, then lower yourself slowly. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=eGo4IYlbE5g)"
        },
        {
            "name": "Deadlifts",
            "description": "Full-body exercise for posterior chain",
            "intensity": "High",
            "sets": 4,
            "reps": 6,
            "picture_path": "/static/images/exercises/deadlifts.jpg",
            "tutorial": "Stand with feet hip-width apart, grip the barbell, keep your back straight, and lift the weight by extending your hips and knees. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=1ZXobu7JvvE)"
        },

        # **Arms**
            {
        "name": "Bicep Curls",
        "description": "Strengthens biceps by isolating the muscle.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/bicepcurls.jpg",
        "tutorial": "Hold a dumbbell in each hand with your palms facing forward. Keep your elbows close to your torso and curl the dumbbells towards your shoulders by flexing your biceps. Slowly lower them back down. Avoid swinging for maximum effectiveness. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=ykJmrZ5v0Oo)"
    },
    {
        "name": "Hammer Curls",
        "description": "Targets both the biceps and forearms with a neutral grip.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/hammercurls.jpg",
        "tutorial": "Hold a dumbbell in each hand with your palms facing your torso (neutral grip). Keeping your elbows close to your body, curl the dumbbells up while maintaining a controlled motion. Lower them back down slowly. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=TwD-YGVP4Bk)"
    },
    {
        "name": "Tricep Dips",
        "description": "Targets the triceps and also engages the shoulders and chest.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/tricepdips.jpg",
        "tutorial": "Sit on the edge of a bench and place your hands shoulder-width apart beside your hips. Move your feet forward and lower your body by bending your elbows to a 90-degree angle. Push yourself back up to the starting position. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=0326dy_-CzM)"
    },

        # **Legs (Quads, Hamstrings, Glutes, Calves)**
        {
        "name": "Squats",
        "description": "A fundamental compound exercise that targets the quads, hamstrings, and glutes.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/squats.jpg",
        "tutorial": "Stand with your feet shoulder-width apart. Keep your chest up and core engaged. Lower your body by bending your knees and hips as if sitting into a chair, keeping your knees aligned with your toes. Push through your heels to return to the starting position. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=aclHkVaku9U)"
    },
    {
        "name": "Lunges",
        "description": "A unilateral leg exercise that strengthens the quads and glutes while improving balance.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/lunges.jpg",
        "tutorial": "Step forward with one leg and lower your hips until both knees are bent at about a 90-degree angle. Keep your chest up and your front knee aligned with your ankle. Push off with your front foot to return to the starting position. Repeat on the other leg. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=QOVaHwm-Q6U)"
    },
    {
        "name": "Step-ups",
        "description": "A functional movement that builds leg strength and balance.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/stepups.jpg",
        "tutorial": "Find a sturdy box or bench. Step up with one foot, pressing through your heel, and bring the other foot up to stand on the box. Step down carefully and repeat with the opposite leg. Maintain control and avoid pushing off too much with the trailing leg. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=PhF3gR0LRwM)"
    },
    {
        "name": "Romanian Deadlifts",
        "description": "A hip-hinge movement that primarily targets the hamstrings and glutes.",
        "intensity": "High",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/romaniandeadlifts.jpg",
        "tutorial": "Hold a barbell or dumbbells in front of you with a slight bend in the knees. Hinge at the hips, lowering the weights while keeping your back straight. Lower until you feel a stretch in your hamstrings, then engage your glutes to return to standing. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=RZrvjC5BeCc)"
    },
    {
        "name": "Glute Bridges",
        "description": "Strengthens the glutes and hamstrings while improving hip mobility.",
        "intensity": "Low",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/glutebridges.jpg",
        "tutorial": "Lie on your back with your knees bent and feet flat on the floor. Drive through your heels, lifting your hips towards the ceiling. Squeeze your glutes at the top, then slowly lower back down. Keep your core engaged throughout. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=8bbE64NuDTU)"
    },
    {
        "name": "Hip Thrusts",
        "description": "A powerful glute-building exercise that increases lower body strength.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/hipthrusts.jpg",
        "tutorial": "Sit with your upper back against a bench and place a barbell across your hips. Plant your feet firmly on the ground and thrust your hips upward until your thighs are parallel to the floor. Squeeze your glutes at the top, then lower back down. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=SEdqd1n0cvg)"
    },
    {
        "name": "Bulgarian Split Squats",
        "description": "A challenging unilateral leg exercise that targets the quads and glutes.",
        "intensity": "High",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/bulgariansplitsquats.jpg",
        "tutorial": "Stand a few feet away from a bench and place one foot behind you on it. Lower your hips until your front thigh is parallel to the ground, then press through your front foot to stand back up. Keep your torso upright and balanced. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=2C-uNgKwPLE)"
    },
    {
        "name": "Standing Calf Raises",
        "description": "A simple exercise that strengthens and defines the calf muscles.",
        "intensity": "Low",
        "sets": 3,
        "reps": 15,
        "picture_path": "/static/images/exercises/calfraises.jpg",
        "tutorial": "Stand tall with your feet hip-width apart. Raise your heels off the ground as high as possible while keeping your legs straight. Hold for a moment at the top, then slowly lower back down. You can hold weights for added resistance. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=-M4-G8p8fmc)"
    },
    {
        "name": "Seated Calf Raises",
        "description": "Isolates the soleus muscle for deeper calf development.",
        "intensity": "Low",
        "sets": 3,
        "reps": 15,
        "picture_path": "/static/images/exercises/seatedcalfraises.jpg",
        "tutorial": "Sit on a calf raise machine or bench with a weight on your knees. Press through the balls of your feet to lift your heels as high as possible, then slowly lower back down. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=5yWaNOvgFCM)"
    },

        # **Core**
            {
        "name": "Plank",
        "description": "An isometric exercise that engages the core and lower back, improving endurance and stability.",
        "intensity": "Low",
        "sets": 3,
        "reps": 1,
        "duration": "30-60 seconds",
        "picture_path": "/static/images/exercises/plank.jpg",
        "tutorial": "Start in a forearm or high push-up position. Keep your body straight from head to heels, engage your core, and avoid sagging or raising your hips. Hold for the desired duration while maintaining tight core engagement. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=BQu26ABuVS0)"
    },
    {
        "name": "Bicycle Crunches",
        "description": "A dynamic ab exercise that targets the rectus abdominis and obliques.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/bicyclecrunches.jpg",
        "tutorial": "Lie on your back with hands behind your head. Lift your shoulders off the ground and bring your right elbow towards your left knee while extending the right leg. Switch sides in a pedaling motion. Keep your core tight and movements controlled. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=9FGilxCbdz8)"
    },
    {
        "name": "Russian Twists",
        "description": "A rotational core movement that works the obliques and stabilizing muscles.",
        "intensity": "Medium",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/russiantwists.jpg",
        "tutorial": "Sit on the floor with knees bent, lean back slightly, and lift your feet off the ground (for added difficulty). Hold a weight or clasp your hands together. Rotate your torso from side to side, engaging your obliques. Avoid using momentum. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=wkD8rjkodUI)"
    },
    {
        "name": "Side Planks",
        "description": "A core stability exercise that primarily strengthens the obliques.",
        "intensity": "Low",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/sideplanks.jpg",
        "tutorial": "Lie on your side with your elbow directly under your shoulder. Lift your hips off the ground, creating a straight line from head to feet. Keep your core tight and hold the position. Switch sides and repeat. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=K3_HmjKJv5M)"
    },
    {
        "name": "Hanging Leg Raises",
        "description": "A challenging lower ab exercise that strengthens the core and hip flexors.",
        "intensity": "High",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/hanginglegraises.jpg",
        "tutorial": "Hang from a pull-up bar with a firm grip. Engage your core and slowly lift your legs to a 90-degree angle or higher. Lower them back down with control. Avoid swinging for momentum. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=JB2oyawG9KI)"
    },

        # **Cardio**
        {
        "name": "Jumping Jacks",
        "description": "A full-body cardio exercise that improves heart rate, coordination, and endurance.",
        "intensity": "High",
        "sets": 3,
        "reps": 20,
        "picture_path": "/static/images/exercises/jumpingjacks.jpg",
        "tutorial": "Stand upright with feet together and hands at your sides. Jump while spreading your legs and raising your arms overhead. Return to the starting position and repeat in a rhythmic motion. Keep a steady pace for maximum cardiovascular benefit. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=c4DAnQ6DtF8)"
    },
    {
        "name": "Burpees",
        "description": "A high-intensity exercise that combines strength and cardio, targeting the whole body.",
        "intensity": "High",
        "sets": 3,
        "reps": 12,
        "picture_path": "/static/images/exercises/burpees.jpg",
        "tutorial": "Start in a standing position, squat down, and place your hands on the ground. Jump your feet back into a push-up position, perform a push-up (optional), then jump your feet forward and explode upwards into a jump. Land softly and repeat. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=TU8QYVW0gDU)"
    },
    {
        "name": "Mountain Climbers",
        "description": "A core-engaging cardio exercise that mimics a running motion in a plank position.",
        "intensity": "High",
        "sets": 3,
        "reps": 15,
        "picture_path": "/static/images/exercises/mountainclimbers.jpg",
        "tutorial": "Start in a high plank position with hands directly under shoulders. Bring one knee toward your chest, then quickly switch legs, keeping a fast and controlled pace. Maintain a tight core and avoid bouncing hips. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=nmwgirgXLYM)"
    },
       # **Flexibility & Mobility**
        {
        "name": "Yoga Stretch",
        "description": "A basic stretch that improves overall flexibility, focusing on increasing joint mobility and lengthening muscles.",
        "intensity": "Low",
        "sets": 2,
        "reps": 1,
        "picture_path": "/static/images/exercises/yogastretch.jpg",
        "tutorial": "Start in a seated position with your legs extended. Slowly bend forward at the hips and try to touch your toes. Focus on breathing deeply and hold the position to stretch the hamstrings and lower back. Keep your back straight to avoid strain. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=5zJ4F8C1TkM)"
    },
    {
        "name": "Cat-Cow Pose",
        "description": "A yoga sequence that improves spinal flexibility and mobility, helps relieve tension, and stretches the back and neck.",
        "intensity": "Low",
        "sets": 3,
        "reps": 10,
        "picture_path": "/static/images/exercises/catcow.jpg",
        "tutorial": "Start on your hands and knees with a neutral spine. Inhale as you arch your back (cow pose), lifting your head and tailbone. Exhale as you round your spine (cat pose), tucking your chin and tailbone. Repeat the sequence in a controlled manner to increase spinal flexibility. \n\n[Watch Tutorial](https://www.youtube.com/watch?v=kqnua4mDvz0)"
    }
    ]
    app = create_app()

    with app.app_context():
        db.session.commit()

        for exercise_data in exercises:
            exercise = ExerciseModel(
                name=exercise_data["name"],
                description=exercise_data["description"],
                intensity=exercise_data["intensity"],
                sets=exercise_data["sets"],
                reps=exercise_data["reps"],
                picture_path=exercise_data["picture_path"],
                tutorial=exercise_data["tutorial"],  # ✅ Added tutorial data
                created_at=datetime.now(),
                updated_at=datetime.now(),
            )
            db.session.add(exercise)
        
        try:
            db.session.commit()
            print("Successfully seeded exercises with tutorials!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding exercises: {str(e)}")

if __name__ == "__main__":
    seed_exercises()