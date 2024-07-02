from time import sleep
import tkinter as tk
from tkinter.scrolledtext import ScrolledText
import threading, asyncio


class Interface(threading.Thread):
    title: str
    height = 20
    width = 100
    font = ("Courier New", "12")
    root: tk.Tk = None
    st: ScrolledText = None
    entry: tk.Entry = None
    send_button: tk.Button = None
    send_callback = None  # Callback function to send messages to the other user
    loop: asyncio.AbstractEventLoop = None

    def __init__(self, title="Terminal", send_callback=None):
        self.title = title
        self.st = None
        self.send_callback = send_callback
        self.loop = asyncio.new_event_loop()
        threading.Thread.__init__(self)
        self.daemon = True  # terminate when the main thread terminates
        self.start()
        sleep(0.5)  # wait for window to open

    def close(self):
        if self.root:
            self.root.destroy()
        self.root = None
        self.st = None

    def is_open(self):
        return self.root is not None

    def run(self):
        asyncio.set_event_loop(self.loop)
        self.root = tk.Tk()
        self.root.protocol("WM_DELETE_WINDOW", self.close)
        self.root.title(self.title)
        self.st = ScrolledText(self.root, height=self.height, width=self.width, font=self.font)
        self.st.pack()

        # Entry and send button
        self.entry = tk.Entry(self.root, font=self.font)
        self.entry.pack(fill=tk.X, padx=10, pady=5)
        self.send_button = tk.Button(self.root, text="Send", command=self.send_message)
        self.send_button.pack(pady=5)

        self.root.mainloop()

    def print(self, toPrint):
        if self.root is None or self.st is None:
            return None  # window has been closed; raise error?
        else:
            self.st.configure(state="normal")
            self.st.see("end")  # show last line printed (could also put this under "insert" but there would be a gap)
            self.st.insert("end", toPrint + "\n")
            self.st.configure(state="disabled")

    def send_message(self):
        message = self.entry.get()
        print(f"(interface.send_messge) mensagem: {message}")
        if message and self.send_callback:
            # Use run_coroutine_threadsafe to ensure the coroutine runs in the event loop
            print(f"Vai executar asyncio.ensure_future")
            asyncio.ensure_future(self.send_callback(message), loop=self.loop)
            self.print(f"executou asyncio.ensure_future Você: {message}")  # Display the message locally
            self.entry.delete(0, tk.END)