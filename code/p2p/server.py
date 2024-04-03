import asyncio
import websockets

async def server(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        # Process message if needed

print("Starting server")
start_server = websockets.serve(server, "10.12.156.179", 8765)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()