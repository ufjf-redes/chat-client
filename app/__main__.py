import asyncio
import shared
from websockets import serve
from websockets.server import WebSocketServerProtocol, WebSocketServer
import socket as EnumSocketFamily
from server_handler import me_registrar
from graceful_exit import GracefulExit
from menu import exibirMenu

get_client_host = lambda: 'localhost'

def create_url(server: WebSocketServer):
    sock = server.sockets[0]
    url: str
    if sock.family == EnumSocketFamily.AF_INET:
        url = "%s:%d" % sock.getsockname()
    elif sock.family == EnumSocketFamily.AF_INET6:
        url = "[%s]:%d" % sock.getsockname()[:2]
    elif sock.family == EnumSocketFamily.AF_UNIX:
        url = sock.getsockname()
    else:
        url = str(sock.getsockname())
    shared.socket_url = url
    
async def websocket_handler(websocket: WebSocketServerProtocol, path: str) -> None: 
    async for message in websocket:
        print(message)

async def start_ws_server():
    server: WebSocketServer = await serve(websocket_handler, get_client_host(), 0)
    create_url(server)
    me_registrar()
    print(f"WebSocket server running at {shared.socket_url}")
    shared.evento_socket_iniciado.set()
    
    try:

        await asyncio.Future()
    except GracefulExit:
        print("Received exit signal, shutting down...")
    finally:
        server.close()
        await server.wait_closed()
        print("WebSocket server stopped")

async def main():
    await asyncio.gather(
        asyncio.create_task(start_ws_server()), 
        asyncio.create_task(exibirMenu())    
    )
    
if __name__ == "__main__":
    asyncio.run(main())
    