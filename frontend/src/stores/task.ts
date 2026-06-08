import { defineStore } from 'pinia'
import { ref } from 'vue'
import { taskApi, categoryApi, Task, Category, TaskCreate, TaskUpdate, CategoryCreate } from '../api/task'

export const useTaskStore = defineStore('task', () => {
  const tasks = ref<Task[]>([])
  const categories = ref<Category[]>([])
  const loading = ref(false)

  const fetchTasks = async (params?: { status?: number; priority?: number; category_id?: number }) => {
    loading.value = true
    try {
      const response = await taskApi.getTasks(params)
      tasks.value = response.data
    } catch (error) {
      console.error('获取任务列表失败:', error)
      throw error
    } finally {
      loading.value = false
    }
  }

  const createTask = async (task: TaskCreate) => {
    try {
      const response = await taskApi.createTask(task)
      tasks.value.unshift(response.data)
      return response.data
    } catch (error) {
      console.error('创建任务失败:', error)
      throw error
    }
  }

  const updateTask = async (id: number, task: TaskUpdate) => {
    try {
      const response = await taskApi.updateTask(id, task)
      const index = tasks.value.findIndex(t => t.id === id)
      if (index !== -1) {
        tasks.value[index] = response.data
      }
      return response.data
    } catch (error) {
      console.error('更新任务失败:', error)
      throw error
    }
  }

  const deleteTask = async (id: number) => {
    try {
      await taskApi.deleteTask(id)
      tasks.value = tasks.value.filter(t => t.id !== id)
    } catch (error) {
      console.error('删除任务失败:', error)
      throw error
    }
  }

  const fetchCategories = async () => {
    try {
      const response = await categoryApi.getCategories()
      categories.value = response.data
    } catch (error) {
      console.error('获取分类列表失败:', error)
      throw error
    }
  }

  const createCategory = async (category: CategoryCreate) => {
    try {
      const response = await categoryApi.createCategory(category)
      categories.value.push(response.data)
      return response.data
    } catch (error) {
      console.error('创建分类失败:', error)
      throw error
    }
  }

  const deleteCategory = async (id: number) => {
    try {
      await categoryApi.deleteCategory(id)
      categories.value = categories.value.filter(c => c.id !== id)
    } catch (error) {
      console.error('删除分类失败:', error)
      throw error
    }
  }

  return {
    tasks,
    categories,
    loading,
    fetchTasks,
    createTask,
    updateTask,
    deleteTask,
    fetchCategories,
    createCategory,
    deleteCategory
  }
})