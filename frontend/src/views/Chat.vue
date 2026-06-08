<template>
  <div class="chat-container">
    <div class="chat-sidebar">
      <div class="sidebar-header">
        <h3>历史对话</h3>
        <div class="header-btns">
          <el-button v-if="selectedIds.size > 0" type="danger" size="small" @click="handleBatchDelete">
            <el-icon><Delete /></el-icon>
            删除选中 ({{ selectedIds.size }})
          </el-button>
          <el-button v-else type="primary" size="small" @click="handleNewConversation">
            <el-icon><Plus /></el-icon>
            新建对话
          </el-button>
        </div>
      </div>
      <div v-if="chatStore.conversations.length > 0" class="select-all-bar">
        <el-checkbox :model-value="isAllSelected" @change="toggleSelectAll" size="small">全选</el-checkbox>
      </div>
      <div class="conversation-list">
        <div
          v-for="conv in chatStore.conversations"
          :key="conv.id"
          class="conversation-item"
          :class="{ active: conv.id === chatStore.currentConversationId, selected: selectedIds.has(conv.id) }"
          @click="handleSelectConversation(conv.id)"
        >
          <el-checkbox
            class="conv-checkbox"
            :checked="selectedIds.has(conv.id)"
            @click.stop
            @change="(val: boolean) => toggleSelect(conv.id, val)"
            size="small"
          />
          <div class="conv-info">
            <div class="conv-title">{{ conv.title }}</div>
            <div class="conv-meta">
              <span>{{ formatDate(conv.created_at) }}</span>
              <span>{{ conv.message_count }}条消息</span>
            </div>
          </div>
          <el-button
            class="delete-btn"
            type="danger"
            link
            size="small"
            @click.stop="handleDeleteConversation(conv.id)"
          >
            <el-icon><Delete /></el-icon>
          </el-button>
        </div>
        <el-empty v-if="chatStore.conversations.length === 0" description="暂无对话" :image-size="60" />
      </div>

      <div v-if="chatStore.currentConversationId" class="ai-settings">
        <div class="settings-header" @click="settingsOpen = !settingsOpen">
          <el-icon :size="16"><MagicStick /></el-icon>
          <span>AI 角色设置</span>
          <el-icon :class="{ 'arrow-open': settingsOpen }" style="transition: transform 0.2s"><ArrowRight /></el-icon>
        </div>
        <el-collapse-transition>
          <div v-show="settingsOpen" class="settings-body">
            <div class="setting-field">
              <label>预设</label>
              <el-select v-model="presetKey" placeholder="选择预设" size="small" style="width: 100%" @change="applyPreset">
                <el-option v-for="p in presets" :key="p.key" :label="p.label" :value="p.key" />
              </el-select>
            </div>
            <div class="setting-field">
              <label>角色</label>
              <el-input v-model="aiRole" size="small" placeholder="如：小美" />
            </div>
            <div class="setting-field">
              <label>性格</label>
              <el-input v-model="aiPersonality" size="small" placeholder="如：温柔体贴的妹子" />
            </div>
            <div class="setting-field">
              <label>地区</label>
              <el-input v-model="aiRegion" size="small" placeholder="如：广西" />
            </div>
            <el-button type="primary" size="small" style="width: 100%; margin-top: 6px" @click="saveAiSettings">
              保存设置
            </el-button>
          </div>
        </el-collapse-transition>
      </div>
    </div>

    <div class="chat-main">
      <div v-if="!chatStore.currentConversationId" class="chat-empty">
        <el-icon :size="60" color="#909399"><ChatLineSquare /></el-icon>
        <p>选择一个对话或新建对话开始聊天</p>
      </div>

      <template v-else>
        <div class="message-list" ref="messageListRef">
          <div v-if="chatStore.loading" class="loading-center">
            <el-icon class="is-loading" :size="24"><Loading /></el-icon>
          </div>
          <div
            v-for="msg in chatStore.messages"
            :key="msg.id"
            class="message-item"
            :class="msg.role"
          >
            <div class="message-avatar">
              <el-avatar :size="36" :icon="msg.role === 'user' ? UserFilled : ChatDotSquare" :style="{ background: msg.role === 'user' ? '#409EFF' : '#67C23A' }" />
            </div>
            <div class="message-content">
              <div class="message-text">{{ msg.content }}</div>
              <div class="message-time">{{ formatDateTime(msg.created_at) }}</div>
            </div>
          </div>
          <div v-if="chatStore.sending" class="message-item assistant">
            <div class="message-avatar">
              <el-avatar :size="36" icon="ChatDotSquare" style="background: #67C23A" />
            </div>
            <div class="message-content">
              <div class="message-text thinking-text">
                <span class="dot-pulse"></span>
              </div>
            </div>
          </div>
        </div>

        <div class="chat-input">
          <el-input
            v-model="inputText"
            type="textarea"
            :rows="3"
            placeholder="输入消息..."
            @keydown.enter.exact.prevent="handleSend"
            ref="inputRef"
          />
          <div class="input-actions">
            <span class="input-hint">Enter 发送，Shift+Enter 换行</span>
            <div class="input-right">
              <el-button v-if="chatStore.sending" type="danger" @click="handleStop">
                <el-icon><VideoPause /></el-icon>
                停止
              </el-button>
              <el-button v-else type="primary" @click="handleSend" :disabled="!canSend">
                发送
              </el-button>
            </div>
          </div>
        </div>
      </template>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, computed, onMounted, nextTick, watch } from 'vue'
