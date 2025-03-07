import customtkinter as ctk
from recursos import colors, botones

class Frames:

    def __init__(self):
        self.colors = colors.Colors()
        self.button = botones.Buttons()

    def create_frame(self, master, height, width, x=0, y=0):
            self.frame = ctk.CTkFrame(master)
            self.frame.place(relx=x, rely=y, relwidth= width, relheight=height)
            return self.frame

    def main_interfas_frame(self,master):
        self.master = master
        self.menu_frame = self.create_frame(self.master, 0.05,1)
        self.menu_frame.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'))
        self.interfas_frame = self.create_frame(self.master, 0.95, 1, y=0.05)
        self.interfas_frame.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'))
    
    def menu(self, cantidad, nombres):
        self.list_botones = {}
        for i in range (cantidad):
            self.function = nombres[i][1]
            self.list_botones[nombres[i][0]] = self.button.create_button(self.master, nombres[i][0], 0.17*i+0.01, 0.01, 0.12, 0.04, func=self.function)

