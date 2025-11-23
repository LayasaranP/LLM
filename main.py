from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from langchain_groq import ChatGroq
from dotenv import load_dotenv
import os
import re

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ")

app = FastAPI()

templates = Jinja2Templates(directory="templates")

llm = ChatGroq(model="llama-3.1-8b-instant")


@app.get("/")
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
async def chat_api(request: Request):
    data = await request.json()
    user_msg = data.get("message")

    if not user_msg:
        return JSONResponse({"error": "Message is required"}, status_code=400)

    response = llm.invoke(user_msg)
    reply = response.content

    reply = reply.replace("Meta", "Layasaran")

    reply = re.sub(r"\bat\b", "by", reply)

    return JSONResponse({"reply": reply})
