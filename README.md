# Messaging_server

This is the implementation of a simple targeted chat service.

Each user can send a message to a specified user after having logged in.

## Usage

- Run `python3 server.py`

- You can instantiate several clients by opening `index.html` in a web browser.

- Use the chat serive.

## Details

The backend server is implemented in Python3 and uses the asyncio library.

The client is implemented in a web browser (basic combination of HTML and JavaScript).

The server is a central actor in the system, all the messages transit here and client cannot communicate directly wih each other. Clients and server communicate via websockets.

## Requirements

Python3 and the websockets library are needed to run this project (I used Python version 3.7.3 and websockets version 7.0 when working on it).

## Possible further work

- Implement the server part in Go.

- Have a database to store historic of messages.
