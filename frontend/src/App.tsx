import ReactMarkdown from 'react-markdown'
import remarkGfm from 'remark-gfm'
import { useEffect, useState } from 'react'
import {
  createConversation,
  getConversations,
  getMessages,
  sendChatMessage,
  type Conversation,
  type Message,
} from './api'
import './App.css'

type Chat = Conversation & {
  messages: Message[]
}

function App() {
  const [chats, setChats] = useState<Chat[]>([])
  const [activeChatId, setActiveChatId] = useState<string | null>(null)
  const [input, setInput] = useState('')
  const [loadingChats, setLoadingChats] = useState(true)
  const [sending, setSending] = useState(false)
  const [error, setError] = useState('')

  const activeChat = chats.find((chat) => chat.id === activeChatId)

  // 1. Tải danh sách hội thoại khi mở ứng dụng.
  useEffect(() => {
    let cancelled = false

    async function loadChats() {
      try {
        setError('')
        const conversations = await getConversations()

        if (cancelled) return

        setChats(
          conversations.map((conversation) => ({
            ...conversation,
            messages: [],
          })),
        )

        setActiveChatId((currentId) => {
          if (
            currentId &&
            conversations.some((chat) => chat.id === currentId)
          ) {
            return currentId
          }

          return conversations[0]?.id ?? null
        })
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : 'Không thể tải danh sách hội thoại.',
          )
        }
      } finally {
        if (!cancelled) setLoadingChats(false)
      }
    }

    loadChats()

    return () => {
      cancelled = true
    }
  }, [])

  // 2. Tải tin nhắn khi chọn một hội thoại.
  useEffect(() => {
    if (!activeChatId) return

    let cancelled = false

    async function loadMessages() {
      try {
        const messages = await getMessages(activeChatId!)

        if (cancelled) return

        setChats((previous) =>
          previous.map((chat) =>
            chat.id === activeChatId
              ? { ...chat, messages }
              : chat,
          ),
        )
      } catch (err) {
        if (!cancelled) {
          setError(
            err instanceof Error
              ? err.message
              : 'Không thể tải tin nhắn.',
          )
        }
      }
    }

    loadMessages()

    return () => {
      cancelled = true
    }
  }, [activeChatId])

  // 3. Tạo hội thoại thật trong database.
  async function createChat() {
    try {
      setError('')

      const conversation = await createConversation()

      const newChat: Chat = {
        ...conversation,
        messages: [],
      }

      setChats((previous) => [newChat, ...previous])
      setActiveChatId(newChat.id)
      setInput('')
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Không thể tạo cuộc trò chuyện.',
      )
    }
  }

  // 4. Gửi câu hỏi đến backend và nhận câu trả lời AI.
  async function sendMessage() {
    const content = input.trim()

    if (!content || !activeChatId || sending) return

    const conversationId = activeChatId

    try {
      setSending(true)
      setError('')
      setInput('')

      const result = await sendChatMessage(conversationId, content)

      setChats((previous) =>
        previous.map((chat) => {
          if (chat.id !== conversationId) return chat

          return {
            ...chat,
            updated_at: new Date().toISOString(),
            messages: [
              ...chat.messages,
              result.user_message,
              result.assistant_message,
            ],
          }
        }),
      )

      // Đồng bộ danh sách để tiêu đề mới nhất nằm trên đầu.
      const conversations = await getConversations()
      setChats((previous) =>
        conversations.map((conversation) => {
          const existing = previous.find(
            (chat) => chat.id === conversation.id,
          )

          return {
            ...conversation,
            messages: existing?.messages ?? [],
          }
        }),
      )
    } catch (err) {
      setInput(content)
      setError(
        err instanceof Error
          ? err.message
          : 'Không thể gửi câu hỏi đến AI.',
      )
    } finally {
      setSending(false)
    }
  }

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon">✳</div>
          <div>
            <h1>Chat History AI</h1>
            <span>Your AI workspace</span>
          </div>
        </div>

        <button className="new-chat-button" onClick={createChat}>
          <span>＋</span> Cuộc trò chuyện mới
        </button>

        <p className="sidebar-label">LỊCH SỬ</p>

        <div className="chat-list">
          {loadingChats && <p>Đang tải hội thoại...</p>}

          {!loadingChats && chats.length === 0 && (
            <p>Chưa có cuộc trò chuyện nào.</p>
          )}

          {chats.map((chat) => (
            <button
              key={chat.id}
              className={`chat-item ${
                chat.id === activeChatId ? 'active' : ''
              }`}
              onClick={() => setActiveChatId(chat.id)}
            >
              <span className="chat-item-icon">▤</span>
              <span className="chat-item-title">{chat.title}</span>
            </button>
          ))}
        </div>

        <div className="sidebar-footer">
          <div className="avatar">U</div>
          <div>
            <strong>Người dùng</strong>
            <span>Personal workspace</span>
          </div>
        </div>
      </aside>

      <main className="main-panel">
        <header className="topbar">
          <div>
            <span className="status-dot" />
            <span>AI Assistant</span>
          </div>
          <span className="model-label">Chat History AI</span>
        </header>

        <section className="conversation">
          <div className="conversation-heading">
            <span className="eyebrow">YOUR WORKSPACE</span>
            <h2>{activeChat?.title ?? 'Cuộc trò chuyện'}</h2>
            <p>Hỏi đáp, khám phá ý tưởng và xây dựng cùng AI.</p>
          </div>

          <div className="message-list">
            {!activeChat || activeChat.messages.length === 0 ? (
              <div className="empty-state">
                <div className="empty-icon">✳</div>
                <h3>Bắt đầu một cuộc trò chuyện</h3>
                <p>Nhập câu hỏi bên dưới để bắt đầu.</p>
              </div>
            ) : (
              activeChat.messages.map((message) => (
                <article
                  key={message.id}
                  className={`message-row ${message.role}`}
                >
                  <div className="message-avatar">
                    {message.role === 'assistant' ? '✳' : 'U'}
                  </div>
                  <div className="message-body">
                    <strong>
                      {message.role === 'assistant'
                        ? 'AI Assistant'
                        : 'Bạn'}
                    </strong>

                    <div className="markdown-content">
                      {message.role === 'assistant' ? (
                        <ReactMarkdown remarkPlugins={[remarkGfm]}>
                          {message.content}
                        </ReactMarkdown>
                      ) : (
                        <p>{message.content}</p>
                      )}
                    </div>
                  </div>
                </article>
              ))
            )}

            {sending && (
              <p>AI đang suy nghĩ, em chờ một chút nhé...</p>
            )}
          </div>

          {error && (
            <p role="alert" className="error-message">
              {error}
            </p>
          )}

          <form
            className="composer"
            onSubmit={(event) => {
              event.preventDefault()
              void sendMessage()
            }}
          >
            <textarea
              value={input}
              onChange={(event) => setInput(event.target.value)}
              onKeyDown={(event) => {
                if (event.key === 'Enter' && !event.shiftKey) {
                  event.preventDefault()
                  void sendMessage()
                }
              }}
              placeholder="Nhập câu hỏi của bạn..."
              rows={2}
              disabled={sending}
            />
            <div className="composer-bottom">
              <span>Enter để gửi · Shift + Enter xuống dòng</span>
              <button
                type="submit"
                disabled={!input.trim() || !activeChatId || sending}
              >
                {sending ? 'Đang gửi...' : 'Gửi'} <span>↑</span>
              </button>
            </div>
          </form>

          <p className="disclaimer">
            Câu hỏi và câu trả lời được xử lý qua backend AI.
          </p>
        </section>
      </main>
    </div>
  )
}

export default App
