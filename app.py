import requests
import os

GROQ_API_KEY = os.getenv("GROQ_API_KEY")  # o ponla directamente si estás local: "sk-..."

def generar_respuesta_groq(mensaje, modelo="mistral-7b-instruct"):
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
    except requests.exceptions.RequestException as e:
        print("[ERROR] Falló la llamada a Groq:", e)
        return "Lo siento, hubo un error generando la respuesta."