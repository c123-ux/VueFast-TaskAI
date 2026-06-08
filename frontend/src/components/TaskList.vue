<template>
  <div class="task-list">
    <el-table 
      :data="tasks" 
      v-loading="loading" 
      stripe 
      style="width: 100%"
      empty-text="暂无任务"
    >
      <el-table-column label="状态" width="80">
        <template #default="{ row }">
          <el-select 
            :model-value="row.status" 
            @change="(value: number) => $emit('change-status', row, value)"
            size="small"
          >
            <el-option label="待办" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已完成" :value="2" />
          </el-select>
        </template>
      </el-table-column>
      
      <el-table-column prop="title" label="任务标题" min-width="200">
        <template #default="{ row }">
          <div class="task-title" :class="{ 'completed': row.status === 2 }">
            {{ row.title }}
          </div>
          <div v-if="row.description" class="task-description">
            {{ row.description }}
          </div>
        </template>
      </el-table-column>
      
      <el-table-column label="优先级" width="100">
        <template #default="{ row }">
          <el-tag :type="getPriorityType(row.priority)" size="small">
            {{ getPriorityText(row.priority) }}
          </el-tag>
        </template>
      </el-table-column>
      
      <el-table-column label="分类" min-width="150">
        <template #default="{ row }">
          <el-tag 
            v-for="category in row.categories" 
            :key="category.id" 
            :color="category.color"
            size="small"
            style="margin-right: 5px; color: white;"
          >
            {{ category.name }}
          </el-tag>
          <span v-if="row.categories.length === 0" class="no-category">无分类</span>
        </template>
      </el-table-column>
      
      <el-table-column label="截止日期" width="120">
        <template #default="{ row }">
          <span v-if="row.due_date" :class="{ 'overdue': isOverdue(row.due_date) }">
            {{ formatDate(row.due_date) }}
          </span>
          <span v-else class="no-date">未设置</span>
        </template>
      </el-table-column>
      
      <el-table-column label="操作" width="150" fixed="right">
        <template #default="{ row }">
          <el-button type="primary" link size="small" @click="$emit('edit', row)">
            编辑
          </el-button>
          <el-button type="danger" link size="small" @click="$emit('delete', row)">
            删除
          </el-button>
        </template>
      </el-table-column>
    </el-table>
  </div>
</template>

<script setup lang="ts">
import { Task } from '../api/task'

defineProps<{
  tasks: Task[]
  loading: boolean
}>()

defineEmits<{
  edit: [task: Task]
  delete: [task: Task]
  'change-status': [task: Task, status: number]
}>()

const getPriorityType = (priority: number) => {
  switch (priority) {
    case 1: return 'info'
    case 2: return 'warning'
    case 3: return 'danger'
    default: return 'info'
  }
}

const getPriorityText = (priority: number) => {
  switch (priority) {
    case 1: return '低'
    case 2: return '中'
    case 3: return '高'
    default: return '中'
  }
}

const formatDate = (dateStr: string) => {
  const date = new Date(dateStr)
  return date.toLocaleDateString('zh-CN')
}

const isOverdue = (dateStr: string) => {
  const date = new Date(dateStr)
  const today = new Date()
  today.setHours(0, 0, 0, 0)
  return date < today
}
</script>

<style scoped>
.task-list {
  background-color: white;
  border-radius: 8px;
  padding: 20px;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.1);
}

.task-title {
  font-size: 16px;
  font-weight: 500;
  color: #303133;
}

.task-title.completed {
  text-decoration: line-through;
  color: #909399;
}

.task-description {
  font-size: 14px;
  color: #606266;
  margin-top: 5px;
  overflow: hidden;
  text-overflow: ellipsis;
  white-space: nowrap;
}

.no-category, .no-date {
  color: #909399;
  font-size: 14px;
}

.overdue {
  color: #f56c6c;
  font-weight: 500;
}
</style>