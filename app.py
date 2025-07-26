import os
import requests
from flask import Flask, request, jsonify

# Obtener clave API de Groq
GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # O escribe directamente: "sk-..."

# Inicializar Flask
app = Flask(__name__)

# Función para generar respuesta usando Groq
def generar_respuesta_groq(mensaje, modelo="mixtral-8x7b-32768"):
    url = "https://api.groq.com/openai/v1/chat/completions"

    headers = {
        "Authorization": f"Bearer {GROQ_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": modelo,
        "messages": [
            {"role": "system", "content": "Eres un asistente útil y conversacional."},
            {"role": "user", "content": mensaje}
        ],
        "temperature": 0.7
    }

    try:
        response = requests.post(url, headers=headers, json=data)
        response.raise_for_status()
        respuesta = response.json()["choices"][0]["message"]["content"]
        return respuesta
    except requests.exceptions.HTTPError as http_err:
        print("[ERROR] HTTP error:", http_err.response.status_code, http_err.response.text)
        return "Lo siento, hubo un error HTTP generando la respuesta."
    except Exception as e:
        print("[ERROR] Otro error:", e)
        return "Lo siento, hubo un error generando la respuesta."

# Ruta raíz
@app.route('/')
def index():
    return "¡Hola desde el chatbot con Groq!"

# Webhook para Twilio
@app.route('/webhook', methods=['POST'])
def webhook():
    data = request.form
    mensaje = data.get("Body", "")
    respuesta = generar_respuesta_groq(mensaje)
    print("[INFO] Mensaje recibido:", mensaje)
    print("[INFO] Respuesta generada:", respuesta)
    return jsonify({"respuesta": respuesta})