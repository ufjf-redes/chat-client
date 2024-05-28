import websockets
import shared
from subprocess import Popen, CREATE_NEW_CONSOLE
from enum import Enum
from validacao import validar_nome_cliente
from Cliente import Cliente
from Chat_Thread import Chat_Thread, StatusChat
import subprocess
import json

socket_headers = dict()
def inicializar_socket_headers():
  socket_headers["client-name"] = shared.me.nome

class MensagemSocket(Enum):
  SOLICITAR_CONEXAO = 'SOLICITAR_CONEXAO'
  ACEITAR_CONEXAO = 'ACEITAR_CONEXAO'

async def websocket_handler(websocket: websockets.server.WebSocketServerProtocol, path: str) -> None: 
  client_name: str = websocket.request_headers.get("client-name")
  nome_valido = validar_nome_cliente(client_name)
  if not nome_valido:
    await websocket.send(json.dumps({"error": "Nome de cliente inválido"}))
    await websocket.close()
    return
  async for message in websocket:
    if message == MensagemSocket.SOLICITAR_CONEXAO.value:
      thread_aberta = shared.chat_threads.get(client_name)
      if thread_aberta:
        await websocket.send(json.dumps({"error": "Conexão já solicitada ou ativa"}))
        continue
      print(f"Conexão solicitada por {client_name}")
      shared.chat_threads[client_name] = Chat_Thread(
        Cliente(client_name, websocket.remote_address), 
        websocket, 
        StatusChat.SOLICITACAO_PENDENTE
      )

async def solicitar_conexao_a_endereco(cliente: Cliente):
  endereco_com_protocolo = f"ws://{cliente.endereco}"
  print(f"Solicitando conexão ao endereço {endereco_com_protocolo}")
  async with websockets.connect(endereco_com_protocolo, extra_headers=socket_headers) as socket:
    await socket.send(MensagemSocket.SOLICITAR_CONEXAO.value)
    print("Conexão solicitada")
    resposta = await socket.recv()
    if resposta == MensagemSocket.ACEITAR_CONEXAO.value:
      print("Conexão aceita com sucesso!")
      chat = shared.chat_threads.get(cliente.nome)
      chat.socket = socket
      chat.conectar()
    else: 
      print('Conexão recusada')
      erro = json.loads(resposta).get("error")
      print(f"Erro: {erro}")