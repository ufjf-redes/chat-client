from asyncio import get_event_loop, all_tasks
import shared
import signal

class GracefulExit(SystemExit):
  code = 1

def raise_graceful_exit(*args):
  for task in all_tasks():
    task.cancel()
  for chat in shared.chat_threads.values():
    chat.stop()
  
  print("Gracefully shutdown")
  raise GracefulExit()

for signame in {'SIGINT', 'SIGTERM'}:
  signal.signal(getattr(signal, signame), raise_graceful_exit)