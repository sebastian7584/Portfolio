import customtkinter as ctk
from recursos import colors

class Checkbox:
        
    def __init__(self):
        self.colors = colors.Colors()
    
    def create_checkbox(self,master, texto, func, variable ,letterSize = 16, place= False, x=None, y=None, widht=None, height=None,):
        self.color = getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}')
        if getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}') == self.colors.fondo_Dark: self.text_color = 'white'
        else: self.text_color = 'black'
        self.checkbox = ctk.CTkCheckBox(master, text=texto, variable=variable, command=func, font=('Bold',letterSize), text_color=self.text_color)
        if place:
            self.checkbox.place(relx=x, rely=y, relheight=height, relwidth=widht)
        else:
            self.checkbox.pack(side="bottom", anchor="w")
        
        return self.checkbox