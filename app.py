from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")  # Debes configurar esto en Render

def generar_respuesta_hf(mensaje):
    import requests
    import json
    import os

    url = "https://api-inference.huggingface.co/models/m-a-p/SmalLM-3B-Instruct"
    headers = {
        "Authorization": f"Bearer {os.getenv('HF_API_KEY')}",  # Asegúrate de tener la clave en tus variables de entorno
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": f"[INST] {mensaje} [/INST]",
        "parameters": {
            "temperature": 0.7,
            "max_new_tokens": 200
        }
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()
        return data[0]["generated_text"]
    except requests.exceptions.RequestException as e:
        print(f"[ERROR] Falló la llamada a Hugging Face: {e}")
        return "Lo siento, hubo un error generando la respuesta."

@app.route("/webhook", methods=["POST"])
def webhook():
    mensaje = request.form.get("Body")
    numero = request.form.get("From")

    print("[INFO] Mensaje recibido:", mensaje)

    respuesta = generar_respuesta_hf(mensaje)

    print("[INFO] Respuesta generada:", respuesta)

    twilio_response = MessagingResponse()
    twilio_response.message(respuesta)
    return str(twilio_response)

if __name__ == "__main__":
    app.run(debug=True)