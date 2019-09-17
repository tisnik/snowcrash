from tkinter import *
from random import *
from app import controler, settings, help


# from .app import *

class Gui:
    def __init__(self):
        self.log = ""
        self.master = Tk()
        self.master.geometry("500x500+0+0")
        self.master.minsize(300, 180)
        self.master.tk_setPalette("grey55")
        self.master.overrideredirect(1)
        self.outline_window = Frame(self.master, bg="Black", cursor="fleur")
        self.outline_window.pack(fill=BOTH, ipadx=2, ipady=2, padx=1, pady=1)
        self.window = Frame(self.outline_window, cursor="arrow")
        self.window.pack(fill=BOTH, ipadx=2, ipady=2)
        self.outline_window.bind("<ButtonPress-1>", lambda event, a="Press": self.move(a, event))
        self.outline_window.bind("<ButtonRelease-1>", lambda event, a="Release": self.move(a, event))
        self.outline_window.bind("<B1-Motion>", self.on_motion_resize)
        self.bind("<Control-r>", self.change_palette)
        self.bind("<Control-R>", self.change_palette)
        self.bind("<Map>", self.overrideredirect)
        self.bind("<Control-p> <Control-P>", self.change_palette)
        self.geometry = [500, 500, 50, 50]
        self.screen = "max"
        self.geometrymax = [self.window.winfo_screenwidth(), self.window.winfo_screenheight(), 0, 0]
        self.init_menu_bar()
        self.openMenu = ""
        self.master.mainloop()

    def init_menu_bar(self, null=False):
        self.menu_of_menues = Frame(self.window, width=self.geometry[0], relief=RIDGE, bg="darkblue")
        self.menu = Frame(self.menu_of_menues, width=self.geometry[0], relief=RIDGE)
        self.sub_menu = Frame(self.window, bg="darkblue")
        self.but = []
        self.menu_buttons = []
        list_of_menu_buttons = [["File", "Menu",
                                 [["Insert log", lambda: self.info("InsLog")],
                                  ["Load log", lambda: self.info("LoadLog")],
                                  ["Run app to get log", lambda: self.info("RATGL")],
                                  ["Set random Palette  Ctrl+P", self.change_palette],
                                  ["Exit", self.master.destroy]]],
                                ["Run", "Menu",
                                 [["Withou DB    Ctrl+Shift+R", lambda: self.info("NoneDB")],
                                  ["With DB        Ctrl+R", lambda: self.info("WithDB")],
                                  ["Show DB", lambda: self.info("ShowDB")],
                                  ["Add solution", lambda: self.info("AddSolu")],
                                  ["solve (add in future)", lambda: self.info("Solve")]]],
                                ["Setting", "Button", lambda: self.info("Setting")],
                                ["Help", "Menu",
                                 [["About", lambda: self.info("About")],
                                  ["Licence", lambda: self.info("Licence")],
                                  ["Pls help", lambda: self.info("PlsHelp")],
                                  ["Update", lambda: self.info("Update")]]],
                                ["X", "Button_right", self.master.destroy],
                                [u"⃞", "Button_right", self.maxmalize],
                                ["_", "Button_right", self.minimalize],
                                [u"⛄  SnowCrash", "Label_Center"]]
        for item in list_of_menu_buttons:
            if item[1] == "Label":
                self.menu_buttons.append(Label(self.menu, text=item[0]))
                self.menu_buttons[-1].pack(side=LEFT)
            elif item[1] == "Label_Center":
                self.menu_buttons.append(Label(self.menu, text=item[0]))
                self.menu_buttons[-1].pack()
            elif item[1] == "Menu":
                self.menu_buttons.append(Label(self.menu, text=item[0]))
                self.menu_buttons[-1].pack(side=LEFT)
                self.menu_buttons[-1].bind("<ButtonPress-1>",
                                           lambda event, a=item[2], b="Press", c=item[0]: self.printmenu(a, b, c,
                                                                                                         event))
            elif item[1] == "Button":
                self.menu_buttons.append(
                    Button(self.menu, text=item[0], command=item[2], borderwidth=0, highlightthickness=0))
                self.menu_buttons[-1].pack(side=LEFT)
            elif item[1] == "Button_right":
                self.menu_buttons.append(
                    Button(self.menu, text=item[0], command=item[2], borderwidth=0, highlightthickness=0))
                self.menu_buttons[-1].pack(side=RIGHT)
        self.line = Label(self.menu)
        self.menu_of_menues.pack(fill=X, side=TOP)
        self.menu.pack(padx=(0, 0), pady=(0, 2), fill=X)
        self.menu.bind("<ButtonPress-1>", lambda event, a="Press": self.move(a, event))
        self.menu.bind("<ButtonRelease-1>", lambda event, a="Release": self.move(a, event))
        self.menu.bind("<B1-Motion>", self.on_motion)

    def maxmalize(self, null=False):
        if self.screen == "max":
            self.screen = "ret"
            self.master.wm_state('zoomed')
        else:
            self.screen = "max"
            self.master.wm_state('normal')

    def minimalize(self, null=False):
        self.master.overrideredirect(0)
        self.master.wm_state('iconic')

    def overrideredirect(self, null=False):
        if self.master.state() == 'iconic':
            self.master.overrideredirect(0)
        else:
            self.master.overrideredirect(1)

    def change_palette(self, null=False):
        self.master.tk_setPalette("#{:06x}".format(randint(0, 0xFFFFFF)))

    def bind(self, what, todo):
        if " " in what:
            items = what.split(" ")
        else:
            items = [what]
        for item in items:
            self.master.bind(item, todo)

    def move(self, button, mouse):
        if button == "Release":
            self.x = None
            self.y = None
        else:
            self.x = mouse.x
            self.y = mouse.y
        self.geometrymax = [self.window.winfo_screenwidth(), self.window.winfo_screenheight(), 0, 0]

    def on_motion(self, mouse=False):
        self.geometry[2:4] = self.geometry[2] + mouse.x - self.x, self.geometry[3] + mouse.y - self.y
        self.master.geometry("{}x{}+{}+{}".format(str(self.geometry[0]), str(self.geometry[1]), str(self.geometry[2]),
                                                  str(self.geometry[3])))

    def on_motion_resize(self, mouse=False):
        self.geometry[0:2] = self.geometry[0] + mouse.x - self.x, self.geometry[1] + mouse.y - self.y
        self.move("Press", mouse)
        self.master.geometry("{}x{}+{}+{}".format(str(self.geometry[0]), str(self.geometry[1]), str(self.geometry[2]),
                                                  str(self.geometry[3])))

    def printmenu(self, text, func, menu, null=False):
        if self.sub_menu.winfo_manager() != "pack":
            self.sub_menu.pack(side=LEFT, anchor=N)
            self.openMenu = menu
            for button in text:
                self.but.append(
                    Button(self.sub_menu, text=button[0], command=button[1], borderwidth=0, highlightthickness=0))
                self.but[-1].pack(side=TOP, fill=X, pady=(0, 2), padx=(0, 2))
        elif menu != self.openMenu:
            self.printmenu(text, func, self.openMenu, null)
            self.printmenu(text, func, menu, null)
        else:
            for but in self.but:
                but.pack_forget()
            self.sub_menu.pack_forget()
            self.but = []
            self.openMenu = ""

    def info(self, inp, null=False):
        """ 
        "Insert log"         - "InsLog"     -
        "Load log"           - "LoadLog"    - Load Log from file to gui
        "Run app to get log" - "RATGL"      - controler.run_app()
        "Withou DB"          - "NoneDB"     - controler.get_processed_log(self.log)
        "With DB"            - "WithDB"     - controler.process_log(self.log)
        "Show DB"            - "ShowDB"     - controler.show_db()
        "Add solution"       - "AddSolu"    - controler.Add_solution()
        "solve"              - "Solve"      - controler.add_solution(log,solution,priority)
        "Setting"            - "Setting"    - settings.init_settings()
        "About"              - "About"      -
        "Licence"            - "Licence"    -
        "Pls help"           - "PlsHelp"    -
        "Update"             - "Update"     -
        """
        if inp == "InsLog":
            pass
        elif inp == "LoadLog":
            pass
        elif inp == "RATGL":
            controler.run_app()
        elif inp == "NoneDB":
            controler.get_processed_log(self.log)
        elif inp == "WithDB":
            controler.process_log(self.log)
        elif inp == "ShowDB":
            controler.show_db()
        elif inp == "AddSolu":
            pass
        elif inp == "Solve":
            pass
        elif inp == "Setting":
            settings.init_settings()
        elif inp == "About":
            help.Help_Dialog("../ABOUT")
        elif inp == "Licence":
            help.Help_Dialog("../LICENCE")
        elif inp == "PlsHelp":
            help.Help_Dialog("../README.md")
        elif inp == "Update":
            print("Not implemented yet")


if __name__ == "__main__":
    gui = Gui()
