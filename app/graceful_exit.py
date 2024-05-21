from asyncio import get_event_loop
import signal

class GracefulExit(SystemExit):
  code = 1

def raise_graceful_exit(*args):
  get_event_loop().stop()
  print("Gracefully shutdown")
  raise GracefulExit()

for signame in {'SIGINT', 'SIGTERM'}:
  signal.signal(getattr(signal, signame), raise_graceful_exit)