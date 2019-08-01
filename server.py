import asyncio
import websockets
import json

CLIENTS = {}

"""
async def notify_users():
    if CLIENTS:
        # Tell that new user arrived
"""

async def register(name, websocket):
    print("NEW CLIENT: " + name)
    CLIENTS[name] = websocket

"""
async def unregister(websocket):
    pass
"""

async def send_msg(src, dst, msg):
    to_send = json.dumps({"src": src, "msg": msg})
    await CLIENTS[dst].send(to_send)

async def main(websocket, path):
    async for message in websocket:
        message = json.loads(message)
        
        if message["cmd"] == "register":
            # New client arrived
            await register(message["name"], websocket)

        elif message["cmd"] == "send":
            # Client wants to send message
            await send_msg(message["src"], message["dst"], message["msg"])

start_server = websockets.serve(main, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
