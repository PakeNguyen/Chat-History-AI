from openai import OpenAI
from app.core.config import settings
import tiktoken

client = OpenAI(api_key=settings.openai_api_key)

def generate_answer(messages: list[dict[str, str]]) -> str:
    """Nhận lịch sử hội thoại và trả về câu trả lời của AI."""

    response = client.responses.create(
        model=settings.openai_model,
        input=messages,
    )

    return response.output_text

def count_tokens(text: str) -> int:
    encoding = tiktoken.encoding_for_model(settings.openai_model)
    return len(encoding.encode(text))

def count_messages_tokens(messages: list[dict[str, str]]) -> int:
    total_tokens = 0

    for message in messages:
        total_tokens += count_tokens(message["role"])
        total_tokens += count_tokens(message["content"])

    return total_tokens



def select_history_by_token_budget(
    messages: list[dict[str, str]],
    max_tokens: int,
) -> list[dict[str, str]]:
    """
    Chọn lịch sử từ mới nhất trở về trước.
    Ưu tiên giữ các cặp user-assistant hoàn chỉnh.
    """
    if max_tokens <= 0:
        return []

    selected = []
    total_tokens = 0
    i = len(messages) - 1

    while i >= 0:
        message = messages[i]

        # Nếu là câu trả lời assistant, ưu tiên lấy kèm câu hỏi user trước đó.
        if message["role"] == "assistant":
            if i == 0 or messages[i - 1]["role"] != "user":
                i -= 1
                continue

            pair = [messages[i - 1], message]
            pair_tokens = sum(
                count_tokens(item["role"]) + count_tokens(item["content"])
                for item in pair
            )

            if total_tokens + pair_tokens > max_tokens:
                break

            selected[0:0] = pair
            total_tokens += pair_tokens
            i -= 2

        elif message["role"] == "user":
            # Chỉ giữ tin nhắn user riêng lẻ nếu nó là tin nhắn mới nhất.
            if i == len(messages) - 1:
                message_tokens = (
                    count_tokens(message["role"])
                    + count_tokens(message["content"])
                )

                if total_tokens + message_tokens <= max_tokens:
                    selected.insert(0, message)
                    total_tokens += message_tokens

            i -= 1

        else:
            i -= 1

    return selected


def generate_conversation_title(question: str) -> str:
    """Tạo tiêu đề ngắn từ tin nhắn đầu tiên của người dùng."""
    response = client.responses.create(
        model=settings.openai_model,
        instructions=(
            "Bạn tạo tiêu đề cho cuộc trò chuyện. "
            "Viết bằng ngôn ngữ của người dùng, tối đa 8 từ. "
            "Chỉ trả về tiêu đề, không giải thích, "
            "không dùng dấu ngoặc kép."
        ),
        input=question,
    )

    title = response.output_text.strip().strip('"\'')
    title = " ".join(title.split())

    # Dự phòng nếu AI trả về tiêu đề rỗng.
    if not title:
        title = question[:60].strip()

    return title[:100]
