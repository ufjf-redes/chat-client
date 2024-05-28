from validacao import validar_nome_cliente

def input_nome_cliente(descricao: str):
    while 1:
      client_name = input(f"{descricao} [0 para sair]: ")
      if client_name.isnumeric() and int(client_name) == 0: return
      elif not validar_nome_cliente(client_name): print("Nome inválido, tente novamente.")
      else: return client_name