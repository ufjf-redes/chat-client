import websockets
import subprocess
from enum import Enum

class MensagemSocket(Enum):
  SOLICITAR_CONEXAO
  ACEITAR_CONEXAO
  RECUSAR_CONEXAO

async def solicitar_conexao(endereco_ws: str):
  async with websockets.connect(f"ws://{endereco_ws}") as websocket:
    await websocket.send(MensagemSocket.SOLICITAR_CONEXAO)
    resposta = await websocket.recv()
    if resposta == MensagemSocket.ACEITAR_CONEXAO:
      print("Conexão aceita com sucesso!")
      subprocess.Popen(["python", "seu_script.py"])
    else: print('Conexão recusada!')