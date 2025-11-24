from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
from langchain_groq import ChatGroq
from langchain_core.messages import SystemMessage, HumanMessage
from dotenv import load_dotenv
import os

load_dotenv()

os.environ["GROQ_API_KEY"] = os.getenv("GROQ")

app = FastAPI()
templates = Jinja2Templates(directory="templates")

# System instruction (identity)
system_prompt = """
You are a helpful AI assistant created by Layasaran.
If the user asks who created you, who developed you, who built you, or any similar question,
ALWAYS answer: "I was created by Layasaran."
Never mention Meta, Llama, Groq, or LangChain in creation-related answers.
"""

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

    # Send system + user messages together
    response = llm.invoke([
        SystemMessage(content=system_prompt),
        HumanMessage(content=user_msg)
    ])

    reply = response.content

    return JSONResponse({"reply": reply})
