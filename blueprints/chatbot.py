import requests
import json
from flask import Blueprint, render_template, request, flash


chatbot = Blueprint('chatbot', __name__)

# Route to handle chatbot interactions
@chatbot.route('/chat_with_bot', methods=['GET', 'POST'])
def chat_with_bot():
    user_message = ""
    bot_response = ""

    if request.method == 'POST':
        user_message = request.form.get('message', '')

        if not user_message:
            flash("Please ask a workout-related question!", "warning")
        else:
            try:
                # Sending request to the local Ollama server
                response = requests.post(
                    "http://localhost:11434/api/generate",
                    json={"model": "mistral", "prompt": f"Answer this workout-related question: {user_message}"},
                    stream=True  # Enable streaming
                )

                # Check if the response is successful
                if response.status_code != 200:
                    bot_response = f"Error: Received non-200 status code {response.status_code} from server."
                    return render_template('chat_with_bot.html', user_message=user_message, bot_response=bot_response)

                
                print(f"Raw response: {response.text}")

                
                full_response = ""

                # Process the response as a stream of JSON objects
                for line in response.iter_lines():
                    if line:
                        try:
                            # Attempt to decode and parse each line as JSON
                            line_data = line.decode('utf-8')
                            
                            
                            if not line_data.strip():
                                continue
                            
                            # Attempt to parse the line as JSON
                            try:
                                json_data = json.loads(line_data)
                                if "response" in json_data:
                                    full_response += json_data["response"]
                            except ValueError as e:
                                
                                print(f"Error parsing chunk: {line_data} | Error: {str(e)}")
                                continue
                            
                        except Exception as e:
                    
                            print(f"Unexpected error: {str(e)}")

                # Final response after processing all chunks
                bot_response = full_response.strip()

                if not bot_response:
                    bot_response = "Error: No valid response generated."

            except Exception as e:
                bot_response = f"Error: {str(e)}"

    return render_template('chat_with_bot.html', user_message=user_message, bot_response=bot_response)
