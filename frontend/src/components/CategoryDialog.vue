<template>
  <el-dialog 
    :model-value="visible" 
    @update:model-value="$emit('update:visible', $event)"
    title="分类管理"
    width="500px"
  >
    <div class="category-section">
      <div class="add-category">
        <el-input 
          v-model="newCategoryName" 
          placeholder="请输入分类名称" 
          style="width: 200px; margin-right: 10px;"
        />
        <el-color-picker v-model="newCategoryColor" style="margin-right: 10px;" />
        <el-button type="primary" @click="handleAdd" :disabled="!newCategoryName">
          添加
        </el-button>
      </div>
      
      <el-divider />
      
      <div class="category-list">
        <div 
          v-for="category in categories" 
          :key="category.id" 
          class="category-item"
        >
          <div class="category-info">
            <span 
              class="category-color" 
              :style="{ backgroundColor: category.color }"
            ></span>
            <span class="category-name">{{ category.name }}</span>
          </div>
          <el-button 
            type="danger" 
            link 
            size="small"
            @click="$emit('delete', category.id)"
          >
            删除
          </el-button>
        </div>
        
        <el-empty v-if="categories.length === 0" description="暂无分类" />
      </div>
    </div>
  </el-dialog>
</template>

<script setup lang="ts">
import { ref } from 'vue'
import { Category } from '../api/task'

defineProps<{
  visible: boolean
  categories: Category[]
}>()

const emit = defineEmits<{
  'update:visible': [value: boolean]
  create: [name: string, color: string]
  delete: [id: number]
}>()

const newCategoryName = ref('')
const newCategoryColor = ref('#409EFF')

const handleAdd = () => {
  if (!newCategoryName.value) return
  emit('create', newCategoryName.value, newCategoryColor.value)
  newCategoryName.value = ''
  newCategoryColor.value = '#409EFF'
}
</script>

<style scoped>
.category-section {
  padding: 10px 0;
}

.add-category {
  display: flex;
  align-items: center;
  margin-bottom: 20px;
}

.category-list {
  max-height: 300px;
  overflow-y: auto;
}

.category-item {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding: 10px;
  border-bottom: 1px solid #ebeef5;
}

.category-item:last-child {
  border-bottom: none;
}

.category-info {
  display: flex;
  align-items: center;
}

.category-color {
  width: 16px;
  height: 16px;
  border-radius: 50%;
  margin-right: 10px;
}

.category-name {
  font-size: 14px;
  color: #303133;
}
</style>