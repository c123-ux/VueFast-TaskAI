from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
import httpx
import os
import asyncio
from datetime import datetime
from dotenv import load_dotenv
from ..database import get_db
from ..models.chat import Conversation as ConversationModel, Message as MessageModel
from ..schemas.chat import (
    Conversation, ConversationCreate, ConversationUpdate, ConversationListItem,
    ChatRequest, ChatResponse, Message, StopResponse
)

load_dotenv()

router = APIRouter()

API_URL = "https://open.bigmodel.cn/api/paas/v4/chat/completions"

active_requests: dict[int, asyncio.Task] = {}

def get_api_key():
    api_key = os.getenv("ZHIPU_API_KEY")
    if not api_key or api_key == "your_api_key_here":
        raise HTTPException(status_code=500, detail="未配置API Key，请在 backend/.env 文件中设置")
    return api_key

# ─── 对话管理 ───

@router.get("/conversations", response_model=List[ConversationListItem])
def list_conversations(db: Session = Depends(get_db)):
    conversations = db.query(ConversationModel).order_by(ConversationModel.updated_at.desc()).all()
    result = []
    for conv in conversations:
        msg_count = len(conv.messages)
        result.append(ConversationListItem(
            id=conv.id,
            title=conv.title,
            ai_role=conv.ai_role,
            ai_personality=conv.ai_personality,
            ai_region=conv.ai_region,
            created_at=conv.created_at,
            updated_at=conv.updated_at,
            message_count=msg_count
        ))
    return result

@router.post("/conversations", response_model=Conversation)
def create_conversation(conv: ConversationCreate = ConversationCreate(), db: Session = Depends(get_db)):
    title = conv.title or datetime.now().strftime("%Y-%m-%d %H:%M")
    db_conv = ConversationModel(title=title)
    if conv.ai_role:
        db_conv.ai_role = conv.ai_role
    if conv.ai_personality:
        db_conv.ai_personality = conv.ai_personality
    if conv.ai_region:
        db_conv.ai_region = conv.ai_region
    db.add(db_conv)
    db.commit()
    db.refresh(db_conv)
    return db_conv

@router.patch("/conversations/{conversation_id}", response_model=Conversation)
def update_conversation(conversation_id: int, update: ConversationUpdate, db: Session = Depends(get_db)):
    db_conv = db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
    if db_conv is None:
        raise HTTPException(status_code=404, detail="对话不存在")
    if update.ai_role is not None:
        db_conv.ai_role = update.ai_role
    if update.ai_personality is not None:
        db_conv.ai_personality = update.ai_personality
    if update.ai_region is not None:
        db_conv.ai_region = update.ai_region
    db_conv.updated_at = datetime.now()
    db.commit()
    db.refresh(db_conv)
    return db_conv

@router.get("/conversations/{conversation_id}", response_model=Conversation)
def get_conversation(conversation_id: int, db: Session = Depends(get_db)):
    db_conv = db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
    if db_conv is None:
        raise HTTPException(status_code=404, detail="对话不存在")
    from ..schemas.chat import Message as MessageSchema
    msgs = db.query(MessageModel).filter(MessageModel.conversation_id == conversation_id).order_by(MessageModel.created_at).all()
    return Conversation(
        id=db_conv.id,
        title=db_conv.title,
        ai_role=db_conv.ai_role or "小美",
        ai_personality=db_conv.ai_personality or "温柔体贴的妹子",
        ai_region=db_conv.ai_region or "广西",
        created_at=db_conv.created_at,
        updated_at=db_conv.updated_at,
        messages=[MessageSchema(
            id=m.id, conversation_id=m.conversation_id,
            role=m.role, content=m.content,
            created_at=m.created_at
        ) for m in msgs]
    )

@router.delete("/conversations/{conversation_id}")
def delete_conversation(conversation_id: int, db: Session = Depends(get_db)):
    if conversation_id in active_requests:
        active_requests[conversation_id].cancel()
        del active_requests[conversation_id]
    db_conv = db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
    if db_conv is None:
        raise HTTPException(status_code=404, detail="对话不存在")
    db.delete(db_conv)
    db.commit()
    return {"message": "对话已删除"}

