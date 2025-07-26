from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from huggingface_hub import InferenceClient
import os

app = Flask(__name__)

# Inicializar cliente de Hugging Face con tu token
HF_TOKEN = os.getenv("HF_API_KEY")  # Asegúrate de que esta variable esté en Render
inference_client = InferenceClient(api_key=HF_TOKEN)

# Modelo a usar
MODEL_NAME = "m-a-p/SmolLM-3B-Instruct"

def generar_respuesta_hf(mensaje):
    try:
        messages = [{"role": "user", "content": mensaje}]
        completion = inference_client.chat.completions.create(
            model=MODEL_NAME,
            messages=messages,
            max_tokens=200,
            temperature=0.7,
        )
        return completion.choices[0].message.content
    except Exception as e:
        print(f"[ERROR] Falló la llamada a Hugging Face: {e}")
        return "Lo siento, hubo un error generando la respuesta."

@app.route("/webhook", methods=["POST"])
def webhook():
    mensaje_usuario = request.form.get("Body")
    print(f"[INFO] Mensaje recibido: {mensaje_usuario}")
    
    respuesta = generar_respuesta_hf(mensaje_usuario)
    print(f"[INFO] Respuesta generada: {respuesta}")
    
    twilio_response = MessagingResponse()
    twilio_response.message(respuesta)
    return str(twilio_response)

@app.route("/")
def home():
    return "Webhook de WhatsApp con SmolLM-3B activo"

if __name__ == "__main__":
    app.run(debug=True)
