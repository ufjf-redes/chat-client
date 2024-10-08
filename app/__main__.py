import shared
from threading import Thread
from validacao import validar_nome_cliente
from websockets.sync.server import serve, WebSocketServer
import socket as EnumSocketFamily
from server_handler import me_registrar
from graceful_exit import GracefulExit
from menu import exibir_menu
from sys import argv
from random import choices, choice
from string import ascii_lowercase, digits
from conexao_socket import websocket_handler, inicializar_socket_headers
from Cliente import Cliente
from criptografia import generate_key

get_client_host = lambda: 'localhost'
def criar_nome_cliente():
  if len(argv) <= 1 or not validar_nome_cliente(argv[1]):
    identifier = ''.join(choices(ascii_lowercase, k=4))
    print(f"Nome não inserido ou inválido, seu nome será {identifier}")
    return identifier
  else:
    return argv[1]

def criar_url(server: WebSocketServer):
    if server.socket.family == EnumSocketFamily.AF_INET:
        return "%s:%d" % server.socket.getsockname()
    elif server.socket.family == EnumSocketFamily.AF_INET6:
        return "[%s]:%d" % server.socket.getsockname()[:2]
    elif server.socket.family == EnumSocketFamily.AF_UNIX:
        return server.socket.getsockname()
    else:
        return str(server.socket.getsockname())

def criar_cliente(server: WebSocketServer):
    shared.me = Cliente(criar_nome_cliente(), criar_url(server))
    print(f"Seja bem vindo, {shared.me.nome}!")

def start_ws_server():
    server: WebSocketServer = serve(websocket_handler, get_client_host(), 0)
    criar_cliente(server)
    me_registrar()
    inicializar_socket_headers()
    generate_key()
    
    print(f"WebSocket server running at {shared.me.endereco}")
    
    Thread(target = exibir_menu, daemon=True).start()
    shared.shutdown_server = server.shutdown
    try:
      server.serve_forever()
    except GracefulExit:
      print("Received exit signal, shutting down...")
    finally:
      for chat in shared.chat_threads.values():
        chat.stop()
      server.shutdown()
      print("WebSocket server stopped")
        
if __name__ == "__main__":
    start_ws_server()
    