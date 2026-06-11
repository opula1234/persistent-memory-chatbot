import os
import uvicorn
import nest_asyncio
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, select, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage
from contextlib import asynccontextmanager

nest_asyncio.apply()


# Database configuration
DATABASE_URL = "sqlite:///chat_history.db"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# SQLModel DB Schema: to save chat history


class ChatMessageRecord(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    session_id: str = Field(index=True)
    sender_type: str
    content: str

# Table creation on server start on


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    SQLModel.metadata.create_all(engine)

    yield

    # Shutdown logic (optional)
    print("Application shutting down...")

app = FastAPI(
    title="Project 2: AI Chatbot with Persistent DB Memory",
    lifespan=lifespan
)

# AI Model Configuration
os.environ["GEMINI_API_KEY"] = "Gemini API Key"
llm = ChatGoogleGenerativeAI(model="gemini-2.5-flash")

# Input Schema


class ChatRequest(BaseModel):
    session_id: str
    prompt: str

# FastAPI resonse with persistent logic


@app.post("/api/v1/chat-with-history")
async def chat_handler(request: ChatRequest):
    if not request.prompt.strip():
        raise HTTPException(
            status_code=400, detail="Prompt cannot be empty!")

    session_id = request.session_id

    # Using Context Manager to handle DB memory
    with Session(engine) as db_session:
        try:
            # STEP 1: Fetching old chats for this session_id from the DB sequentially
            statement = select(ChatMessageRecord).where(
                ChatMessageRecord.session_id == session_id).order_by(ChatMessageRecord.id)
            db_records = db_session.exec(statement).all()

            # STEP 2: Converting DB data to LangChain message format
            chat_history_payload = []
            for record in db_records:
                if record.sender_type == "human":
                    chat_history_payload.append(
                        HumanMessage(content=record.content))
                else:
                    chat_history_payload.append(
                        AIMessage(content=record.content))

            # STEP 3: Adding the current new question to the history
            chat_history_payload.append(HumanMessage(content=request.prompt))

            # STEP 4: Invoking the Gemini model with the full history
            ai_response = llm.invoke(chat_history_payload)
            ai_reply_text = ai_response.content

            # STEP 5: [Very Important] Saving the current question and response in the DB
            user_record = ChatMessageRecord(
                session_id=session_id, sender_type="human", content=request.prompt)
            ai_record = ChatMessageRecord(
                session_id=session_id, sender_type="ai", content=ai_reply_text)

            db_session.add(user_record)
            db_session.add(ai_record)
            db_session.commit()  # Data is saved permanently!

            return {
                "session_id": session_id,
                "reply": ai_reply_text
            }

        except Exception as e:
            db_session.rollback()
            raise HTTPException(status_code=500, detail=str(e))


# Server Run
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
