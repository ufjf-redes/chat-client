from cliente import Cliente
from chat_thread import Chat_Thread
from threading import Event
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPrivateKeyWithSerialization

me: Cliente
chat_threads = dict[str, Chat_Thread]()
shutdown_server = None
my_key: RSAPrivateKeyWithSerialization = None