@router.get("/conversations/{conversation_id}/messages", response_model=List[Message])
def get_messages(conversation_id: int, db: Session = Depends(get_db)):
    db_conv = db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
    if db_conv is None:
        raise HTTPException(status_code=404, detail="对话不存在")
    msgs = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.created_at).all()
    result = []
    for m in msgs:
        result.append(Message(
            id=m.id,
            conversation_id=m.conversation_id,
            role=m.role,
            content=m.content,
            created_at=m.created_at
        ))
    return result

# ─── 停止生成 ───

@router.post("/conversations/{conversation_id}/stop", response_model=StopResponse)
def stop_generation(conversation_id: int):
    if conversation_id in active_requests:
        active_requests[conversation_id].cancel()
        del active_requests[conversation_id]
        return StopResponse(message="已停止生成")
    return StopResponse(message="没有正在进行的生成")

# ─── 发送消息 ───

@router.post("/conversations/{conversation_id}/messages", response_model=ChatResponse)
async def send_message(conversation_id: int, request: ChatRequest, db: Session = Depends(get_db)):
    db_conv = db.query(ConversationModel).filter(ConversationModel.id == conversation_id).first()
    if db_conv is None:
        raise HTTPException(status_code=404, detail="对话不存在")

    user_msg = MessageModel(
        conversation_id=conversation_id,
        role="user",
        content=request.content
    )
    db.add(user_msg)
    db.commit()
    db.refresh(user_msg)

    # 构建 system prompt（AI角色/性格/地区）
    role = db_conv.ai_role or "小美"
    personality = db_conv.ai_personality or "温柔体贴的妹子"
    region = db_conv.ai_region or "广西"
    system_prompt = (
        f"你现在扮演的角色是{role}，你的性格是{personality}，你来自{region}。\n"
        "请严格按照当前设定的角色、性格和地区来进行回复。\n"
        "请使用该地区特色的口语风格，在适当的地方添加表情符号让对话更生动。"
    )
    api_messages = [{"role": "system", "content": system_prompt}]

    # 构建历史（不含当前最新消息）
    all_msgs = db.query(MessageModel).filter(
        MessageModel.conversation_id == conversation_id
    ).order_by(MessageModel.created_at).all()

    for m in all_msgs[:-1]:
        api_messages.append({"role": m.role, "content": m.content})

    # 当前用户消息
    api_messages.append({"role": "user", "content": request.content})

    # 更新对话标题
    if db_conv.title in ("新对话", datetime.now().strftime("%Y-%m-%d %H:%M")):
        db_conv.title = request.content[:20] + ("..." if len(request.content) > 20 else "")

    api_key = get_api_key()

    try:
        task = asyncio.create_task(call_api(api_key, api_messages))
        active_requests[conversation_id] = task
        reply = await asyncio.wait_for(task, timeout=120)
    except asyncio.CancelledError:
        reply = "已停止生成"
    except asyncio.TimeoutError:
        reply = "请求超时，请重试"
    except Exception as e:
        reply = f"调用AI服务出错: {str(e)}"
    finally:
        if conversation_id in active_requests:
            del active_requests[conversation_id]

    # 保存AI回复
    assistant_msg = MessageModel(
        conversation_id=conversation_id,
        role="assistant",
        content=reply
    )
    db.add(assistant_msg)
    db_conv.updated_at = datetime.now()
    db.commit()
    db.refresh(assistant_msg)

    # 构建返回
    user_result = Message(
        id=user_msg.id, conversation_id=user_msg.conversation_id,
        role=user_msg.role, content=user_msg.content,
        created_at=user_msg.created_at
    )
    assistant_result = Message(
        id=assistant_msg.id, conversation_id=assistant_msg.conversation_id,
        role=assistant_msg.role, content=assistant_msg.content,
        created_at=assistant_msg.created_at
    )

    return ChatResponse(reply=reply, user_message=user_result, assistant_message=assistant_result)

# ─── 辅助函数 ───

async def call_api(api_key: str, messages: list) -> str:
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    payload = {
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 2048
    }
    async with httpx.AsyncClient(timeout=120) as client:
        response = await client.post(API_URL, json=payload, headers=headers)
        try:
            data = response.json()
        except Exception:
            return "AI服务响应解析失败，请稍后重试"
        if response.status_code == 200:
            return data.get("choices", [{}])[0].get("message", {}).get("content", "我现在有点累了，休息一下再回答你吧～")
        else:
            return "我现在有点累了，休息一下再回答你吧～"