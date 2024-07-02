from enum import Enum
from cliente import Cliente
from threading import Thread
from interface import Interface
from websockets.server import WebSocketServerProtocol
from asyncio import run, create_task, get_event_loop
from my_enum import StatusChat, MensagemSocket
import subprocess

class Chat_Thread:
    cliente: Cliente
    thread: Thread
    status: StatusChat
    socket: WebSocketServerProtocol
    interface: Interface

    def __init__(self, cliente: Cliente, status: StatusChat, thread: Thread = None, socket: WebSocketServerProtocol = None):
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
            self.thread = Thread(target=run, args=(self.enviar_aceite(),), daemon=True)
            self.thread.start()
        elif oldStatus == StatusChat.AGUARDANDO_ACEITE:
            get_event_loop().create_task(self.talk())

    def stop(self):
        if self.interface is not None and self.interface.is_open():
            self.interface.close()

    async def enviar_aceite(self):
        await self.socket.send(MensagemSocket.ACEITAR_CONEXAO.value)
        await self.talk()

    async def talk(self):
        self.interface = Interface(self.cliente.nome, send_callback=self.send_message)
        self.interface.print("Você está conversando com " + self.cliente.nome)
        async for message in self.socket:
          print(f"Recebendo mensagem: {message}")
          self.interface.print(f"[{self.cliente.nome}]: {message}")

    async def send_message(self, message):
        if self.socket:          
            print(f"Enviando mensagem: {message}")
            await self.socket.send(message)
            self.interface.print(f"Você: {message}")
        else:
          print(f"DEU MERDA")