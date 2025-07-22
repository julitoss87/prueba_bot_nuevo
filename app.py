# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

# Inicializa Flask y OpenAI client
app = Flask(__name__)
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "")

    # Llama a GPT con el nuevo cliente
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente para un centro de alquiler de quirófanos en Colombia. Responde de forma profesional y clara."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    bot_response = response.choices[0].message.content

    # Construye la respuesta de Twilio
    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    msg.body(bot_response)

    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)