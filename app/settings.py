from tkinter import *
from tkinter import filedialog
from tkinter.colorchooser import askcolor
from tkinter.font import *
from json import dumps, loads, decoder
import os


def get_path(path=None):
        if path:
            return path
        else:
            return input("Please enter path of your config file: ")

def import_setting(path=None):
    path = get_path(path)
    if os.path.isfile(path):
        try:
            with open(path) as f:
                return loads(f.read(), strict=False)
        except decoder.JSONDecodeError as error:
            print(error)
            print("File:\"{}\" is not JSON".format(path))
            return False
    else:
        print("File:\"{}\" not exist".format(path))
        return False

def export_setting(setting, path=None):
    path = get_path(path)
    try:
        with open(path, "w") as f:
            f.write(dumps(setting))
            return True
    except NotADirectoryError as error:
        print(error)
        print("Not existing directory: {}".foramt(path))
    except decoder.JSONDecodeError as error:
            print(error)
            print("Setting: \"{}\" is not JSON".format(setting))
    return False



class Settings(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.listbox = None
        self.db = None
        self.theme = None
        self.parent = parent
        self.setting = None
        self.list_of_pages = ['Database', 'Theme', 'Close']
        self.pack(fill=BOTH, expand=True)
        self.init_list_settings()

    def init_list_settings(self):
        self.listbox = Listbox(self, selectmode=SINGLE, font=Font(size=14))
        self.listbox.pack(side=LEFT, anchor="w", padx=0, fill=Y, expand=True)
        self.listbox.bind('<<ListboxSelect>>', lambda event: self.onclick_list_event())
        for i in range(len(self.list_of_pages)):
            self.listbox.insert(i, self.list_of_pages[i])

    def onclick_list_event(self):
        selection = self.listbox.curselection()[0]
        if selection == 0:
            self.show_db_settings()
        elif selection == 1:
            self.show_theme_settings()
        elif selection == self.listbox.size() - 1:
            self.parent.quit()

    def show_db_settings(self):
        if self.theme is not None:
            self.theme.pack_forget()
            self.theme = None
        if self.db is None:
            self.db = DBSettings(self)

    def show_theme_settings(self):
        if self.db is not None:
            self.db.pack_forget()
            self.db = None
        if self.theme is None:
            self.theme = ThemeSettings(self)


class DBSettings(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.db_file_file = "memory.db"
        self.pack(side=LEFT, ipadx=10000, fill=BOTH, expand=True)
        self.show_settings()

    def show_settings(self):
        Label(self, text="Database configuration", width=int(self.parent.winfo_width() / 30), font=Font(size=30)) \
            .grid(row=0, column=0, columnspan=3)
        Label(self, text="Database location: ").grid(row=1, column=0, sticky="we")
        self.db_file = Entry(self)
        self.db_file.grid(row=1, column=1, sticky="we")
        file = Button(self, text="Select file", command=lambda: self.onclick_event(button="select_file"))
        file.grid(row=1, column=2)

        Label(self, text=" ").grid(row=2, column=0, pady=self.parent.winfo_height() / 2.5)
        ok = Button(self, text="OK", command=lambda: self.onclick_event(button="ok"))
        ok.grid(row=2, column=0, sticky="es")
        apply = Button(self, text="Apply", command=lambda: self.onclick_event(button="apply"))
        apply.grid(row=2, column=1, sticky="wes")
        cancel = Button(self, text="Cancel", command=lambda: self.onclick_event("cancel"))
        cancel.grid(row=2, column=2, sticky="ws")

    def onclick_event(self, button):
        if button == 'cancel':
            self.parent.parent.quit()
        elif button == 'ok':
            self.db_file_file = self.db_file.get()
            self.parent.parent.quit()
        elif button == 'apply':
            self.db_file_file = self.db_file.get()
        elif button == 'select_file':
            filename = filedialog.askopenfilename()
            self.db_file.delete(0, 'end')
            self.db_file.insert(0, filename)


class ThemeSettings(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.color = "grey55"
        self.pack(side=LEFT, ipadx=10000, fill="both", expand=True)
        self.show_settings()

    def show_settings(self):
        Label(self, text="Theme configuration", width=int(self.parent.winfo_width() / 30), font=Font(size=30)) \
            .grid(row=0, column=0, columnspan=3)
        Label(self, text="Theme color: ").grid(row=1, column=0)
        self.color_picker = Button(self, text="Pick color", command=lambda: self.onclick_event(button="color_picker"))
        self.color_picker.grid(row=1, column=1)

        Label(self, text=" ").grid(row=2, column=0, pady=self.parent.winfo_height() / 2.5)
        ok = Button(self, text="OK", command=lambda: self.onclick_event(button="ok"))
        ok.grid(row=2, column=0, sticky="es")
        apply = Button(self, text="Apply", command=lambda: self.onclick_event(button="apply"))
        apply.grid(row=2, column=1, sticky="wes")
        cancel = Button(self, text="Cancel", command=lambda: self.onclick_event("cancel"))
        cancel.grid(row=2, column=2, sticky="ws")

    def onclick_event(self, button):
        if button == "color_picker":
            self.color = askcolor(color=self.color, parent=self, title="Pick color")
            self.color_picker.config(bg=self.color[1])
        elif button == 'ok':
            self.parent.parent.quit()
        elif button == 'apply':
            self.parent.parent.tk_setPalette(self.color[1])
        elif button == 'cancel':
            self.parent.parent.quit()


def init_settings():
    window = Tk()
    window.wm_attributes('-type', 'splash')
    window.geometry("1280x720")
    color = "grey55"
    window.tk_setPalette(color)
    app = Settings(window)
    app.mainloop()


if __name__ == "__main__":
    init_settings()
