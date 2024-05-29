from time import sleep
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading

class Interface(threading.Thread):
  title: str
  height = 20
  width = 100
  font = ("Courier New", "12")
  root: tk.Tk = None
  st: ScrolledText = None
  
  def __init__(self, title="Terminal"):
      self.title=title
      self.st = None
      threading.Thread.__init__(self)
      self.daemon = True  # terminate when the main thread terminates
      self.start()
      sleep(0.5)  # wait for window to open

  def close(self):
    self.root.destroy()
    self.root.update()
    self.root = None
    self.st = None

  def is_open(self):
    return self.root is not None

  def run(self):
      self.root = tk.Tk()
      self.root.protocol("WM_DELETE_WINDOW", self.close)
      self.root.title(self.title)
      self.st = ScrolledText(self.root, height=self.height, width=self.width, font=self.font)
      self.st.pack()
      self.root.mainloop()

  def print(self, toPrint):
      if self.root is None or self.st is None:
          return None  # window has been closed; raise error?
      else:
          self.st.configure(state="normal")
          self.st.see("end")  # show last line printed (could also put this under "insert" but there would be a gap)
          self.st.insert("end", toPrint)
          self.st.configure(state="disabled")