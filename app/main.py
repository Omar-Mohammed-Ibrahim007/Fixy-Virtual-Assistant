# routes.py
from fastapi import APIRouter, WebSocket, WebSocketDisconnect
from app.routes import process_chat
from app.data_cleaner import cleaner_main
from app.ask import ask

router = APIRouter()
cleaner_main()

@router.websocket("/support/chatbot")
async def websocket_chat(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:
            # RECEIVE MESSAGE
            data = await websocket.receive_json()

            # PROCESS THROUGH API LAYER
            result = await process_chat(data)

            # SEND RESPONSE
            await websocket.send_json(result.model_dump())

    except WebSocketDisconnect:
        print("Client disconnected")


