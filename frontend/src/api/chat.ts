import api from './task'

export interface Conversation {
  id: number
  title: string
  ai_role: string
  ai_personality: string
  ai_region: string
  created_at: string
  updated_at: string
  message_count: number
}

export interface Message {
  id: number
  conversation_id: number
  role: 'user' | 'assistant'
  content: string
  images: string[]
  created_at: string
}

export interface ChatResponse {
  reply: string
  user_message: Message
  assistant_message: Message
}

export interface UploadResponse {
  id: string
  filename: string
  size: number
  mime_type: string
}

export const chatApi = {
  getConversations() {
    return api.get<Conversation[]>('/chat/conversations')
  },

  createConversation() {
    return api.post<Conversation>('/chat/conversations')
  },

  deleteConversation(id: number) {
    return api.delete(`/chat/conversations/${id}`)
  },

  getMessages(conversationId: number) {
    return api.get<Message[]>(`/chat/conversations/${conversationId}/messages`)
  },

  sendMessage(conversationId: number, content: string, images: string[] = []) {
    return api.post<ChatResponse>(`/chat/conversations/${conversationId}/messages`, { content, images })
  },

  getConversation(id: number) {
    return api.get<Conversation>(`/chat/conversations/${id}`)
  },

  updateConversation(id: number, data: { ai_role?: string; ai_personality?: string; ai_region?: string }) {
    return api.patch<Conversation>(`/chat/conversations/${id}`, data)
  },

  uploadFile(file: File) {
    const form = new FormData()
    form.append('file', file)
    return api.post<UploadResponse>('/chat/upload', form, {
      headers: { 'Content-Type': 'multipart/form-data' }
    })
  },

  stopGeneration(conversationId: number) {
    return api.post(`/chat/conversations/${conversationId}/stop`)
  }
}