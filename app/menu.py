import server_handler
import shared
from graceful_exit import GracefulExit
from typing import Tuple
from validacao import validar_nome_cliente
from conexao_socket import solicitar_conexao_a_endereco
from util import input_nome_cliente
from Cliente import Cliente
from Chat_Thread import Chat_Thread
from my_enum import StatusChat
from threading import Thread

def listar_clientes():
  clientes = server_handler.get_clientes()
  if not len(clientes): print("Nenhum cliente disponível")
  print("\nClientes disponíveis:")
  for cliente in clientes:
    print(f"-> {cliente}")

def solicitar_conexao():
  client_name = input_nome_cliente("Nome do cliente que deseja conectar")
  if not client_name: return
  thread_aberta = shared.chat_threads.get(client_name)
  if thread_aberta:
    print("Conexão já solicitada ou ativa!")
    return
  cliente_endereco = server_handler.obter_endereco_cliente(client_name)
  cliente = Cliente(client_name, cliente_endereco)
  thread = Thread(target = solicitar_conexao_a_endereco, args = (cliente,), daemon=True)
  shared.chat_threads[client_name] = Chat_Thread(cliente, StatusChat.AGUARDANDO_ACEITE, thread = thread)
  thread.start()

def visualizar_solicitacoes():
  print("\nSolicitações de conexão:")
  for solicitacao in [chat for chat in shared.chat_threads.values() if chat.status == StatusChat.SOLICITACAO_PENDENTE]:
    print(solicitacao)

def aceitar_solicitacao():
  client_name = input_nome_cliente("Nome do cliente que deseja aceitar a conexão")
  if not client_name: return
  chat = shared.chat_threads.get(client_name)
  if not chat or chat.status != StatusChat.SOLICITACAO_PENDENTE:
    if chat.status == StatusChat.ATIVO: print("Conexão já ativa")
    else: print("Cliente não solicitou conexão")
    return
  chat.conectar()

opcoes = [
  ("Listar clientes", listar_clientes),
  ("Solicitar conexão", solicitar_conexao),
  ("Visualizar solicitações de conexão", visualizar_solicitacoes),
  ("Aceitar solicitação de conexão", aceitar_solicitacao),
]

def exibir_menu():
  while 1:
    print(f"\nMenu: [usuario: {shared.me.nome}]")
    for index, opcao in enumerate(opcoes):
      print(f"[{index}] - {opcao[0]}")
    print(f"[exit] - Sair")
    try:
      resposta = input()
    except (EOFError, KeyboardInterrupt):
      resposta = 'exit'
    if resposta == 'exit':
      shared.shutdown_server()
      continue
    if resposta.isnumeric() and int(resposta) < len(opcoes):
      opcoes[int(resposta)][1]()
    else:
      print("Opção desconhecida")