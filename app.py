import os
import requests
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse

app = Flask(__name__)

# Cargar el token desde las variables de entorno (Render)
OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
if not OPENROUTER_API_KEY:
    raise ValueError("Error: No se encontró la variable OPENROUTER_API_KEY")

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '').strip()

    resp = MessagingResponse()
    msg = resp.message()

    try:
        system_prompt = (
            "Eres un asistente profesional que responde en español, especializado en brindar información clara, útil y persuasiva "
            "para personas interesadas en servicios de salud, medicina estética o cirugía plástica. Sé breve, cálido y directo. "
            "No inventes datos médicos. Si el mensaje no es claro, haz una pregunta breve para continuar la conversación."
        )

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {OPENROUTER_API_KEY}",
                "Content-Type": "application/json",
                "HTTP-Referer": "https://tusitio.com",  # cambia por tu dominio si tienes uno
                "X-Title": "Chatbot IA Clínica"
            },
            json={
                "model": "qwen/qwen3-coder:free",  # modelo gratuito
                "messages": [
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": incoming_msg}
                ],
                "temperature": 0.7
            }
        )

        if response.status_code == 200:
            data = response.json()
            reply = data['choices'][0]['message']['content'].strip()
            msg.body(reply)
        else:
            error_info = response.text
            msg.body(f"Ocurrió un error: Error {response.status_code}: {error_info}")

    except Exception as e:
        msg.body(f"Ocurrió un error: {str(e)}")

    return str(resp)