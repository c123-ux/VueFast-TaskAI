<template>
  <div class="home-container">
    <div class="home-header">
      <div class="header-actions">
        <el-button type="primary" @click="editingTask = null; showTaskForm = true">
          <el-icon><Plus /></el-icon>
          新建任务
        </el-button>
        <el-button @click="showCategoryDialog = true">
          <el-icon><Setting /></el-icon>
          分类管理
        </el-button>
      </div>
    </div>
        <div class="filter-section">
          <el-select v-model="filterStatus" placeholder="任务状态" clearable @change="loadTasks">
            <el-option label="待办" :value="0" />
            <el-option label="进行中" :value="1" />
            <el-option label="已完成" :value="2" />
          </el-select>
          
          <el-select v-model="filterPriority" placeholder="优先级" clearable @change="loadTasks">
            <el-option label="低" :value="1" />
            <el-option label="中" :value="2" />
            <el-option label="高" :value="3" />
          </el-select>
          
          <el-select v-model="filterCategory" placeholder="分类" clearable @change="loadTasks">
            <el-option 
              v-for="category in store.categories" 
              :key="category.id" 
              :label="category.name" 
              :value="category.id" 
            />
          </el-select>
        </div>
        
        <TaskList 
          :tasks="store.tasks" 
          :loading="store.loading"
          @edit="editTask"
          @delete="deleteTask"
          @change-status="changeTaskStatus"
        />

        <TaskForm
          :visible="showTaskForm"
          :task="editingTask"
          :categories="store.categories"
          @update:visible="showTaskForm = $event; if(!$event) editingTask = null"
          @submit="handleTaskSubmit"
        />

        <CategoryDialog
          :visible="showCategoryDialog"
          :categories="store.categories"
          @update:visible="showCategoryDialog = $event"
          @create="handleCategoryCreate"
          @delete="handleCategoryDelete"
        />
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { useTaskStore } from '../stores/task'
import { Task, TaskCreate, TaskUpdate } from '../api/task'
import TaskList from '../components/TaskList.vue'
import TaskForm from '../components/TaskForm.vue'
import CategoryDialog from '../components/CategoryDialog.vue'
import { Plus, Setting } from '@element-plus/icons-vue'
import { ElMessage, ElMessageBox } from 'element-plus'

const store = useTaskStore()

const showTaskForm = ref(false)
const showCategoryDialog = ref(false)
const editingTask = ref<Task | null>(null)
const filterStatus = ref<number | undefined>(undefined)
const filterPriority = ref<number | undefined>(undefined)
const filterCategory = ref<number | undefined>(undefined)

const loadTasks = () => {
  const params: { status?: number; priority?: number; category_id?: number } = {}
  if (filterStatus.value !== undefined) params.status = filterStatus.value
  if (filterPriority.value !== undefined) params.priority = filterPriority.value
  if (filterCategory.value !== undefined) params.category_id = filterCategory.value
  store.fetchTasks(params)
}

const editTask = (task: Task) => {
  editingTask.value = task
  showTaskForm.value = true
}

const deleteTask = async (task: Task) => {
  try {
    await ElMessageBox.confirm('确定要删除这个任务吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await store.deleteTask(task.id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

const changeTaskStatus = async (task: Task, status: number) => {
  try {
    await store.updateTask(task.id, { status })
    ElMessage.success('状态更新成功')
  } catch (error) {
    ElMessage.error('状态更新失败')
  }
}

const handleTaskSubmit = async (taskData: TaskCreate | TaskUpdate) => {
  try {
    if (editingTask.value) {
      await store.updateTask(editingTask.value.id, taskData as TaskUpdate)
      ElMessage.success('更新成功')
    } else {
      await store.createTask(taskData as TaskCreate)
      ElMessage.success('创建成功')
    }
    showTaskForm.value = false
    editingTask.value = null
  } catch (error) {
    ElMessage.error('操作失败')
  }
}

const handleCategoryCreate = async (name: string, color: string) => {
  try {
    await store.createCategory({ name, color })
    ElMessage.success('分类创建成功')
  } catch (error) {
    ElMessage.error('分类创建失败')
  }
}

const handleCategoryDelete = async (id: number) => {
  try {
    await ElMessageBox.confirm('确定要删除这个分类吗？', '确认删除', {
      confirmButtonText: '确定',
      cancelButtonText: '取消',
      type: 'warning'
    })
    await store.deleteCategory(id)
    ElMessage.success('删除成功')
  } catch {
    // 用户取消
  }
}

onMounted(() => {
  store.fetchTasks()
  store.fetchCategories()
})
</script>

<style scoped>
.home-container {
  padding: 20px;
  max-width: 1400px;
  margin: 0 auto;
}

.home-header {
  margin-bottom: 20px;
}

.header-actions {
  display: flex;
  gap: 10px;
}

.filter-section {
  display: flex;
  gap: 10px;
  margin-bottom: 20px;
}

.filter-section .el-select {
  width: 150px;
}
</style>