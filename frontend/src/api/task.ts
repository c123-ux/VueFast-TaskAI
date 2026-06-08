import axios from 'axios'

const api = axios.create({
  baseURL: '/api',
  timeout: 10000,
  headers: {
    'Content-Type': 'application/json'
  }
})

export interface Category {
  id: number
  name: string
  color: string
}

export interface Task {
  id: number
  title: string
  description?: string
  priority: number
  status: number
  due_date?: string
  created_at: string
  updated_at: string
  categories: Category[]
}

export interface TaskCreate {
  title: string
  description?: string
  priority?: number
  status?: number
  due_date?: string
  category_ids?: number[]
}

export interface TaskUpdate {
  title?: string
  description?: string
  priority?: number
  status?: number
  due_date?: string
  category_ids?: number[]
}

export interface CategoryCreate {
  name: string
  color?: string
}

// 任务 API
export const taskApi = {
  getTasks(params?: {
    status?: number
    priority?: number
    category_id?: number
  }) {
    return api.get<Task[]>('/tasks', { params })
  },

  getTask(id: number) {
    return api.get<Task>(`/tasks/${id}`)
  },

  createTask(task: TaskCreate) {
    return api.post<Task>('/tasks', task)
  },

  updateTask(id: number, task: TaskUpdate) {
    return api.put<Task>(`/tasks/${id}`, task)
  },

  deleteTask(id: number) {
    return api.delete(`/tasks/${id}`)
  }
}

// 分类 API
export const categoryApi = {
  getCategories() {
    return api.get<Category[]>('/categories')
  },

  createCategory(category: CategoryCreate) {
    return api.post<Category>('/categories', category)
  },

  deleteCategory(id: number) {
    return api.delete(`/categories/${id}`)
  }
}

export default api