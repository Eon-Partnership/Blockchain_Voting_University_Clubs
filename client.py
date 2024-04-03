import asyncio
import websockets

async def send_message():
    uri = "ws://10.12.156.179:8765"
    async with websockets.connect(uri) as websocket:
        await websocket.send("Hello Eric")
        print("Message sent")

asyncio.get_event_loop().run_until_complete(send_message())