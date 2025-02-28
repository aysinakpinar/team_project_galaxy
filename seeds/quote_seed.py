from flask_sqlalchemy import SQLAlchemy
from extension import db
from models.quote import QuoteModel
from app import create_app  # Replace 'your_app' with your actual Flask app name

def seed_quotes():
    quotes = [
        {
            "body": "“Push harder than yesterday if you want a different tomorrow.” Vincent Williams Sr."
        },
        {
            "body": "“The secret of getting ahead is getting started.” Mark Twain"
        },
        {
            "body": "“You miss one hundred percent of the shots you don’t take.” Wayne Gretzky"
        },
        {
            "body": "“All progress takes place outside the comfort zone.” Michael John Bobak"
        },
        {
            "body": "“Think of your workouts as important meetings you schedule with yourself. Bosses don’t cancel” Unknown"
        },
        {
            "body": "“Never give up on a dream just because of the time it will take to accomplish it. The time will pass anyway.” Earl Nightingale"
        },
        {
            "body": "“The only place where success comes before work is in the dictionary.”  Vidal Sassoon"
        }
    ]
    # Create application contex
    app = create_app()

    with app.app_context():
        # Clear existing exercises (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new exercises
        for quote_data in quotes:
            quote = QuoteModel(
                body=quote_data["body"],
            )
            db.session.add(quote)
        
        # Commit all changes
        try:
            db.session.commit()
            print("Successfully seeded quotes!")
        except Exception as e:
            db.session.rollback()
            print(f"Error seeding quotes: {str(e)}")

if __name__ == "__main__":
    seed_quotes()