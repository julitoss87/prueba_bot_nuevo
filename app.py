from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import replicate
import os

app = Flask(__name__)

REPLICATE_API_TOKEN = os.environ.get("REPLICATE_API_TOKEN")

def responder_usuario(mensaje_usuario):
    if not REPLICATE_API_TOKEN:
        return "Error: No se encontró el token de Replicate. Asegúrate de configurarlo en Render."

    try:
        os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN
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
        return f"Ocurrió un error en el modelo: {str(e)}"

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    respuesta = responder_usuario(incoming_msg)
    twilio_resp = MessagingResponse()
    twilio_resp.message(respuesta)
    return str(twilio_resp)

@app.route("/", methods=["GET"])
def home():
    return "Servidor activo: chatbot IA (Mistral vía Replicate)"