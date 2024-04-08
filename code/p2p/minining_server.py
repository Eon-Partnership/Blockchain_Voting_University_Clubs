import asyncio
import websockets
import json

# This server simulates 1 Miner
ip_address = "10.12.143.86"
port = 8765

async def server(websocket, path):
    async for message in websocket:
        print(f"Received message: {message}")
        # Process message if needed

# Main
start_server = websockets.serve(server, ip_address, port)

# This needs to be explored/mpodified
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
