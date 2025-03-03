import sys
import os
# Add the project root to sys.path BEFORE imports
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))


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
        },
        {
            "body": "“There is no magic pill.” Arnold Schwarzenegger"
        },
        {
            "body": "“Success is usually a culmination of controlling failure.” Sylvester Stallone"
        },
        {
            "body": "“A year from now you may wish you had started today.” Karen Lamb"
        },
        {
            "body": "“Everyone's dream can come true if you just stick to it and work hard.” Serena Williams"
        },
        {
            "body": "“Acknowledge the fear and do it anyway.“ Emma Lovewell"
        }
    ]
    # Create application contex
    app = create_app()

    with app.app_context():
        # # Clear existing quotes (optional - remove if you want to keep existing data)
        db.session.commit()

        # Add new quotes
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