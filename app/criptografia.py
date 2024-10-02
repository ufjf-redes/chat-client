from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
import shared

def generate_key():
  shared.my_key = rsa.generate_private_key(public_exponent=65537, key_size=2048)
  
def get_public_key():
  return shared.my_key.public_key().public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
  )
  
def criptografar(mensagem: str, cliente_public_key: rsa.RSAPublicKey):
  encrypted_message = cliente_public_key.encrypt(
    mensagem.encode(),
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )
  return encrypted_message
  
def descriptografar(mensagem: str):
  decrypted= shared.my_key.decrypt(
    mensagem,
    padding.OAEP(
      mgf=padding.MGF1(algorithm=hashes.SHA256()),
      algorithm=hashes.SHA256(),
      label=None
    )
  )
  return decrypted.decode()