from tkinter import *


class Help_Dialog:

    def __init__(self, data_file=None, data=None):
        self.window = Tk()
        self.file_text = ""
        if data_file is not None:
            self.load_text(data_file)
        else:
            self.file_text = data
        self.add_components()
        self.window.mainloop()

    def load_text(self, file):
        with open(file, mode="r") as f:
            self.file_text = f.read()
            f.close()

    def add_components(self):
        scrollbar = Scrollbar(self.window)
        scrollbar.pack(side=RIGHT, fill=Y)

        label = Text(self.window)
        label.insert(END, str(self.file_text))
        label.config(width=75, height=15)
        label.config(yscrollcommand=scrollbar.set)
        label.pack(fill="both")
        Button(self.window, text="Ok", command=lambda: self.on_ok()).pack(fill="both")
        scrollbar.config(command=label.yview)
        label.config(xscrollcommand=scrollbar.set)

    def on_ok(self):
        self.window.destroy()
