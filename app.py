import os
from flask import Flask, request
from twilio.twiml.messaging_response import MessagingResponse
from openai import OpenAI
from openai.types.chat import ChatCompletionMessageParam

app = Flask(__name__)

client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=os.environ.get("OPENROUTER_API_KEY"),
)

@app.route("/webhook", methods=["POST"])
def webhook():
    incoming_msg = request.values.get('Body', '')
    resp = MessagingResponse()
    msg = resp.message()

    try:
        completion = client.chat.completions.create(
            model="google/gemma-3-27b-it:free",
            messages=[
                ChatCompletionMessageParam(role="system", content="Eres un asistente amable."),
                ChatCompletionMessageParam(role="user", content=incoming_msg)
            ],
            extra_headers={
                "HTTP-Referer": "https://tuapp.render.com",  # Opcional
                "X-Title": "BotWhatsAppIA"
            }
        )

        reply = completion.choices[0].message.content
        msg.body(reply)

    except Exception as e:
        msg.body(f"Ocurrió un error: {e}")

    return str(resp)