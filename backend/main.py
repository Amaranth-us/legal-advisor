import os

import database
import tiktoken
from crud import chat_history_crud
from dotenv import load_dotenv
from fastapi import Depends, FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from openai import OpenAI, OpenAIError, RateLimitError
from openai.types.chat import ChatCompletionMessageParam
from pydantic import BaseModel, ValidationError
from schemas import chat_history_schemas
from sqlalchemy.orm import Session
from tenacity import (
    retry,
    retry_if_exception_type,
    stop_after_attempt,
    wait_random_exponential,
)

MAX_TOKENS = 4096
MAX_RESPONSE_TOKENS = 500
MAX_PROMPT_TOKENS = MAX_TOKENS - MAX_RESPONSE_TOKENS


def count_tokens(messages: list[dict], model: str = "gpt-3.5-turbo") -> int:
    enc = tiktoken.encoding_for_model(model)
    num_tokens = 0
    for message in messages:
        num_tokens += 4  # every message has a metadata overhead
        for key, value in message.items():
            num_tokens += len(enc.encode(value))
    num_tokens += 2  # end-of-sequence tokens
    return num_tokens


def trim_input_if_needed(messages, max_prompt_tokens=MAX_PROMPT_TOKENS):
    current_tokens = count_tokens(messages)
    if current_tokens <= max_prompt_tokens:
        return messages

    print("⚠️ Input trimmed to fit token limits.")
    user_msg = messages[-1]
    enc = tiktoken.encoding_for_model("gpt-3.5-turbo")
    trimmed = enc.encode(user_msg["content"])[
        : max_prompt_tokens - count_tokens(messages[:-1])
    ]
    user_msg["content"] = enc.decode(trimmed)
    return messages


@retry(
    reraise=True,
    stop=stop_after_attempt(3),
    wait=wait_random_exponential(min=1, max=10),
    retry=retry_if_exception_type((RateLimitError, OpenAIError)),
)
def get_openai_response(messages: list[ChatCompletionMessageParam]):
    return client.chat.completions.create(
        model="gpt-3.5-turbo", messages=messages, max_tokens=500, temperature=0.7
    )


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
        messages: list[ChatCompletionMessageParam] = [
            {
                "role": "system",
                "content": "Act as a professional legal advisor. Provide general legal "
                "information only. Do not give specific legal advice or act as a lawyer. "
                "Analyze the documents provided and identify any potential liability and the parties involved. "
                "If the document discusses employment agreements, summarize the sections related to termination and severance pay.",
            },
            {"role": "user", "content": request.question},
        ]

        messages = trim_input_if_needed(messages)

        # response = client.chat.completions.create(
        #     model="gpt-3.5-turbo", messages=messages, max_tokens=500, temperature=0.7
        # )
        response = get_openai_response(messages)

        answer_res = response.choices[0].message.content
        answer = answer_res.strip() if answer_res else "No response from model."
        return {"answer": answer}

    except ValidationError as ve:
        return JSONResponse(
            status_code=422, content={"error": "Invalid input", "details": ve.errors()}
        )

    except OpenAIError as oe:
        return JSONResponse(
            status_code=502, content={"error": "OpenAI API error", "details": str(oe)}
        )

    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"error": "Internal server error", "details": str(e)},
        )


@app.post("/chat-history/", response_model=chat_history_schemas.ChatHistory)
def create_chat_history(
    chat_history: chat_history_schemas.ChatHistoryCreate,
    db: Session = Depends(database.get_db),
):
    return chat_history_crud.create_chat_history(db=db, chat_history=chat_history)


@app.get(
    "/chat-history/{session_id}", response_model=list[chat_history_schemas.ChatHistory]
)
def get_chat_history(session_id: str, db: Session = Depends(database.get_db)):
    chat_history = chat_history_crud.get_chat_history_by_session_id(
        db=db, session_id=session_id
    )
    return chat_history
