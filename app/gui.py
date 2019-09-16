from tkinter import *
from random import *

class Gui:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x500+0+0")
        self.window.tk_setPalette("grey55")
        self.window.overrideredirect(1)
        self.bind("<Control-r> <Control-Shift-R>",self.change_palette)
        self.bind("<Map>",self.overrideredirect)
        self.bind("<Control-p> <Control-P>",self.change_palette)
        self.geometry=[500,500,50,50]
        self.screen="max"
        self.geometrymax=[self.window.winfo_screenwidth(),self.window.winfo_screenheight(),0,0]
        self.init_menu_bar()
        self.window.mainloop()
    
    def init_menu_bar(self):
        self.menu_bar=Menu(self.window)
        list_of_menu_buttons=[["File","Menu",
                                [["Insert log",lambda: None],
                                ["Load log",lambda: None],
                                ["Run app to get log",lambda: None],
                                ["Set random Palette  Ctrl+P",lambda: self.change_palette()],
                                ["Exit",lambda: None]]],
                            ["Run","Menu",
                                [["Withou DB",lambda: None],
                                ["With DB Ctrl+R",lambda: None],
                                ["Show DB",lambda: None],
                                ["Add solution",lambda: None],
                                ["solve (add in future)",lambda: None]]],
                            ["Setting","Button",lambda:print("\r")],
                            ["Help","Menu",
                                [["About",lambda: None],
                                ["Licence",lambda: None],
                                ["Pls help",lambda: None],
                                ["Update",lambda: None]]],
                            [u"⛄","Label"],
                            ["SnowCrash","Label"],
                            ["_","Button_left",lambda:self.minimalize()],
                            ["⛄","Button",lambda:self.maxmalize()],
                            ["X","Button",lambda:self.window.destroy()]]
        for item in list_of_menu_buttons:
            if item[1] == "Label":
                self.menu_bar.add_command(label=item[0])
            elif item[1] == "Menu":
                widget=Menu(self.menu_bar, tearoff=0)
                for command in item[2]:
                    widget.add_command(label=command[0], command=command[1], background="grey95")
                self.menu_bar.add_cascade(label = item[0], menu=widget)
            elif item[1] == "Button":
                self.menu_bar.add_command(label=item[0],command=item[2])     
            elif item[1] == "Button_left":
                self.menu_bar.add_command(label=item[0],command=item[2])  
        self.window.config(menu=self.menu_bar)

    def maxmalize(self):
        if self.screen=="max":
            self.screen="ret"
            self.window.wm_state('zoomed')
        else:
            self.screen="max"
            self.window.wm_state('normal')
    
    def minimalize(self):
        self.window.wm_state('iconic')

    def overrideredirect(self,null=False):
        if self.window.state()=='iconic':
            self.window.overrideredirect(0)
        else:
            self.window.overrideredirect(1)

    def change_palette(self,null=False):
        self.window.tk_setPalette("#{:06x}".format(randint(0, 0xFFFFFF)))

    def bind(self,what,todo):
        if " " in what:
            items=what.split(" ")
        else:
            items=[what]
        for item in items:
            self.window.bind(item, todo)
gui=Gui()