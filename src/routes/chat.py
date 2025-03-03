from typing import List, Dict, Set, Any
from uuid import UUID

from fastapi import WebSocket, Depends, FastAPI, HTTPException
from sqlalchemy.orm import Session
from starlette.websockets import WebSocketDisconnect

from src.aouth import get_current_user
from src.database import get_db
from src.models import Users
from src.models.chat import Chats, ChatMembers, Messages
from src.schemas.chat import CreateChat, ChatResponse, ChatMemberResponse, AddChatMember, CreateMessage
from src.utils import ChatType, MessageType
app = FastAPI()


class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[UUID, Set[WebSocket]] = {}

    async def connect(self, chat: Chats, websocket: WebSocket):

        await websocket.accept()

        if chat.id not in self.active_connections:
            self.active_connections[chat.id] = set()
        self.active_connections[chat.id].add(websocket)

    def disconnect(self, chat: Chats, websocket: WebSocket):
        self.active_connections[chat.id].remove(websocket)

    async def broadcast(self, chat: Chats, message: CreateMessage):
        for connection in self.active_connections.get(chat.id, set()):
            await connection.send_json(message.model_dump())

    async def shutdown(self):
        for connections in self.active_connections.values():
            for connection in connections:
                await connection.close()
        self.active_connections.clear()


connection_manager = ConnectionManager()


@app.websocket("/ws/chat/{chat_id}")
async def websocket_endpoint(websocket: WebSocket, chat: Chats, db: Session = Depends(get_db())):
    chat = db.query(Chats).filter(Chats.id == chat.id).first()

    if not chat:
        await websocket.close(code=1008)
        raise HTTPException(status_code=404, detail="Chat not found")

    await connection_manager.connect(chat, websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data["type"] == MessageType.EDITING:
                message = db.query(Messages).filter(Messages.id == data['id']).first()
                if message:
                    message.content = data["content"]
                    db.commit()
                    db.refresh(message)
                await connection_manager.broadcast(chat, CreateMessage.model_validate(message))
            else:
                new_message = Messages(chat_id=chat.id, content=data["content"])
                db.add(new_message)
                db.commit()
                db.refresh(new_message)
                await connection_manager.broadcast(chat, CreateMessage.model_validate(new_message))
    except WebSocketDisconnect:
        connection_manager.disconnect(chat, websocket)


@app.post("/chat/create")
def create_chat(chat: CreateChat, db: Session = Depends(get_db), user: Users = Depends(get_current_user)):
    old_chat = db.query(Chats).filter(Chats.id == chat.id).first()

    if old_chat:
        raise HTTPException(status_code=400, detail="Chat already exists")

    new_chat = Chats(owner_id=user.id, name=chat.name, chat_type=chat.chat_type)
    db.add(new_chat)
    db.commit()
    db.refresh(new_chat)

    first_member = ChatMembers(
        chat_id=new_chat.id,
        user_id=user.id,
    )

    db.add(first_member)
    db.commit()

    return {
        "message": "Successfully created chat",
        "owner": user.username,
        "name": new_chat.name,
        "created_at": new_chat.created_at,
        "members": new_chat.members}


@app.post("/chat/update/add_member/{chat_id}")
def add_member(chat_id: UUID, member: AddChatMember, db: Session = Depends(get_db)):
    chat = db.query(Chats).filter(Chats.id == chat_id).first()
    if not chat:
        raise HTTPException(status_code=404, detail="Chat not found")

    user = db.query(Users).filter(Users.id == member.user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    existing_member = db.query(ChatMembers).filter(ChatMembers.chat_id == chat.id,
                                                   ChatMembers.user_id == member.user_id).first()

    if existing_member:
        raise HTTPException(status_code=400, detail="User in group already")

    new_member = ChatMembers(
        chat_id=member.chat_id,
        user_id=member.user_id,
    )

    db.add(new_member)
    db.commit()

    return {"message": "User added to chat successfully.",
            "chat_name": chat.name,
            "username": new_member.user.username,
            "members": chat.members}

