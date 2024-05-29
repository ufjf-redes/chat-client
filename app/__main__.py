import asyncio
import shared
from validacao import validar_nome_cliente
from websockets.server import WebSocketServerProtocol, WebSocketServer, serve
import socket as EnumSocketFamily
from server_handler import me_registrar
from graceful_exit import GracefulExit
from menu import exibir_menu
from sys import argv
from random import choices, choice
from string import ascii_lowercase, digits
from conexao_socket import websocket_handler, inicializar_socket_headers
from cliente import Cliente

get_client_host = lambda: 'localhost'
def criar_nome_cliente():
    if len(argv) <= 1 or not validar_nome_cliente(argv[1]):
        identifier = ''.join(choices(ascii_lowercase, k=4))
        print(f"Nome não inserido ou inválido, seu nome será {identifier}")
        return identifier
    else:
        return argv[1]

def criar_url(server: WebSocketServer):
    sock = server.sockets[0]
    if sock.family == EnumSocketFamily.AF_INET:
        return "%s:%d" % sock.getsockname()
    elif sock.family == EnumSocketFamily.AF_INET6:
        return "[%s]:%d" % sock.getsockname()[:2]
    elif sock.family == EnumSocketFamily.AF_UNIX:
        return sock.getsockname()
    else:
        return str(sock.getsockname())

def criar_cliente(server: WebSocketServer):
    shared.me = Cliente(criar_nome_cliente(), criar_url(server))
    print(f"Seja bem vindo, {shared.me.nome}!")

async def start_ws_server():
    server = await serve(websocket_handler, get_client_host(), 0)
    criar_cliente(server)
    me_registrar()
    inicializar_socket_headers()
    
    print(f"WebSocket server running at {shared.me.endereco}")
    menu_task = asyncio.create_task(exibir_menu())
    
    try:
        await asyncio.Future()
    except GracefulExit:
        print("Received exit signal, shutting down...")
    finally:
        menu_task.cancel()
        server.close()
        await server.wait_closed()
        print("WebSocket server stopped")

if __name__ == "__main__":
    asyncio.run(start_ws_server())
    