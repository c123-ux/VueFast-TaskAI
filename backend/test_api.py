"""测试所有后端API"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.database import Base, engine
from app.models.task import Task, Category

# 重置数据库
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)

from fastapi.testclient import TestClient
from app.main import app

client = TestClient(app)

def test(name, func):
    try:
        func()
        print(f"[PASS] {name}")
    except AssertionError as e:
        print(f"[FAIL] {name}: {e}")
    except Exception as e:
        import traceback
        traceback.print_exc()
        print(f"[ERROR] {name}: {e}")

# 测试1: 创建分类
def t1():
    r = client.post('/api/categories', json={'name': '工作', 'color': '#409EFF'})
    assert r.status_code == 200
    data = r.json()
    assert data['name'] == '工作'
    assert data['id'] == 1
    print(f"  分类: {data}")

# 测试2: 获取分类列表
def t2():
    r = client.get('/api/categories')
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 1
    print(f"  分类数量: {len(data)}")

# 测试3: 创建任务（不带分类）
def t3():
    r = client.post('/api/tasks', json={
        'title': '任务1',
        'description': '描述1',
        'priority': 2,
        'status': 0
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()
    assert data['title'] == '任务1'
    print(f"  任务: {data['id']}, 分类: {data['categories']}")

# 测试4: 创建任务（带分类）
def t4():
    r = client.post('/api/tasks', json={
        'title': '任务2',
        'description': '描述2',
        'priority': 3,
        'status': 0,
        'category_ids': [1]
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()
    assert data['title'] == '任务2'
    assert len(data['categories']) == 1
    print(f"  任务: {data['id']}, 分类: {[c['name'] for c in data['categories']]}")

# 测试5: 创建任务（带截止日期）
def t5():
    r = client.post('/api/tasks', json={
        'title': '任务3',
        'priority': 1,
        'status': 0,
        'due_date': '2026-06-10T00:00:00'
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()
    assert data['due_date'] is not None
    print(f"  任务: {data['id']}, 截止日期: {data['due_date']}")

# 测试6: 获取任务列表
def t6():
    r = client.get('/api/tasks')
    assert r.status_code == 200
    data = r.json()
    assert len(data) >= 3
    print(f"  任务数量: {len(data)}")

# 测试7: 按状态筛选
def t7():
    r = client.get('/api/tasks?status=0')
    assert r.status_code == 200
    data = r.json()
    print(f"  待办任务数量: {len(data)}")

# 测试8: 按优先级筛选
def t8():
    r = client.get('/api/tasks?priority=3')
    assert r.status_code == 200
    data = r.json()
    print(f"  高优先级任务数量: {len(data)}")

# 测试9: 按分类筛选
def t9():
    r = client.get('/api/tasks?category_id=1')
    assert r.status_code == 200
    data = r.json()
    print(f"  分类1的任务数量: {len(data)}")

# 测试10: 更新任务
def t10():
    r = client.put('/api/tasks/1', json={
        'title': '更新后的任务1',
        'status': 1
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()
    assert data['title'] == '更新后的任务1'
    assert data['status'] == 1
    print(f"  任务1已更新: {data['title']}, 状态: {data['status']}")

# 测试11: 更新任务（修改分类）
def t11():
    r = client.put('/api/tasks/1', json={
        'category_ids': []
    })
    assert r.status_code == 200, f"Expected 200, got {r.status_code}: {r.text}"
    data = r.json()
    assert len(data['categories']) == 0
    print(f"  任务1分类已清空")

# 测试12: 删除任务
def t12():
    r = client.delete('/api/tasks/3')
    assert r.status_code == 200
    print(f"  任务3已删除")

# 测试13: 删除不存在的任务
def t13():
    r = client.delete('/api/tasks/999')
    assert r.status_code == 404
    print(f"  正确返回404")

# 测试14: 删除分类
def t14():
    r = client.delete('/api/categories/2')
    assert r.status_code == 200
    print(f"  分类2已删除")

print("=" * 50)
print("开始测试...")
print("=" * 50)

test("创建分类", t1)
test("获取分类列表", t2)
test("创建任务（无分类）", t3)
test("创建任务（带分类）", t4)
test("创建任务（带截止日期）", t5)
test("获取任务列表", t6)
test("按状态筛选", t7)
test("按优先级筛选", t8)
test("按分类筛选", t9)
test("更新任务", t10)
test("更新任务分类", t11)
test("删除任务", t12)
test("删除不存在任务", t13)
test("删除分类", t14)

print("=" * 50)
print("测试完成")
print("=" * 50)