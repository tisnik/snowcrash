import platform
from tkinter import *
import tkinter.simpledialog as sm
import tkinter.messagebox as ms
from tkinter import filedialog
from random import *
try:
    from app import settings, controler, help
except:
    import settings, controler, help

class Gui:
    def __init__(self):
        self.info_function=""
        self.settings=settings.import_setting("app/config.json")
        self.log=""
        self.master = Tk()
        self.master.geometry("500x500+0+0")
        self.master.minsize(300,180)
        self.master.tk_setPalette(self.settings['color'])
        if platform.system() == 'Windows':
            self.master.overrideredirect(True)
        self.outline_window = Frame(self.master, bg="Black", cursor="fleur")
        self.outline_window.pack(fill=BOTH)
        self.window = Frame(self.outline_window, cursor="arrow")
        self.window.pack(fill=BOTH, padx=4, pady=4)
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
        self.info_height=30
        self.info_frame=Frame(self.window, height = self.geometry[1]-self.info_height)
        self.info_frame.pack(fill=BOTH,side=BOTTOM)
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
                                  ["Exit", lambda: exit(0)]]],
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
                                ["X", "Button_right", lambda: exit(0)],
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
            self.info_frame.config(height=self.master.winfo_height()-self.info_height)
            self.menu.bind("<B1-Motion>",self.passs)
            self.outline_window.bind("<B1-Motion>", self.passs)
            self.outline_window.config(cursor="pirate")
        else:
            self.screen = "max"
            self.master.wm_state('normal')
            self.info_frame.config(height=self.geometry[1]-self.info_height)
            self.bind("<Control-p> <Control-P>", self.change_palette)
            self.menu.bind("<B1-Motion>", self.on_motion)
            self.outline_window.bind("<B1-Motion>", self.on_motion_resize)
            self.outline_window.config(cursor="fleur")
        
    def passs(self,mouse=False):
        pass

    def minimalize(self, null=False):
        self.master.overrideredirect(0)
        self.master.wm_state('iconic')

    def overrideredirect(self, null=False):
        if self.master.state() == 'iconic':
            self.master.overrideredirect(0)
        else:
            if platform.system() == 'Windows':
                self.master.overrideredirect(1)

    def change_palette(self,null=False):
        color="#{:06x}".format(randint(0, 0xFFFFFF))
        self.master.tk_setPalette(color)
        self.settings['color']=color
        settings.export_setting(self.settings,"app/config.json")

    def bind(self, what, todo):
        if todo == None:
            self.master.bind(what)
            return
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
        self.geometrymax = self.window.winfo_screenwidth, self.window.winfo_screenheight, 0, 0
        self.geometry[2:4] = self.geometry[2] + mouse.x - self.x, self.geometry[3] + mouse.y - self.y
        self.master.geometry("{}x{}+{}+{}".format(str(self.geometry[0]), str(self.geometry[1]), str(self.geometry[2]),
                                                  str(self.geometry[3])))
        self.info_frame.config(height = self.geometry[1] - self.info_height)

    def on_motion_resize(self, mouse=False):
        if self.geometry[0] + mouse.x - self.x >= 300 and self.geometry[0] + mouse.x - self.x <= self.window.winfo_screenwidth() and mouse.x >= self.window.winfo_width()-15:
            self.geometry[0] = self.geometry[0] + mouse.x - self.x
        elif self.geometry[0] + mouse.x - self.x >= 300 and self.geometry[0] + mouse.x - self.x <= self.window.winfo_screenwidth() and mouse.x <=15:
            self.geometry[0] = self.geometry[0] - mouse.x + self.x
            self.geometry[2] = self.geometry[2] + mouse.x - self.x
        if self.geometry[1] + mouse.y - self.y >= 180 and self.geometry[1] + mouse.y - self.y <= self.window.winfo_screenheight() and mouse.y >= self.window.winfo_height()-10:
            self.geometry[1] = self.geometry[1] + mouse.y - self.y
        elif self.geometry[1] + mouse.y - self.y >= 180 and self.geometry[1] + mouse.y - self.y <= self.window.winfo_screenheight() and mouse.y <=15:
            self.geometry[1] = self.geometry[1] - mouse.y + self.y
            self.geometry[3] = self.geometry[3] + mouse.y - self.y
        self.y=mouse.y
        self.x=mouse.x
        self.master.geometry("{}x{}+{}+{}".format(str(self.geometry[0]), str(self.geometry[1]), str(self.geometry[2]),
                                                  str(self.geometry[3])))
        self.info_frame.config(height = self.geometry[1] - self.info_height)

    def printmenu(self, text, func, menu, null=False):
        if self.sub_menu.winfo_manager() != "pack":
            self.sub_menu.pack(side=LEFT, anchor=N)
            self.openMenu = menu
            for button in text:
                self.but.append(
                    Button(self.sub_menu, text=button[0], command=button[1], borderwidth=0, highlightthickness=0))
                self.but[-1].pack(side=TOP, fill=X, pady=(0, 2), padx=(0, 2))
                self.info_height=30+len(self.but)*22
        elif menu != self.openMenu:
            self.printmenu(text, func, self.openMenu, null)
            self.printmenu(text, func, menu, null)
        else:
            for but in self.but:
                but.destroy()
            self.sub_menu.pack_forget()
            self.but = []
            self.openMenu = ""
            self.info_height=30
        if self.master.state()=="normal":
            self.info_frame.config(height = self.geometry[1] - self.info_height)
        else:
            self.info_frame.config(height = self.master.winfo_height() - self.info_height)
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
            self.input_some("InsLog")
        elif inp == "LoadLog":
            self.clear_info()
            self.master.wm_state('withdraw')
            filename = filedialog.askopenfilename()
            self.master.wm_state('normal')
            filename=open(filename,'r')
            self.log=filename.read()
            filename.close()
        elif inp == "RATGL":
            self.master.withdraw()
            d = sm.askstring("Run app to get log", "Enter Command: ", parent=self.window)
            d = d.split(" ")
            d = controler.run_app(d)
            self.master.deiconify()
            print(d)
            self.log = d
        elif inp == "NoneDB":
            text = controler.get_processed_log(self.log)
            print(text)
            help.Help_Dialog(data=text)
        elif inp == "WithDB":
            text = controler.process_log(self.log)
            print(text)
            help.Help_Dialog(data=text)
        elif inp == "ShowDB":
            text = controler.show_db()
            print(text)
            help.Help_Dialog(data=text)
        elif inp == "AddSolu":
            self.master.withdraw()
            controler.add_solution(self.log, sm.askstring("Add solution", "Insert solution: "),
                                   sm.askinteger("Add solution", "Priority: "),
                                   ms.askyesno("Add solution", "Is solved?"))
            self.master.iconify()
        elif inp == "Solve":
            print("Not implemented yet")
        elif inp == "Setting":
            settings.init_settings(self.master)
        elif inp == "About":
            help.Help_Dialog(data_file="./ABOUT")
        elif inp == "Licence":
            help.Help_Dialog(data_file="./LICENCE")
        elif inp == "PlsHelp":
            help.Help_Dialog(data_file="./README.md")
        elif inp == "Update":
            print("Not implemented yet")
        print("haha")
        self.master.destroy()
        self.master.mainloop()

    def clear_info(self):
        if self.info_function == "input_some":
            for item in self.input_some_items:
                item.destroy()


    def input_some(self,what):
        self.clear_info()
        self.info_function="input_some"
        self.input_some_items=[]
        self.input_some_items.append(Label(self.info_frame,text="Insert Log",font=("Times", 24, "bold underline"),width=20))
        self.input_some_items[-1].place(x=50,y=50)
        self.input_some_items.append(Label(self.info_frame,text="Insert Log:",width=20))
        self.input_some_items[-1].place(x=-30,y=100)
        self.input_some_items.append(Text(self.info_frame,width=35,height=10))
        self.input_some_items[-1].insert("0.0",self.log)
        self.input_some_items[-1].place(x=100,y=100)
        self.input_some_items.append(Button(self.info_frame,text="Add Log",command=self.addLog))
        self.input_some_items[-1].place(x=400,y=100)
    
    def addLog(self):
        self.log=self.input_some_items[2].get("0.0",END)
        for item in self.input_some_items:
            item.destroy()

#if __name__ == "__main__":
gui = Gui()
