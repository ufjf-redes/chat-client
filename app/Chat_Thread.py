from enum import Enum
from cliente import Cliente
from threading import Thread, Event
from interface import Interface
from websockets.sync.server import ServerConnection
from websockets.exceptions import ConnectionClosedError, ConnectionClosedOK
from my_enum import StatusChat, MensagemSocket
import subprocess

class Chat_Thread:
  cliente: Cliente
  thread: Thread
  status: StatusChat
  socket: ServerConnection
  interface: Interface
  encerrado_event = Event()
  
  def __init__(self, cliente: Cliente, status: StatusChat, thread: Thread = None, socket: ServerConnection = None):
    self.cliente = cliente
    self.thread = thread
    self.status = status
    self.socket = socket
    self.interface = None
    
  def conectar(self):
    if self.status == StatusChat.ATIVO:
      return
    oldStatus = self.status
    self.status = StatusChat.ATIVO
    if oldStatus == StatusChat.SOLICITACAO_PENDENTE: 
      self.socket.send(MensagemSocket.ACEITAR_CONEXAO.value)
      self.thread = Thread(target = self.talk, daemon=True)
      self.thread.start()
    elif oldStatus == StatusChat.AGUARDANDO_ACEITE: 
      self.talk()
      
  def stop(self):
    self.socket.close()
    self.status = StatusChat.ENCERRADO
    self.encerrado_event.set()
    if self.interface is not None and self.interface.is_open():
      self.interface.close()
          
  def send(self, message: str):
    self.socket.send(message)
    self.interface.print(f"[Você]: {message}\n")
  
  def talk(self):
    self.interface = Interface(self.cliente.nome)
    self.interface.onClose = self.stop
    self.interface.onInput = self.send
    self.interface.print(f"Você está conversando com {self.cliente.nome}\n\n")
    try:
      for message in self.socket:
        self.interface.print(f"[{self.cliente.nome}]: {message}\n")
    except (ConnectionClosedOK, ConnectionClosedError):
      pass
    finally:
      self.stop()