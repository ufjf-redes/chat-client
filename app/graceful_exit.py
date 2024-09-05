import shared
import signal

class GracefulExit(SystemExit):
  code = 1

def raise_graceful_exit(*args):
  print("Gracefully shutdown")
  raise GracefulExit()

for signame in {'SIGINT', 'SIGTERM'}:
  signal.signal(getattr(signal, signame), raise_graceful_exit)