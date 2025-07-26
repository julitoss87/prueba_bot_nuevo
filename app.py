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
    incoming_msg = request.values.get('Body', '')
    print(f"[INFO] Mensaje recibido: {incoming_msg}")

    resp = MessagingResponse()
    msg = resp.message()

    try:
        completion = client.chat.completions.create(
            model="google/gemma-1.1-7b-it:free",  # usa aquí el modelo gratis que funcione
            messages=[
                {"role": "system", "content": "Eres un asistente útil y claro."},
                {"role": "user", "content": incoming_msg}
            ],
            extra_headers={
                "HTTP-Referer": "https://tuapp.render.com",
                "X-Title": "BotWhatsAppIA"
            }
        )

        if completion.choices:
            content = completion.choices[0].message.content
            print(f"[INFO] Respuesta cruda: {content}")
            if content:
                msg.body(content.strip())
            else:
                msg.body("No se generó respuesta. Intenta de nuevo.")
        else:
            print("[WARN] El modelo no devolvió ninguna elección.")
            msg.body("No se recibió respuesta del modelo. Intenta más tarde.")

    except Exception as e:
        print(f"[ERROR] Ocurrió un error en la generación: {e}")
        msg.body("Ocurrió un error al procesar tu mensaje. Intenta más tarde.")

    return str(resp)
