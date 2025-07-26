import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming = request.values.get('Body', '').strip()
    print(f"[INFO] Mensaje recibido: {incoming}")

    resp = MessagingResponse()
    msg = resp.message()

    try:
        completion = client.chat.completions.create(
            model="mistralai/mistral-7b-instruct:free",
            messages=[
                {"role": "system", "content": "Eres un asistente en español, amable y persuasivo para ventas."},
                {"role": "user", "content": incoming}
            ],
            extra_headers={
                "HTTP-Referer": "https://bot-whatsapp-gpt-nz35.onrender.com",
                "X-Title": "BotVentasIA"
            },
            extra_body={
                "models": ["openchat/openchat-3.5-0106:free", "gryphe/mythomax-l2-13b:free"]
            }
        )

        reply = completion.choices[0].message.content.strip()
        print(f"[INFO] Respuesta del modelo: {reply}")
        msg.body(reply)

    except Exception as e:
        print(f"[ERROR] Generación falla: {e}")
        msg.body("Lo siento, hubo un problema generando la respuesta. Intenta más tarde.")


    return str(resp)

