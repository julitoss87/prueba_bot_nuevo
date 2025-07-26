import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

app = Flask(__name__)

# Cliente OpenRouter
client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    print(f"[INFO] Mensaje recibido: {incoming_msg}")  # Verificación 1

    resp = MessagingResponse()
    msg = resp.message()

    try:
        # Llamada al modelo Qwen2.5 VL Instruct
        completion = client.chat.completions.create(
            model="qwen/qwen2.5-vl-32b-instruct:free",
            messages=[
                ChatCompletionMessageParam(role="system", content="Eres un asistente útil y claro."),
                ChatCompletionMessageParam(role="user", content=incoming_msg)
            ],
            extra_headers={
                "HTTP-Referer": "https://tuapp.render.com",  # Opcional
                "X-Title": "BotWhatsAppIA"
            }
        )

        reply = completion.choices[0].message.content.strip()
        print(f"[INFO] Respuesta del modelo: {reply}")  # Verificación 2

        msg.body(reply)

    except Exception as e:
        print(f"[ERROR] Ocurrió un error en la generación: {e}")  # Verificación 3
        msg.body(f"Ocurrió un error: {e}")

    return str(resp)