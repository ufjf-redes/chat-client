import asyncio
import shared
from validacao import validar_nome_cliente
from websockets import serve
from websockets.server import WebSocketServerProtocol, WebSocketServer
import socket as EnumSocketFamily
from server_handler import me_registrar
from graceful_exit import GracefulExit
from menu import exibirMenu
from sys import argv
from random import choices, choice
from string import ascii_lowercase, digits

get_client_host = lambda: 'localhost'
def criar_nome_cliente():
    if len(argv) <= 1 or not validar_nome_cliente(argv[1]):
        identifier = ''.join(choices(ascii_lowercase, k=4))
        print(f"Nome não inserido ou inválido, seu nome será {identifier}")
        shared.nome_cliente = identifier
    else:
        shared.nome_cliente = argv[1]
        print(f"Seja bem vindo, {shared.nome_cliente}!")

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
    criar_nome_cliente()
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
    