import { defineStore } from 'pinia'
import { ref } from 'vue'
import { chatApi, Conversation, Message } from '../api/chat'

export const useChatStore = defineStore('chat', () => {
  const conversations = ref<Conversation[]>([])
  const currentConversationId = ref<number | null>(null)
  const messages = ref<Message[]>([])
  const loading = ref(false)
  const sending = ref(false)

  const fetchConversations = async () => {
    try {
      const response = await chatApi.getConversations()
      conversations.value = response.data
    } catch (error) {
      console.error('获取对话列表失败:', error)
    }
  }

  const createConversation = async () => {
    try {
      const response = await chatApi.createConversation()
      conversations.value.unshift(response.data)
      currentConversationId.value = response.data.id
      messages.value = []
      return response.data
    } catch (error) {
      console.error('创建对话失败:', error)
      throw error
    }
  }

  const deleteConversation = async (id: number) => {
    try {
      await chatApi.deleteConversation(id)
      conversations.value = conversations.value.filter(c => c.id !== id)
      if (currentConversationId.value === id) {
        currentConversationId.value = null
        messages.value = []
      }
    } catch (error) {
      console.error('删除对话失败:', error)
      throw error
    }
  }

  const selectConversation = async (id: number) => {
    currentConversationId.value = id
    loading.value = true
    try {
      const msgRes = await chatApi.getMessages(id)
      messages.value = msgRes.data
    } catch (error) {
      console.error('获取消息失败:', error)
    }
    try {
      const convRes = await chatApi.getConversation(id)
      currentAiRole.value = convRes.data.ai_role || '小美'
      currentAiPersonality.value = convRes.data.ai_personality || '温柔体贴的妹子'
      currentAiRegion.value = convRes.data.ai_region || '广西'
    } catch (error) {
      console.error('获取对话设置失败:', error)
    } finally {
      loading.value = false
    }
  }

  const sendMessage = async (content: string, imageIds: string[] = []) => {
    if (!currentConversationId.value) return

    const tempId = -Date.now()
    const userMsg: Message = {
      id: tempId,
      conversation_id: currentConversationId.value,
      role: 'user',
      content,
      images: imageIds,
      created_at: new Date().toISOString()
    }
    messages.value.push(userMsg)

    sending.value = true
    try {
      const response = await chatApi.sendMessage(currentConversationId.value, content, imageIds)
      const idx = messages.value.findIndex(m => m.id === tempId)
      if (idx !== -1) {
        messages.value[idx] = response.data.user_message
      }
      messages.value.push(response.data.assistant_message)
      await fetchConversations()
    } catch (error) {
      console.error('发送消息失败:', error)
      throw error
    } finally {
      sending.value = false
    }
  }

  const uploadFile = async (file: File) => {
    try {
      const response = await chatApi.uploadFile(file)
      return response.data
    } catch (error) {
      console.error('上传文件失败:', error)
      throw error
    }
  }

  const currentAiRole = ref('小美')
  const currentAiPersonality = ref('温柔体贴的妹子')
  const currentAiRegion = ref('广西')

  const updateAiSettings = async (role: string, personality: string, region: string) => {
    if (!currentConversationId.value) return
    currentAiRole.value = role
    currentAiPersonality.value = personality
    currentAiRegion.value = region
    try {
      await chatApi.updateConversation(currentConversationId.value, {
        ai_role: role, ai_personality: personality, ai_region: region
      })
      await fetchConversations()
    } catch (error) {
      console.error('更新AI设置失败:', error)
    }
  }

  const loadAiSettings = () => {
    const conv = conversations.value.find(c => c.id === currentConversationId.value)
    if (conv) {
      currentAiRole.value = conv.ai_role || '小美'
      currentAiPersonality.value = conv.ai_personality || '温柔体贴的妹子'
      currentAiRegion.value = conv.ai_region || '广西'
    }
  }

  const stopGeneration = async () => {
    if (!currentConversationId.value) return
    try {
      await chatApi.stopGeneration(currentConversationId.value)
    } catch (error) {
      console.error('停止生成失败:', error)
    }
  }

  return {
    conversations,
    currentConversationId,
    messages,
    loading,
    sending,
    currentAiRole,
    currentAiPersonality,
    currentAiRegion,
    fetchConversations,
    createConversation,
    deleteConversation,
    selectConversation,
    sendMessage,
    uploadFile,
    stopGeneration,
    updateAiSettings,
    loadAiSettings
  }
})