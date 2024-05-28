from enum import Enum
from Cliente import Cliente
from threading import Thread
from websockets.server import WebSocketServerProtocol
from asyncio import run
import subprocess

class StatusChat(Enum): 
  ATIVO = 'ATIVO'
  AGUARDANDO_ACEITE = 'AGUARDANDO_ACEITE'
  SOLICITACAO_PENDENTE = 'SOLICITACAO_PENDENTE'

class Chat_Thread:
  cliente: Cliente
  thread: Thread
  status: StatusChat
  socket: WebSocketServerProtocol
  processo: subprocess.Popen
  
  def __init__(self, cliente: Cliente, thread: Thread, status: StatusChat, socket: WebSocketServerProtocol):
    self.cliente = cliente
    self.thread = thread
    self.status = status
    self.socket = socket
    
  def conectar():
    if self.status == StatusChat.ATIVO:
      return
      self.status = StatusChat.ATIVO
    if self.status == StatusChat.SOLICITACAO_PENDENTE: self.talk()
    elif self.status == StatusChat.AGUARDANDO_ACEITE: 
      self.thread = Thread(target = run, args = (self.talk,))
      self.thread.start()
    
  def send_message(message: str):
    self.processo.stdin.write(mensagem.encode('utf-8') + b'\n')
    self.processo.stdin.flush()
    
  async def talk():
    if self.status != StatusChat.ATIVO:
      return
    
    self.processo = subprocess.Popen(["py", "chat.py"], 
      stdin=subprocess.PIPE, 
      stdout=subprocess.PIPE, 
      stderr=subprocess.PIPE,
      universal_newlines=True,
      creationflags = subprocess.CREATE_NEW_CONSOLE
    )
    saida, erro = subprocesso.communicate()

    print("Saída do subprocesso:", saida)
    print("Erro do subprocesso:", erro)
