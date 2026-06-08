<template>
  <el-dialog 
    :model-value="visible" 
    @update:model-value="$emit('update:visible', $event)"
    :title="task ? '编辑任务' : '新建任务'"
    width="500px"
  >
    <el-form :model="form" label-width="80px">
      <el-form-item label="标题" required>
        <el-input v-model="form.title" placeholder="请输入任务标题" />
      </el-form-item>
      
      <el-form-item label="描述">
        <el-input 
          v-model="form.description" 
          type="textarea" 
          :rows="3"
          placeholder="请输入任务描述" 
        />
      </el-form-item>
      
      <el-form-item label="优先级">
        <el-select v-model="form.priority" placeholder="请选择优先级">
          <el-option label="低" :value="1" />
          <el-option label="中" :value="2" />
          <el-option label="高" :value="3" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="状态">
        <el-select v-model="form.status" placeholder="请选择状态">
          <el-option label="待办" :value="0" />
          <el-option label="进行中" :value="1" />
          <el-option label="已完成" :value="2" />
        </el-select>
      </el-form-item>
      
      <el-form-item label="截止日期">
        <el-date-picker
          v-model="form.due_date"
          type="date"
          placeholder="选择截止日期"
          format="YYYY-MM-DD"
          value-format="YYYY-MM-DDT00:00:00"
        />
      </el-form-item>
      
      <el-form-item label="分类">
        <el-select 
          v-model="form.category_ids" 
          multiple 
          placeholder="请选择分类"
        >
          <el-option 
            v-for="category in categories" 
            :key="category.id" 
            :label="category.name" 
            :value="category.id" 
          />
        </el-select>
      </el-form-item>
    </el-form>
    
    <template #footer>
      <el-button @click="$emit('update:visible', false)">取消</el-button>
      <el-button type="primary" @click="handleSubmit" :disabled="!form.title">
        确定
      </el-button>
    </template>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref, watch } from 'vue'
import { Task, TaskCreate, TaskUpdate, Category } from '../api/task'

const props = defineProps<{
  visible: boolean
  task: Task | null
  categories: Category[]
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  submit: [taskData: TaskCreate | TaskUpdate]
}>()

const form = ref<TaskCreate & { category_ids: number[] }>({
  title: '',
  description: '',
  priority: 2,
  status: 0,
  due_date: undefined,
  category_ids: []
})

watch(() => props.visible, (newVal) => {
  if (newVal && props.task) {
    form.value = {
      title: props.task.title,
      description: props.task.description || '',
      priority: props.task.priority,
      status: props.task.status,
      due_date: props.task.due_date,
      category_ids: props.task.categories.map(c => c.id)
    }
  } else if (newVal) {
    form.value = {
      title: '',
      description: '',
      priority: 2,
      status: 0,
      due_date: undefined,
      category_ids: []
    }
  }
})

const handleSubmit = () => {
  if (!form.value.title) return
  
  const taskData: TaskCreate | TaskUpdate = {
    title: form.value.title,
    description: form.value.description || undefined,
    priority: form.value.priority,
    status: form.value.status,
    due_date: form.value.due_date || undefined,
    category_ids: form.value.category_ids
  }
  
  emit('submit', taskData)
}
</script>