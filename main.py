import os
import uvicorn
import nest_asyncio
from typing import List
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from sqlmodel import SQLModel, create_engine, Session, select
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.messages import HumanMessage, AIMessage

nest_asyncio.apply()

app = FastAPI(title="Project 2: AI Chatbot with Persistent DB Memory")

# Database configuration