import { useChatStore } from '../stores/chat'
import { ElMessage, ElMessageBox } from 'element-plus'
import { Plus, Delete, ChatLineSquare, UserFilled, ChatDotSquare, Loading, VideoPause, MagicStick, ArrowRight } from '@element-plus/icons-vue'

const chatStore = useChatStore()
const inputText = ref('')
const inputRef = ref<any>(null)
const messageListRef = ref<HTMLElement | null>(null)

const settingsOpen = ref(true)
const aiRole = ref('小美')
const aiPersonality = ref('温柔体贴的妹子')
const aiRegion = ref('广西')
const presetKey = ref('')

const presets = [
  { key: 'xiaomei', label: '小美（温柔体贴·广西）', role: '小美', personality: '温柔体贴的妹子', region: '广西' },
  { key: 'xiaoshuai', label: '小帅（阳光开朗·北京）', role: '小帅', personality: '阳光开朗的帅哥', region: '北京' },
  { key: 'xiaozhi', label: '小智（博学多才·上海）', role: '小智', personality: '博学多才的老师', region: '上海' },
  { key: 'xiaomeng', label: '小萌（活泼可爱·四川）', role: '小萌', personality: '活泼可爱的少女', region: '四川' },
  { key: 'custom', label: '自定义', role: '', personality: '', region: '' },
]

const applyPreset = (key: string) => {
  const p = presets.find(pp => pp.key === key)
  if (p && key !== 'custom') {
    aiRole.value = p.role
    aiPersonality.value = p.personality
    aiRegion.value = p.region
  }
}

const selectedIds = ref(new Set<number>())
const isAllSelected = computed(() => chatStore.conversations.length > 0 && selectedIds.value.size === chatStore.conversations.length)

const toggleSelect = (id: number, checked: boolean) => {
  const s = new Set(selectedIds.value)
  if (checked) s.add(id)
  else s.delete(id)
  selectedIds.value = s
}

const toggleSelectAll = (checked: boolean) => {
  if (checked) {
    selectedIds.value = new Set(chatStore.conversations.map(c => c.id))
  } else {
    selectedIds.value = new Set()
  }
}

const handleBatchDelete = async () => {
  const count = selectedIds.value.size
  if (count === 0) return
  try {
    await ElMessageBox.confirm(`确定要删除选中的 ${count} 个对话吗？`, '批量删除', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
    await Promise.all([...selectedIds.value].map(id => chatStore.deleteConversation(id)))
    selectedIds.value = new Set()
    ElMessage.success(`已删除 ${count} 个对话`)
  } catch {
    // 用户取消
  }
}

const saveAiSettings = async () => {
  await chatStore.updateAiSettings(aiRole.value, aiPersonality.value, aiRegion.value)
  ElMessage.success('AI角色设置已保存')
}

const loadCurrentSettings = () => {
  if (chatStore.currentConversationId) {
    aiRole.value = chatStore.currentAiRole
    aiPersonality.value = chatStore.currentAiPersonality
    aiRegion.value = chatStore.currentAiRegion
  }
}

watch(() => chatStore.currentConversationId, loadCurrentSettings)

const canSend = computed(() => inputText.value.trim().length > 0)

const scrollToBottom = async () => {
  await nextTick()
  if (messageListRef.value) {
    messageListRef.value.scrollTop = messageListRef.value.scrollHeight
  }
}

watch(() => chatStore.messages.length, scrollToBottom)
watch(() => chatStore.sending, (val) => { if (val) scrollToBottom() })

const handleSend = async () => {
  const text = inputText.value.trim()
  if (!text || chatStore.sending) return
  inputText.value = ''
  try {
    await chatStore.sendMessage(text, [])
  } catch {
    ElMessage.error('发送失败')
  }
}

const handleStop = async () => {
  await chatStore.stopGeneration()
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  const now = new Date()
  if (date.toDateString() === now.toDateString()) return '今天'
  return date.toLocaleDateString('zh-CN', { month: 'short', day: 'numeric' })
}

const formatDateTime = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleTimeString('zh-CN', { hour: '2-digit', minute: '2-digit' })
}

