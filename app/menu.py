import server_handler
import shared
from graceful_exit import GracefulExit
from typing import Tuple
from validacao import validar_nome_cliente
from asyncio import run

def listar_clientes():
  clientes = server_handler.get_clientes()
  if not len(clientes): print("Nenhum cliente disponível")
  for cliente in clientes:
    print(cliente)

def solicitar_conexao():
  while 1:
    client_name = input("Nome do cliente que deseja conectar [0 para sair]:")
    if client_name.isnumeric() and int(client_name) == 0: return
    elif not validar_nome_cliente(client_name): print("Nome inválido, tente novamente.")
    else: break
  cliente = server_handler.obter_endereco_cliente(client_name)
  run(solicitar_conexao(cliente))

opcoes = [
  ("Listar clientes", listar_clientes),
  ("Solicitar conexão", solicitar_conexao)
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
    else:
      print("Opção desconhecida")