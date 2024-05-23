def validar_nome_cliente(nome_cliente: str):
  return bool(nome_cliente) and type(nome_cliente) == str and nome_cliente.isidentifier()
  