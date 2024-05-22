import requests
import shared
from enum import Enum

get_client_name = lambda: 'teste'
get_server_url = lambda: 'http://localhost:5000'

class Endpoints(Enum):
  ME_REGISTRAR = '/registrar-cliente'
  LISTAR_CLIENTES = '/lista-clientes'
def build_url(endpoint: Endpoints):
  return f"{get_server_url()}/{endpoint.value}"


def me_registrar():
  try:
    response = requests.post(build_url(Endpoints.ME_REGISTRAR), {
      "name": get_client_name(),
      "address": shared.socket_url
    })
    if(response.text):
      print(response.text)
  except requests.exceptions.HTTPError as e:
    print("Erro ao se registrar no servidor")
    SystemExit(e)
    
def get_clientes() -> list[str]:
  clientes: list[str] = requests.get(build_url(Endpoints.LISTAR_CLIENTES)).json()
  return [cliente for cliente in clientes if cliente != get_client_name()]