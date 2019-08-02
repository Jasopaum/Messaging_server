import asyncio
import websockets
import json

CLIENTS = {}


async def register(name, websocket):
    if name in CLIENTS:
        to_send = json.dumps({"cmd": "usedname", "msg": f"{name} is already connected on this server."})
        await websocket.send(to_send)
    else:
        await notify_new_user(name)
        await init_list_users(websocket)
        CLIENTS[name] = websocket

async def unregister(websocket):
    # Remove client and corresponding websocket from dict of clients
    for k,v in CLIENTS.items():
        if v == websocket:
            v.close()
            del CLIENTS[k]
            break
    await notify_rm_user(k)  # k is the client who left

async def notify_new_user(name):
    # When a new client joins, add it to everybody's lists of users
    to_send = json.dumps({"cmd": "addusr", "usr": [name]})
    if CLIENTS:
        await asyncio.wait([ws.send(to_send) for c, ws in CLIENTS.items()])

async def init_list_users(ws):
    # When a new client joins, init its list of users
    to_send = json.dumps({"cmd": "addusr", "usr": list(CLIENTS.keys())})
    if CLIENTS:
        await ws.send(to_send)

async def notify_rm_user(name):
    to_send = json.dumps({"cmd": "rmusr", "usr": name})
    if CLIENTS:
        await asyncio.wait([c.send(to_send) for c in CLIENTS.values()])

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

            elif message["cmd"] == "unregister":
                # Client wants to send message
                await unregister(websocket)

    except:
        await unregister(websocket)

start_server = websockets.serve(main, "localhost", 1234)

asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
