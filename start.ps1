# 个人任务计划管理应用 - 一键启动脚本
Write-Host "正在启动后端服务..." -ForegroundColor Green
$backend = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d D:\待办事项管理应用2\todo-app\backend && uvicorn app.main:app --host 127.0.0.1 --port 8000" -WindowStyle Normal -PassThru
Start-Sleep -Seconds 3

Write-Host "正在启动前端服务..." -ForegroundColor Green
$frontend = Start-Process -FilePath "cmd.exe" -ArgumentList "/c", "cd /d D:\待办事项管理应用2\todo-app\frontend && npm run dev" -WindowStyle Normal -PassThru

Write-Host ""
Write-Host "==================================" -ForegroundColor Cyan
Write-Host "  后端: http://localhost:8000" -ForegroundColor Green
Write-Host "  前端: http://localhost:5173" -ForegroundColor Green
Write-Host "  API文档: http://localhost:8000/docs" -ForegroundColor Green
Write-Host "==================================" -ForegroundColor Cyan