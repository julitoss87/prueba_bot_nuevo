import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import requests

app = Flask(__name__)

# Verifica que la clave de OpenRouter exista
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Error: No se encontró la variable OPENROUTER_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Prompt de sistema
        system_prompt = {
            "role": "system",
            "content": (
                "Eres un asistente profesional que responde en español, especializado en brindar información clara, útil y persuasiva "
                "para personas interesadas en servicios de salud, medicina estética o cirugía plástica. Sé breve, cálido, y directo. "
                "No inventes datos médicos. Si el mensaje no es claro, haz una pregunta breve para continuar la conversación."
            )
        }

        # Mensaje del usuario
        user_msg = {"role": "user", "content": incoming_msg}

        # Solicitud al endpoint de OpenRouter
        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json"
            },
            json={
                "model": "gryphe/mythomax-l2-13b",
                "messages": [system_prompt, user_msg],
                "temperature": 0.7
            }
        )

        if response.status_code != 200:
            raise ValueError(f"Error {response.status_code}: {response.text}")

        respuesta = response.json()["choices"][0]["message"]["content"]
        msg.body(respuesta)

    except Exception as e:
        msg.body(f"Ocurrió un error: {str(e)}")

    return str(resp)