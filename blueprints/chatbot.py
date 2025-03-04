import os
import openai
from flask import Blueprint, request, jsonify, render_template
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Define a Flask Blueprint
chatbot = Blueprint("chatbot", __name__, template_folder="../templates", url_prefix="/chatbot")

@chatbot.route("/")
def chatbot_home():
    return render_template("chatbot.html")

@chatbot.route("/ask", methods=["POST"])
def ask():
    user_question = request.form["question"]

    # OpenAI API call
    response = openai.ChatCompletion.create(
        model="gpt-4",
        messages=[{"role": "system", "content": "You are a fitness expert who provides workout advice."},
                {"role": "user", "content": user_question}]
    )

    answer = response["choices"][0]["message"]["content"]
    return jsonify({"answer": answer})
