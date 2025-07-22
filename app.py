# Nuevo import (para nueva API OpenAI >=1.0.0)
from openai import OpenAI
import os

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "")
    sender = request.values.get("From", "")

    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "Eres un asistente para un centro de alquiler de quirófanos en Colombia. Responde de forma profesional y clara."},
            {"role": "user", "content": incoming_msg}
        ]
    )

    bot_response = response.choices[0].message.content

    twilio_response = MessagingResponse()
    msg = twilio_response.message()
    msg.body(bot_response)

    return str(twilio_response)