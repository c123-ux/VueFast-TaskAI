<template>
  <el-config-provider :locale="zhCn">
    <el-container style="min-height: 100vh">
      <el-header class="nav-header">
        <div class="nav-content">
          <div class="nav-brand">个人任务计划管理</div>
          <div class="nav-menu">
            <router-link to="/" class="nav-item" :class="{ active: $route.path === '/' }">
              <el-icon><List /></el-icon>
              任务管理
            </router-link>
            <router-link to="/chat" class="nav-item" :class="{ active: $route.path === '/chat' }">
              <el-icon><ChatLineSquare /></el-icon>
              AI 助手
            </router-link>
          </div>
        </div>
      </el-header>
      <el-main class="nav-main">
        <router-view />
      </el-main>
    </el-container>
  </el-config-provider>
</template>

<script setup lang="ts">
import zhCn from 'element-plus/dist/locale/zh-cn.mjs'
import { List, ChatLineSquare } from '@element-plus/icons-vue'
</script>

<style>
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
}

body {
  font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
  background-color: #f5f7fa;
}

.nav-header {
  background: #fff;
  border-bottom: 1px solid #e4e7ed;
  box-shadow: 0 2px 8px rgba(0, 0, 0, 0.06);
  padding: 0 20px;
  height: 60px;
  display: flex;
  align-items: center;
  position: sticky;
  top: 0;
  z-index: 100;
}

.nav-content {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  max-width: 1400px;
  margin: 0 auto;
}

.nav-brand {
  font-size: 18px;
  font-weight: 600;
  color: #303133;
}

.nav-menu {
  display: flex;
  gap: 8px;
}

.nav-item {
  display: flex;
  align-items: center;
  gap: 6px;
  padding: 8px 16px;
  border-radius: 8px;
  text-decoration: none;
  color: #606266;
  font-size: 14px;
  transition: all 0.2s;
}

.nav-item:hover {
  background: #ecf5ff;
  color: #409EFF;
}

.nav-item.active {
  background: #ecf5ff;
  color: #409EFF;
  font-weight: 500;
}

.nav-main {
  padding: 0;
  background: #f5f7fa;
}
</style>