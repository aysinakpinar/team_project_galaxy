from flask import Blueprint, render_template, request, flash, session
import ollama

chatbot = Blueprint('chatbot', __name__)

model_name = "mistral:7b-instruct-q4_K_M"

# Function to get response from Ollama chatbot API
def get_response(message):
    try:
        # Set loading state before making the API request
        session['loading'] = True
        session.modified = True  # Ensure the session is updated

        # Get the response from Ollama chatbot API
        response = ollama.chat(model_name, [{"role": "user", "content": message}])
        print("Ollama Response:", response)  # Log the full response
        
        content = response.get('message', {}).get('content', "Error: No valid response generated.")
        
        # Add to chat history
        if 'chat_history' not in session:
            session['chat_history'] = []

        session['chat_history'].append({'user_message': message, 'bot_response': content})

        # Clear loading state after processing the response
        session['loading'] = False
        session.modified = True  # Ensure session is saved
        return content
    except Exception as e:
        # Handle any exceptions that occur during the API call
        session['loading'] = False
        session.modified = True
        return f"Error: {str(e)}"

@chatbot.route('/ask', methods=['GET', 'POST'])
def chat_with_bot():
    user_message = ""
    bot_response = ""
    error_message = None

    if request.method == 'POST':
        user_message = request.form.get('message', '').strip()

        if not user_message:
            flash("Please ask a workout-related question!", "chatbot")
        else:
            try:
                # Get the response from the chatbot
                bot_response = get_response(user_message)

                # Handle response if it's empty
                if not bot_response:
                    bot_response = "Error: No valid response generated."
            except Exception as e:
                bot_response = f"Error: {str(e)}"
                error_message = "Sorry, there seems to be an issue with the bot. Please try again later."

    # Pass chat history, loading status, and bot response to template
    return render_template('chatbot.html', user_message=user_message, bot_response=bot_response, 
                        chat_history=session.get('chat_history', []), loading=session.get('loading', False), 
                        error_message=error_message)
