from app.services.llm import (
    select_history_by_token_budget,
    count_messages_tokens,
)

messages = [
    {"role": "user", "content": "Xin chào"},
    {"role": "assistant", "content": "Chào bạn!"},
    {"role": "user", "content": "A" * 1000},
]

selected = select_history_by_token_budget(
    messages=messages,
    max_tokens=15,
)

print("Số tin nhắn ban đầu:", len(messages))
print("Số tin nhắn được chọn:", len(selected))
print("Token ước tính:", count_messages_tokens(selected))
print("Lịch sử được chọn:", selected)