const handleNewConversation = async () => {
  try {
    await chatStore.createConversation()
  } catch {
    ElMessage.error('创建对话失败')
  }
}

const handleSelectConversation = async (id: number) => {
  await chatStore.selectConversation(id)
}

const handleDeleteConversation = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个对话吗？', '确认删除', {
      confirmButtonText: '确定', cancelButtonText: '取消', type: 'warning'
    })
    await chatStore.deleteConversation(id)
    ElMessage.success('对话已删除')
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  chatStore.fetchConversations()
})
</script>

<style scoped>
.chat-container {
  display: flex;
  height: calc(100vh - 60px);
  background: #f5f7fa;
}

.chat-sidebar {
  width: 280px;
  background: #fff;
  border-right: 1px solid #e4e7ed;
  display: flex;
  flex-direction: column;
}

.sidebar-header {
  padding: 16px;
  border-bottom: 1px solid #e4e7ed;
  display: flex;
  justify-content: space-between;
  align-items: center;
}

.sidebar-header h3 {
  margin: 0;
  font-size: 16px;
  color: #303133;
}

.header-btns {
  display: flex;
  gap: 4px;
}

.select-all-bar {
  padding: 4px 16px 0;
  border-bottom: 1px solid #e4e7ed;
}

.conversation-list {
  flex: 1;
  overflow-y: auto;
  padding: 8px;
}

.conversation-item {
  position: relative;
  display: flex;
  align-items: flex-start;
  gap: 6px;
  padding: 10px 8px;
  border-radius: 8px;
  cursor: pointer;
  transition: background 0.2s;
  margin-bottom: 4px;
}

.conversation-item:hover, .conversation-item.active, .conversation-item.selected {
  background: #ecf5ff;
}

.conversation-item.active {
  border-left: 3px solid #409EFF;
}

.conv-checkbox {
  margin-top: 2px;
}

.conv-info {
  flex: 1;
  min-width: 0;
  padding-right: 30px;
}

.conv-title {
  font-size: 14px;
  color: #303133;
  font-weight: 500;
  margin-bottom: 4px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.conv-meta {
  font-size: 12px;
  color: #909399;
  display: flex;
  gap: 12px;
}

.delete-btn {
  position: absolute;
  right: 8px;
  top: 50%;
  transform: translateY(-50%);
  opacity: 0;
  transition: opacity 0.2s;
}

.conversation-item:hover .delete-btn {
  opacity: 1;
}

.chat-main {
  flex: 1;
  display: flex;
  flex-direction: column;
  background: #fff;
}

.chat-empty {
  flex: 1;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  color: #909399;
  gap: 16px;
}

.message-list {
  flex: 1;
  overflow-y: auto;
  padding: 20px;
}

.loading-center {
  display: flex;
  justify-content: center;
  padding: 40px;
}

.message-item {
  display: flex;
  gap: 12px;
  margin-bottom: 20px;
}

.message-item.user {
  flex-direction: row-reverse;
}

.message-text {
  max-width: 500px;
  padding: 12px 16px;
  border-radius: 12px;
  line-height: 1.6;
  font-size: 14px;
  white-space: pre-wrap;
  word-break: break-word;
}

.message-item.user .message-text {
  background: #409EFF;
  color: white;
  border-bottom-right-radius: 4px;
}

.message-item.assistant .message-text {
  background: #f0f9eb;
  color: #303133;
  border-bottom-left-radius: 4px;
}

.message-time {
  font-size: 12px;
  color: #909399;
  margin-top: 4px;
}

.message-item.user .message-time {
  text-align: right;
}

.thinking-text {
  color: #909399 !important;
  font-style: italic;
}

.dot-pulse {
  display: inline-block;
  width: 8px;
  height: 8px;
  border-radius: 50%;
  background: #67C23A;
  animation: dotPulse 1.4s infinite ease-in-out;
}

@keyframes dotPulse {
  0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
  40% { opacity: 1; transform: scale(1); }
}

.chat-input {
  padding: 12px 20px 16px;
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}

.input-actions {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-top: 8px;
}

.input-hint {
  font-size: 12px;
  color: #909399;
}

.input-right {
  display: flex;
  gap: 8px;
}

.ai-settings {
  border-top: 1px solid #e4e7ed;
  background: #fafafa;
}

.settings-header {
  display: flex;
  align-items: center;
  gap: 8px;
  padding: 10px 16px;
  cursor: pointer;
  font-size: 13px;
  color: #606266;
  user-select: none;
}

.settings-header:hover {
  background: #f0f2f5;
}

.settings-body {
  padding: 0 12px 12px;
}

.setting-field {
  margin-bottom: 8px;
}

.setting-field label {
  display: block;
  font-size: 12px;
  color: #909399;
  margin-bottom: 4px;
}

.arrow-open {
  transform: rotate(90deg);
}
</style>