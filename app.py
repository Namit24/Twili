from flask import Flask, request, redirect
from twilio.twiml.voice_response import VoiceResponse
import openai
import os
from dotenv import load_dotenv


load_dotenv()
app = Flask(__name__)

# Set your OpenAI API key
openai.api_key = os.getenv('OPENAI_API_KEY')

@app.route("/")
def home():
    return "Welcome to the Mental Health Chatbot! Call the /voice endpoint to interact."

@app.route("/voice", methods=["POST"])
def voice():
    response = VoiceResponse()
    user_input = request.form.get("SpeechResult", "").strip()

    if user_input:
        # Get AI response
        ai_response = get_ai_response(user_input)
        response.say(ai_response)
    else:
        # Prompt the user to speak
        response.say("Hello! Please tell me how I can assist you.")
        response.gather(input="speech", action="/voice", timeout=5)

    return str(response)

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}]
        )
        return response["choices"][0]["message"]["content"]
    except Exception as e:
        print(f"Error fetching AI response: {e}")
        return "Sorry, I encountered an issue while processing your request."

if __name__ == "__main__":
    app.run(debug=True)