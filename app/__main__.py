import asyncio
import websockets
from graceful_exit import GracefulExit
from asyncio import get_event_loop
from websockets.server import WebSocketServerProtocol, WebSocketServer
from socket import AF_INET

def get_server_url() -> str:
    return 'http://localhost:5000'
def get_client_host() -> str:
    return '0.0.0.0'

def create_uri(server: WebSocketServer) -> str:
    sock = server.sockets[0]
    if sock.family == AF_INET:
        return "ws://%s:%d" % sock.getsockname()
    raise ValueError("IPv6 address detected. Only IPv4 addresses are allowed.")


async def websocket_handler(websocket: WebSocketServerProtocol, path: str) -> None: 
    async for message in websocket:
        print(message)

async def main() -> None:
    start_server = websockets.serve(websocket_handler, get_client_host(), 0)
    server: WebSocketServer = await start_server
    uri = create_uri(server)
    
    try:
        print(f"WebSocket server running at {uri}")
        await asyncio.Future()  # Run until interrupted
    except GracefulExit:
        print("Received exit signal, shutting down...")
    finally:
        server.close()
        await server.wait_closed()
        print("WebSocket server stopped")

if __name__ == "__main__":
    asyncio.run(main())