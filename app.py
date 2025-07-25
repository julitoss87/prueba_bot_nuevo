import os
from flask import Flask, request
from huggingface_hub import InferenceClient
from twilio.twiml.messaging_response import MessagingResponse

# Carga el token de Hugging Face
HF_API_KEY = os.getenv("HF_API_KEY")

# Inicializa el cliente de Hugging Face
inference_client = InferenceClient(token=HF_API_KEY)

# ✅ Instancia de Flask (esta línea es la que faltaba)
app = Flask(__name__)

def generate_response(user_prompt: str, model: str = "TinyLlama/TinyLlama-1.1B-Chat-v1.0") -> str:
    try:
        completion = inference_client.text_generation(
            prompt=user_prompt,
            model=model,
            max_new_tokens=200,
            temperature=0.7
        )
        return completion
    except Exception as e:
        print(f"[ERROR] Falló la llamada a Hugging Face: {e}")
        return "Lo siento, hubo un error generando la respuesta."

# ✅ Ruta de Webhook de Twilio
@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get("Body", "").strip()
    print(f"[INFO] Mensaje recibido: {incoming_msg}")

    respuesta = generate_response(incoming_msg)
    print(f"[INFO] Respuesta generada: {respuesta}")

    twilio_response = MessagingResponse()
    twilio_response.message(respuesta)
    return str(twilio_response)