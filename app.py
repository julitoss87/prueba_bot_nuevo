import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
import replicate

app = Flask(__name__)

# Requiere que hayas definido tu token como variable de entorno en Render
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
if not REPLICATE_API_TOKEN:
    raise ValueError("Error: No se encontró el token de Replicate")

os.environ["REPLICATE_API_TOKEN"] = REPLICATE_API_TOKEN

@app.route("/webhook", methods=["POST"])
def webhook():
    # Captura el mensaje entrante
    incoming_msg = request.values.get('Body', '').strip()
    
    # Crea una respuesta de Twilio
    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Mensaje inicial del sistema para orientar el estilo del chatbot
        system_prompt = (
            "Eres un asistente profesional que responde en español, especializado en brindar información clara, útil y persuasiva "
            "para personas interesadas en servicios de salud, medicina estética o cirugía plástica. Sé breve, cálido, y directo. "
            "No inventes datos médicos. Si el mensaje no es claro, haz una pregunta breve para continuar la conversación."
        )

        # Llamada al modelo de Replicate
        model = replicate.models.get("mistralai/mistral-7b-instruct-v0.1")
        version = model.versions.get("01fd75c8f635929c4c401d70b4d79c565c8ed51c594cbdf7bfa91d3b7d37e29f")
        output = version.predict(
            prompt=f"{system_prompt}\n\nUsuario: {incoming_msg}\nAsistente:",
            temperature=0.7,
            max_new_tokens=200,
            top_p=0.9
        )

        # Combina la respuesta generada (es un generador)
        respuesta = "".join(output)
        msg.body(respuesta)

    except Exception as e:
        msg.body(f"Ocurrió un error: {str(e)}")

    return str(resp)