import tkinter as tk
from tkinter import filedialog
from modules.controller import Controller



class Application(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.controller = Controller()
        self.master = master
        self.master.geometry("960x640+300+300")
        self.master.title("MAPS")
        self.pack()
        self.create_widgets()

    def create_widgets(self):
        self.hi_there = tk.Button(self)
        self.hi_there["text"] = "Hello World\n(click me)"
        # self.hi_there["command"]
        self.hi_there.pack(side="top")

        self.quit = tk.Button(self, text="QUIT", fg="red",
                            command=self.master.destroy)
        self.quit.pack(side="bottom")

root = tk.Tk()
app = Application(master=root)
app.mainloop()