import customtkinter as ctk
from recursos import colors

class Label:

    def __init__(self):
        self.colors = colors.Colors()
    
    def create_label(self,master, texto, x, y, widht, height, letterSize = 16):
        self.color = getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}')
        if getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}') == self.colors.fondo_Dark: self.text_color = 'white'
        else: self.text_color = 'black'
        self.label = ctk.CTkLabel(master, text= texto, text_color=self.text_color, font=('Bold',letterSize))
        self.label.place(relx=x, rely=y, relheight=height, relwidth=widht)
        return self.label
    
