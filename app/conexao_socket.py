import websockets
import shared
from subprocess import Popen, CREATE_NEW_CONSOLE
from enum import Enum
from validacao import validar_nome_cliente
from cliente import Cliente
from chat_thread import Chat_Thread
from my_enum import MensagemSocket, StatusChat
import subprocess
import json
import asyncio

socket_headers = dict()
def inicializar_socket_headers():
  socket_headers["client-name"] = shared.me.nome

async def send_error(socket: websockets.server.WebSocketServerProtocol, error: str):
  await socket.send(json.dumps({"error": error}))
  await socket.close()
  raise websockets.exceptions.InvalidMessage

async def websocket_handler(websocket: websockets.server.WebSocketServerProtocol, path: str) -> None: 
  client_name: str = websocket.request_headers.get("client-name")
  nome_valido = validar_nome_cliente(client_name)
  try:
    if not nome_valido: await send_error(websocket, "Nome inválido")
    message = await websocket.recv()
    print(f"(websocket_handler) Mensagem recebida: {message}")
    if message != MensagemSocket.SOLICITAR_CONEXAO.value: await websocket.send(json.dumps({"error": "Mensagem inválida"}))
    thread_aberta = shared.chat_threads.get(client_name)
    if thread_aberta is not None: await send_error(websocket, "Conexão já solicitada ou ativa")
    print(f"Conexão solicitada por {client_name}")
  except websockets.exceptions.InvalidMessage: return
  shared.chat_threads[client_name] = Chat_Thread(
    Cliente(client_name, websocket.remote_address), 
    StatusChat.SOLICITACAO_PENDENTE,
    socket = websocket, 
  )
  print(f"Chat_Thread criado para {client_name}")
  await websocket.wait_closed()


async def solicitar_conexao_a_endereco(cliente: Cliente):
  endereco_com_protocolo = f"ws://{cliente.endereco}"
  print(f"Se conectando ao endereço {endereco_com_protocolo}")
  socket = await websockets.connect(endereco_com_protocolo, extra_headers=socket_headers)
  print('Conectado com sucesso!')
  await socket.send(MensagemSocket.SOLICITAR_CONEXAO.value)
  print("Enviando solicitação...")
  resposta = await socket.recv()
  if resposta == MensagemSocket.ACEITAR_CONEXAO.value:
    print("Conexão aceita com sucesso!")
    chat = shared.chat_threads.get(cliente.nome)
    chat.socket = socket
    chat.conectar()
  else: 
    await socket.close()
    print('Conexão recusada')
    erro = json.loads(resposta).get("error")
    print(f"Erro: {erro}")