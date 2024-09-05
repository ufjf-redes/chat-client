import shared
import json
from websockets.sync import server as websockets
from websockets.sync import client as websockets_client
from enum import Enum
from validacao import validar_nome_cliente
from cliente import Cliente
from chat_thread import Chat_Thread
from my_enum import MensagemSocket, StatusChat
from threading import Thread, current_thread
from time import sleep
import concurrent.futures

socket_headers = dict()
def inicializar_socket_headers():
  socket_headers["client-name"] = shared.me.nome

def send_error(socket: websockets.ServerConnection, error: str):
  socket.send(json.dumps({"error": error}))
  socket.close()
  raise websockets.exceptions.InvalidMessage

def handle_conexao(websocket: websockets.ServerConnection):
  client_name: str = websocket.request.headers.get("client-name")
  nome_valido = validar_nome_cliente(client_name)
  try:
    if not nome_valido: send_error(websocket, "Nome inválido")
    message = websocket.recv()
    if message != MensagemSocket.SOLICITAR_CONEXAO.value: websocket.send(json.dumps({"error": "Mensagem inválida"}))
    thread_aberta = shared.chat_threads.get(client_name)
    if thread_aberta is not None: send_error(websocket, "Conexão já solicitada ou ativa")
    print(f"Conexão solicitada por {client_name}")
  except websockets.exceptions.InvalidMessage: return
  shared.chat_threads[client_name] = Chat_Thread(
    Cliente(client_name, websocket.remote_address), 
    StatusChat.SOLICITACAO_PENDENTE,
    socket = websocket,
  )
  while not shared.chat_threads[client_name].encerrado_event.is_set():
    sleep(2)
  websocket.close()
  
def websocket_handler(websocket: websockets.ServerConnection): 
  with concurrent.futures.ThreadPoolExecutor() as executor:
    executor.submit(handle_conexao, websocket)

def solicitar_conexao_a_endereco(cliente: Cliente):
  endereco_com_protocolo = f"ws://{cliente.endereco}"
  print(f"Se conectando ao endereço {endereco_com_protocolo}")
  socket = websockets_client.connect(endereco_com_protocolo, additional_headers=socket_headers)
  print('Conectado com sucesso!')
  socket.send(MensagemSocket.SOLICITAR_CONEXAO.value)
  print("Enviando solicitação...")
  resposta = socket.recv()
  if resposta == MensagemSocket.ACEITAR_CONEXAO.value:
    print("Conexão aceita com sucesso!")
    chat = shared.chat_threads.get(cliente.nome)
    chat.socket = socket
    chat.conectar()
  else: 
    socket.close()
    print('Conexão recusada')
    erro = json.loads(resposta).get("error")
    print(f"Erro: {erro}")