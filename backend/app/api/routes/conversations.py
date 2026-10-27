import uuid
from datetime import datetime, timezone

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.conversation import Conversation
from app.models.message import Message
from app.schemas.conversation import ConversationCreate, ConversationRead, ChatResponse
from app.schemas.message import MessageRead, UserMessageCreate
from app.services.llm import generate_answer, generate_conversation_title, select_history_by_token_budget, count_tokens

router = APIRouter()

@router.post("", response_model=ConversationRead, status_code=status.HTTP_201_CREATED)
def create_conversation(payload: ConversationCreate, db: Session = Depends(get_db)) -> Conversation:
    conversation = Conversation(title=payload.title.strip())
    if not conversation.title:
        raise HTTPException(status_code=422, detail="Tiêu đề không được để trống")
    db.add(conversation)
    db.commit()
    db.refresh(conversation)
    return conversation

@router.get("", response_model=list[ConversationRead])
def list_conversations(limit: int = 50, db: Session = Depends(get_db)) -> list[Conversation]:
    if not 1 <= limit <= 100:
        raise HTTPException(status_code=422, detail="limit phải nằm trong khoảng 1–100")
    statement = select(Conversation).order_by(Conversation.updated_at.desc()).limit(limit)
    return list(db.scalars(statement).all())

@router.post(
    "/{conversation_id}/messages",
    response_model=MessageRead,
    status_code=status.HTTP_201_CREATED,
)
def add_user_message(
    conversation_id: uuid.UUID,
    payload: UserMessageCreate,
    db: Session = Depends(get_db),
) -> Message:
    conversation = db.get(Conversation, conversation_id)
    if conversation is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")

    content = payload.content.strip()
    if not content:
        raise HTTPException(status_code=422, detail="Nội dung tin nhắn không được để trống")

    message = Message(conversation_id=conversation_id, role="user", content=content)
    db.add(message)
    conversation.updated_at = datetime.now(timezone.utc)
    db.commit()
    db.refresh(message)
    return message

@router.get("/{conversation_id}/messages", response_model=list[MessageRead])
def get_conversation_messages(
    conversation_id: uuid.UUID,
    db: Session = Depends(get_db),
) -> list[Message]:
    if db.get(Conversation, conversation_id) is None:
        raise HTTPException(status_code=404, detail="Không tìm thấy cuộc trò chuyện")
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.asc(), Message.id.asc())
    )
    return list(db.scalars(statement).all())



@router.post(
    "/{conversation_id}/chat",
    response_model=ChatResponse,
    status_code=status.HTTP_201_CREATED,
)
def chat_with_llm(
    conversation_id: uuid.UUID,
    payload: UserMessageCreate,
    db: Session = Depends(get_db),
) -> dict:
    # 1. Kiểm tra cuộc hội thoại
    conversation = db.get(Conversation, conversation_id)

    if conversation is None:
        raise HTTPException(
            status_code=404,
            detail="Không tìm thấy cuộc trò chuyện",
        )

    # 2. Kiểm tra nội dung câu hỏi
    question = payload.content.strip()

    if not question:
        raise HTTPException(
            status_code=422,
            detail="Nội dung tin nhắn không được để trống",
        )

    # 2.1. Giới hạn token của câu hỏi user
    MAX_USER_MESSAGE_TOKENS = 1000

    question_tokens = count_tokens(question)

    if question_tokens > MAX_USER_MESSAGE_TOKENS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Tin nhắn có {question_tokens} token, "
                f"vượt giới hạn {MAX_USER_MESSAGE_TOKENS} token. "
                "Vui lòng rút ngắn câu hỏi."
            ),
        )

    # 3. Lấy lịch sử hội thoại từ database
    statement = (
        select(Message)
        .where(Message.conversation_id == conversation_id)
        .order_by(Message.created_at.desc(), Message.id.desc())
        .limit(8)
    )

    history = list(reversed(db.scalars(statement).all()))

    # Chuyển ORM objects thành định dạng đầu vào của OpenAI
    messages = [
        {"role": message.role, "content": message.content}
        for message in history
        if message.role in ("user", "assistant")
    ]

    messages = select_history_by_token_budget(
        messages=messages,
        max_tokens=1000,
    )

    messages.append({"role": "user", "content": question})
    
    # 4. Gọi LLM trước khi lưu tin nhắn mới
    is_first_message = (
        db.scalar(
            select(Message.id)
            .where(Message.conversation_id == conversation_id)
            .limit(1)
        )
        is None
    )

    try:
        answer = generate_answer(messages)

        new_title = None
        if is_first_message and conversation.title == "Cuộc trò chuyện mới":
            new_title = generate_conversation_title(question)

    except Exception as exc:
        import logging

        logging.exception("Lỗi khi gọi OpenAI API")
        db.rollback()

        raise HTTPException(
            status_code=502,
            detail=f"Lỗi khi gọi AI: {type(exc).__name__}: {exc}",
        ) from exc

    # try:
    #     answer = generate_answer(messages)
    # except Exception as exc:
    #     db.rollback()
    #     raise HTTPException(
    #         status_code=502,
    #         detail="Không thể tạo câu trả lời từ AI",
    #     ) from exc

    # 5. Lưu cả câu hỏi và câu trả lời
    user_message = Message(
        conversation_id=conversation_id,
        role="user",
        content=question,
    )
    assistant_message = Message(
        conversation_id=conversation_id,
        role="assistant",
        content=answer,
    )

    try:
        db.add_all([user_message, assistant_message])
        conversation.updated_at = datetime.now(timezone.utc)
        
        if new_title:
            conversation.title = new_title

        db.commit()

        db.refresh(user_message)
        db.refresh(assistant_message)
    except Exception:
        db.rollback()
        raise HTTPException(
            status_code=500,
            detail="Không thể lưu tin nhắn vào database",
        )

    # 6. Trả kết quả về client
    return {
        "conversation_id": str(conversation_id),
        "user_message": MessageRead.model_validate(
            user_message
        ).model_dump(mode="json"),
        "assistant_message": MessageRead.model_validate(
            assistant_message
        ).model_dump(mode="json"),
    }
