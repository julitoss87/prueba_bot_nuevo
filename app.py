import os
from flask import Flask, request
from huggingface_hub import InferenceClient
from twilio.twiml.messaging_response import MessagingResponse

# Configura tu modelo (liviano y gratuito)
inference_client = InferenceClient(model="TinyLlama/TinyLlama-1.1B-Chat-v1.0")

# Inicializa la app Flask
app = Flask(__name__)

# Función para generar respuesta desde Hugging Face
def generate_response_api(user_prompt: str):
    try:
        messages = [{"role": "user", "content": user_prompt}]
        completion = inference_client.chat.completions.create(messages=messages)
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] Falló la llamada a Hugging Face: {e}")
        return "Lo siento, hubo un error generando la respuesta."

# Ruta del webhook de Twilio
@app.route("/webhook", methods=["POST"])
def whatsapp_webhook():
    incoming_msg = request.form.get("Body", "").strip()
    print(f"[INFO] Mensaje recibido: {incoming_msg}")

    response_text = generate_response_api(incoming_msg)
    print(f"[INFO] Respuesta generada: {response_text}")

    # Crea la respuesta TwiML para WhatsApp
    resp = MessagingResponse()
    resp.message(response_text)
    return str(resp)

# Ruta de test
@app.route("/", methods=["GET"])
def index():
    return "🟢 WhatsApp AI Chatbot está activo."
