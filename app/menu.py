from server_handler import get_clientes
from graceful_exit import GracefulExit
from typing import Tuple
import shared

def buscarClientes():
  clientes = get_clientes()
  for cliente in clientes:
    print(cliente)


opcoes = [
  ("Buscar clientes", buscarClientes)
]

async def exibirMenu():
  await shared.evento_socket_iniciado.wait()
  while 1:
    print("\nMenu:")
    for index, opcao in enumerate(opcoes):
      print(f"[{index}] - {opcao[0]}")
    print(f"[exit] - Sair")
    resposta = input()
    if resposta == 'exit':
      raise GracefulExit
    if resposta.isnumeric() and int(resposta) < len(opcoes):
      opcoes[int(resposta)][1]()
      break
    else:
      print("Opção desconhecida")