from fastapi import APIRouter
from app.api.routes import conversations

api_router = APIRouter()
api_router.include_router(conversations.router, prefix="/conversations", tags=["conversations"])
