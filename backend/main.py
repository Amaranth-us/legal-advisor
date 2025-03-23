import os

from dotenv import load_dotenv
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI
from pydantic import BaseModel

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


class ChatRequest(BaseModel):
    question: str


class ChatResponse(BaseModel):
    answer: str


@app.get("/")
async def root():
    return {"message": "Legal Advisor API is running."}


@app.post("/chat", response_model=ChatResponse)
async def chat(request: ChatRequest):
    try:
        messages = [
            {
                "role": "system",
                "content": "Act as a professional legal advisor. Provide general legal "
                "information only. Do not give specific legal advice or act as a lawyer. "
                "Analyze the documents provided and identify any potential liability and the parties involved. "
                "If the document discusses employment agreements, summarize the sections related to termination and severance pay.",
            },
            {"role": "user", "content": request.question},
        ]

        response = client.chat.completions.create(
            model="gpt-3.5-turbo", messages=messages, max_tokens=500, temperature=0.7
        )

        answer = response.choices[0].message.content
        return {"answer": answer.strip()}

    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})
