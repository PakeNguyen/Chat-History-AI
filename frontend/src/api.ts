
const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? 'http://127.0.0.1:8000'

export type Conversation = {
  id: string
  title: string
  created_at: string
  updated_at: string
}

export type Message = {
  id: number | string
  role: 'user' | 'assistant'
  content: string
  created_at?: string
}

export type ChatResponse = {
  conversation_id: string
  user_message: Message
  assistant_message: Message
}

async function request<T>(
  endpoint: string,
  options: RequestInit = {},
): Promise<T> {
  const response = await fetch(`${API_BASE_URL}${endpoint}`, {
    ...options,
    headers: {
      'Content-Type': 'application/json',
      ...options.headers,
    },
  })

  if (!response.ok) {
    const detail = await response.text()
    throw new Error(detail || `HTTP ${response.status}`)
  }

  return response.json() as Promise<T>
}

export function createConversation(title = 'Cuộc trò chuyện mới') {
  return request<Conversation>('/api/v1/conversations', {
    method: 'POST',
    body: JSON.stringify({ title }),
  })
}

export function getConversations() {
  return request<Conversation[]>('/api/v1/conversations')
}

export function getMessages(conversationId: string) {
  return request<Message[]>(
    `/api/v1/conversations/${conversationId}/messages`,
  )
}

export function sendChatMessage(conversationId: string, content: string) {
  return request<ChatResponse>(
    `/api/v1/conversations/${conversationId}/chat`,
    {
      method: 'POST',
      body: JSON.stringify({ content }),
    },
  )
}
