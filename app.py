from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests
import os

app = Flask(__name__)

HF_TOKEN = os.getenv("HF_TOKEN")  # Debes configurar esto en Render

def generar_respuesta_hf(mensaje, modelo="mistralai/Mistral-7B-Instruct-v0.2"):
    url = "https://api-inference.huggingface.co/models/mistralai/Mistral-7B-Instruct-v0.1"

    headers = {
        "Authorization": f"Bearer {HF_TOKEN}",
        "Content-Type": "application/json"
    }

    payload = {
        "inputs": f"[INST] {mensaje} [/INST]"
    }

    try:
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        data = response.json()

        if isinstance(data, list) and "generated_text" in data[0]:
            return data[0]["generated_text"]
        else:
            return "Lo siento, no pude generar una respuesta."
    except requests.exceptions.RequestException as e:
        print("[ERROR] Falló la llamada a Hugging Face:", e)
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