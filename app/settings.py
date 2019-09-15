from tkinter import *
from tkinter.font import *


class Settings(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.listbox = None
        self.db = None
        self.theme = None
        self.parent = parent
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
        self.pack(side=LEFT, ipadx=10000, fill=BOTH, expand=True)
        self.show_settings()

    def show_settings(self):
        Label(self, text="Database configuration", width=int(self.parent.winfo_width() / 30), font=Font(size=30)) \
            .grid(row=0, column=0, columnspan=3)
        Label(self, text="Database location: ").grid(row=1, column=0, sticky="we")
        db_file = Entry(self).grid(row=1, column=1, sticky="we")
        Button(self, text="Select file").grid(row=1, column=2)
        print(self.parent.winfo_height())
        Label(self, text=" ").grid(row=2, column=0, pady=self.parent.winfo_height()/2.5)
        Button(self, text="OK").grid(row=2, column=0, sticky="es")
        Button(self, text="Apply").grid(row=2, column=1, sticky="wes")
        Button(self, text="Cancel").grid(row=2, column=2, sticky="ws")


class ThemeSettings(Frame):

    def __init__(self, parent):
        super().__init__(parent)
        self.parent = parent
        self.pack(side=LEFT, ipadx=10000, fill="both", expand=True)
        self.show_settings()

    def show_settings(self):
        Label(self, text="Theme configuration", font=Font(size=30)).pack()


def init_settings():
    window = Tk()
    window.wm_attributes('-type', 'splash')
    window.geometry("1280x720")
    window.tk_setPalette("grey55")
    app = Settings(window)
    app.mainloop()


if __name__ == "__main__":
    init_settings()
