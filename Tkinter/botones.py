from tkinter import Button
import customtkinter as ctk
from recursos import colors

class Buttons:

    def __init__(self):
        self.colors = colors.Colors()
    
    def create_button(self,master, texto, x, y, widht, height, func=None, pack=False, teamColor = False):
        self.color = getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}')
        if teamColor:
            self.color = self.colors.team
        if getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}') == self.colors.fondo_Dark: self.text_color = 'white'
        else: self.text_color = 'black'
        self.func = func
        self.button = ctk.CTkButton(master, text=texto, corner_radius=8, fg_color=(self.color), text_color= self.text_color, command=self.func)
        if pack:
            self.button.pack()
        else:
            self.button.place(relx=x, rely=y, relheight=height, relwidth=widht)
        return self.button
    
    
    def create_button2(self,master, texto, x, y, widht, height, func=None, agrandar=False):
        self.color = self.colors.team
        if getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}') == self.colors.fondo_Dark: self.text_color = 'white'
        else: self.text_color = 'white'
        self.func = func
        self.button = ctk.CTkButton(master, text=texto, corner_radius=8, fg_color=(self.color), text_color= self.text_color, command=self.func)
        if agrandar:
            height = 0.8
            widht = 0.8
        self.button.place(relx=x, rely=y, relheight=height, relwidth=widht)
        return self.button
    

