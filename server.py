import asyncio
import websockets
import json

CLIENTS = {}


async def notify_new_user(name):

    list_users = [c for c in CLIENTS.keys()]
    to_send = json.dumps({"cmd": "notifusr", "usrs": list_users})
    if CLIENTS:
        await asyncio.wait([c.send(to_send) for c in CLIENTS.values()])

async def register(name, websocket):
    if name in CLIENTS:
        to_send = json.dumps({"cmd": "err", "msg": f"{name} is already connected on this server."})
        await websocket.send(to_send)
    else:
        print("NEW CLIENT: " + name)
        CLIENTS[name] = websocket
        await notify_new_user(name)

async def unregister(websocket):
    # Remove client and corresponding websocket from dict of clients
    for k,v in CLIENTS.items():
        if v == websocket:
            v.close()
            del CLIENTS[k]
            break

async def send_msg(src, dst, msg):
    try:
        to_send = json.dumps({"cmd": "recv", "src": src, "msg": msg})
        await CLIENTS[dst].send(to_send)
    except KeyError:
        to_send = json.dumps({"cmd": "err", "msg": f"{dst} is not connected on this server."})
        await CLIENTS[src].send(to_send)

async def main(websocket, path):
    try:
        async for message in websocket:
            message = json.loads(message)
            
            if message["cmd"] == "register":
                # New client arrived
                await register(message["name"], websocket)

            elif message["cmd"] == "send":
                # Client wants to send message
                await send_msg(message["src"], message["dst"], message["msg"])
    except:
        await unregister(websocket)

start_server = websockets.serve(main, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
