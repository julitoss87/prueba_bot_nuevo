from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import replicate
import os

app = Flask(__name__)

# Recuperar API Token de Replicate
REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

# Generador de respuesta usando Mistral 7B
def responder_usuario(mensaje_usuario):
    if not REPLICATE_API_TOKEN:
        return "Error: No se encontró el token de Replicate."

    os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

    try:
        output = replicate.run(
            "mistralai/mistral-7b-instruct-v0.1:latest",
            input={
                "prompt": f"Usuario: {mensaje_usuario}\nAsistente:",
                "temperature": 0.7,
                "max_new_tokens": 150,
                "top_p": 0.9
            }
        )
        return "".join(output)
    except Exception as e:
        return f"Ocurrió un error: {str(e)}"

# Webhook para Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    respuesta = responder_usuario(incoming_msg)
    twilio_resp = MessagingResponse()
    twilio_resp.message(respuesta)
    return str(twilio_resp)

# Ruta base opcional
@app.route("/", methods=["GET"])
def home():
    return "Servidor activo: chatbot IA (Mistral vía Replicate)."