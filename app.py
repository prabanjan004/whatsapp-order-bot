from fastapi import FastAPI, Form
from twilio.twiml.messaging_response import MessagingResponse
from groq import Groq
import os

app = FastAPI()

groq_client = Groq(api_key=os.environ["GROQ_API_KEY"])

SYSTEM_PROMPT = """You are a food order-taking assistant for a restaurant.

Menu:
- Burger: ₹120
- Pizza: ₹200
- Fries: ₹60
- Cold drink: ₹40

Be friendly and short."""

@app.post("/whatsapp")
async def whatsapp_reply(Body: str = Form(), From: str = Form()):
    chat = groq_client.chat.completions.create(
        model="mixtral-8x7b-32768",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": Body}
        ],
        max_tokens=200
    )

    reply = chat.choices[0].message.content

    resp = MessagingResponse()
    resp.message(reply)

    return str(resp)

@app.get("/")
def home():
    return {"status": "running"}