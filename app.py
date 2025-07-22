# bot_whatsapp_twilio_gpt/app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import openai
import os
app = Flask(__name__)

# Carga la clave de OpenAI desde variable de entorno
openai.api_key = os.getenv("OPENAI_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "")

    # Mensaje a GPT
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente para un centro de alquiler de quirófanos en Colombia. Responde de forma profesional y clara."},
            {"role": "user", "content": incoming_msg}
        ]
    )
    bot_response = response["choices"][0]["message"]["content"]

    # Crear respuesta de Twilio
    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    msg.body(bot_response)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)
