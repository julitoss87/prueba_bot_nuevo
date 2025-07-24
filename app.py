# app.py

from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
import os

# Inicializa Flask y OpenAI client
app = Flask(__name__)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").lower()
    sender = request.values.get("From", "")

    # Respuesta fija o condicional simple
    if "hola" in incoming_msg:
        respuesta = "Hola, ¿en qué puedo ayudarte hoy?"
    elif "precio" in incoming_msg:
        respuesta = "Nuestros precios varían según el procedimiento. ¿Qué tipo de cirugía te interesa?"
    else:
        respuesta = "Gracias por escribirnos. En breve un asesor te atenderá."

    # Enviar la respuesta al usuario
    twilio_response = MessagingResponse()
    twilio_response.message(respuesta)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)