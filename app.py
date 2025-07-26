import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Cargar el token de OpenRouter
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Error: No se encontró la variable OPENROUTER_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Prompt del sistema para dar contexto
        system_prompt = (
            "Eres un asistente profesional que responde en español, especializado en brindar información clara, útil y persuasiva "
            "para personas interesadas en servicios de salud, medicina estética o cirugía plástica. Sé breve, cálido, y directo. "
            "No inventes datos médicos. Si el mensaje no es claro, haz una pregunta breve para continuar la conversación."
        )

        # Configurar headers y payload para OpenRouter
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "HTTP-Referer": "https://tusitio.com",  # cambia esto por tu dominio o tu página
            "X-Title": "Chatbot Salud",
            "Content-Type": "application/json"
        }

        payload = {
            "model": "openchat/openchat-3.5",  # Modelo gratuito
            "messages": [
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": incoming_msg}
            ]
        }

        # Llamada a la API de OpenRouter
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", headers=headers, json=payload)
        response.raise_for_status()  # lanza excepción si hay error HTTP

        respuesta = response.json()["choices"][0]["message"]["content"]
        msg.body(respuesta)

    except Exception as e:
        msg.body(f"Ocurrió un error: {str(e)}")

    return str(resp)