from tkinter import *
from random import *

class Gui:
    def __init__(self):
        self.window = Tk()
        self.window.geometry("500x500+0+0")
        self.window.tk_setPalette("grey55")
        self.window.overrideredirect(1)
        self.bind("<Control-r>",self.change_palette)
        self.bind("<Control-Shift-r>",self.change_palette)
        self.bind("<Map>",self.overrideredirect)
        self.bind("<Control-p> <Control-P>",self.change_palette)
        self.geometry=[500,500,50,50]
        self.screen="max"
        self.geometrymax=[self.window.winfo_screenwidth(),self.window.winfo_screenheight(),0,0]
        self.init_menu_bar()
        self.openMenu=""
        self.window.mainloop()
    
    def init_menu_bar(self,null=False):
        self.menu_of_menues=Frame(self.window,width=self.geometry[0],relief=RIDGE, bg="darkblue")
        self.menu=Frame(self.menu_of_menues,width=self.geometry[0],relief=RIDGE)
        self.sub_menu=Frame(self.window,bg="darkblue")
        self.but=[]
        self.menu_buttons=[]
        list_of_menu_buttons=[["File","Menu",
                                [["Insert log",lambda: None],
                                ["Load log",lambda: None],
                                ["Run app to get log",lambda: None],
                                ["Set random Palette  Ctrl+P",lambda: self.change_palette()],
                                ["Exit",lambda: self.window.destroy()]]],
                            ["Run","Menu",
                                [["Withou DB    Ctrl+Shift+R",lambda: None],
                                ["With DB        Ctrl+R",lambda: None],
                                ["Show DB",lambda: None],
                                ["Add solution",lambda: None],
                                ["solve (add in future)",lambda: None]]],
                            ["Setting","Button",lambda:print("\r")],
                            ["Help","Menu",
                                [["About",lambda: None],
                                ["Licence",lambda: None],
                                ["Pls help",lambda: None],
                                ["Update",lambda: None]]],
                            ["X","Button_right",lambda:self.window.destroy()],
                            [u"⃞","Button_right",lambda:self.maxmalize()],
                            ["_","Button_right",lambda:self.minimalize()],
                            [u"⛄  SnowCrash","Label_Center"]]
        for item in list_of_menu_buttons:
            if item[1] == "Label": 
                self.menu_buttons.append(Label(self.menu,text=item[0]))
                self.menu_buttons[-1].pack(side=LEFT)
            elif item[1] == "Label_Center":
                self.menu_buttons.append(Label(self.menu,text=item[0]))
                self.menu_buttons[-1].pack()
            elif item[1] == "Menu":
                self.menu_buttons.append(Label(self.menu,text=item[0]))
                self.menu_buttons[-1].pack(side=LEFT)
                self.menu_buttons[-1].bind("<ButtonPress-1>",lambda event, a=item[2], b="Press", c=item[0]:self.printmenu(a,b,c,event))
            elif item[1] == "Button":
                self.menu_buttons.append(Button(self.menu,text=item[0],command=item[2], borderwidth=0, highlightthickness=0))     
                self.menu_buttons[-1].pack(side=LEFT)
            elif item[1] == "Button_right":
                self.menu_buttons.append(Button(self.menu,text=item[0],command=item[2], borderwidth=0, highlightthickness=0))  
                self.menu_buttons[-1].pack(side=RIGHT)
        self.line=Label(self.menu)
        self.menu_of_menues.pack(fill=X,side=TOP)
        self.menu.pack(padx=(0,0),pady=(0,2),fill=X)
        self.bind("<<MenuSlection>>",lambda event, a="Press": self.move(a,event))
        self.bind("<<MenuSlection>>",lambda event, a="Release": self.move(a,event))
        self.bind("<<MenuSelection-Motion>>",self.on_motion)

    def maxmalize(self,null=False):
        if self.screen=="max":
            self.screen="ret"
            self.window.wm_state('zoomed')
        else:
            self.screen="max"
            self.window.wm_state('normal')
    
    def minimalize(self,null=False):
        self.window.overrideredirect(0)
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

    def move(self,button,mouse):
        if button=="Release":
            self.x = None
            self.y = None
        else:
            self.x = mouse.x
            self.y = mouse.y
        
        self.geometrymax=[self.window.winfo_screenwidth(),self.window.winfo_screenheight(),0,0]

    def on_motion(self,mouse=False):
        self.geometry[2:4]=self.geometry[2]+mouse.x-self.x, self.geometry[3]+mouse.y-self.y
        self.window.geometry("{}x{}+{}+{}".format(str(self.geometry[0]),str(self.geometry[1]),str(self.geometry[2]),str(self.geometry[3])))
    
    def printmenu(self,text,func,menu,null=False):
        if self.sub_menu.winfo_manager() != "pack":
            self.sub_menu.pack(side=LEFT, anchor=N)
            self.openMenu=menu
            for button in text:
                self.but.append(Button(self.sub_menu,text=button[0],command=button[1], borderwidth=0, highlightthickness=0))
                self.but[-1].pack(side=TOP,fill=X,pady=(0,2),padx=(0,2))
        elif menu != self.openMenu:
            self.printmenu(text,func,self.openMenu,null)
            self.printmenu(text,func,menu,null)
        else:
            for but in self.but:
                but.pack_forget()
            self.sub_menu.pack_forget()
            self.but=[]
            self.openMenu=""

if __name__ == "__main__":
    gui = Gui()
