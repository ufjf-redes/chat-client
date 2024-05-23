from requests import Session, exceptions
import shared
from enum import Enum
import shared

get_server_url = lambda: 'http://localhost:5000'

class Endpoints(Enum):
  ME_REGISTRAR = '/me-registrar'
  LISTAR_CLIENTES = '/lista-clientes'
def build_url(endpoint: Endpoints):
  return f"{get_server_url()}/{endpoint.value}"

http = Session()
def me_registrar():
  http.headers.update({
    "client-name": shared.nome_cliente
  })
  try:
    response = http.post(build_url(Endpoints.ME_REGISTRAR), data = {
      "address": shared.socket_url
    })
    if(response.text):
      print(response.text)
  except exceptions.HTTPError as e:
    print("Erro ao se registrar no servidor")
    SystemExit(e)
    
def get_clientes() -> list[str]:
  return http.get(build_url(Endpoints.LISTAR_CLIENTES)).json()

def obter_endereco_cliente(nome_cliente: str) -> str:
  pass
