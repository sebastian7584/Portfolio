from tkinter import Canvas
from recursos import colors, botones, create_frame, label
from navegacion import *
import customtkinter as ctk
from PIL import ImageTk, Image


class App:

    def __init__ (self, geometry, title, version, alertas):
        self.version = version
        self.label = label.Label()
        self.colors = colors.Colors()
        self.button =botones.Buttons()
        self.create_frame = create_frame.Frames().create_frame
        self.theme = 'dark'
        self.texto_theme = 'Modo Noche'
        ctk.set_appearance_mode(self.theme)
        ctk.set_default_color_theme('dark-blue')
        self.root = ctk.CTk()
        #self.root.iconbitmap
        self.geometry = geometry
        self.root.geometry(geometry)
        self.root.title(title)
        self.main_frames()
        self.screen = ''
        self.estadopanel = True
        self.alertas = alertas
    
    def cambiarTamaño(self, valor):
        if valor:
            self.main_frames()
            self.root.geometry(f'{self.geometry}+0+0')
            self.root.overrideredirect(False)
        else:
            self.menu_frame.destroy()
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            window_width = 500
            window_height = 50
            x = int(screen_width/2 - window_width/2)
            y = 0
            self.root.overrideredirect(True)
            self.root.wm_attributes("-topmost", 1)
            self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")

    def desactivar_panel(self):
        self.button_activar_lineas.configure(state="disabled")
        self.button_compras.configure(state="disabled")
        self.button_equipos.configure(state="disabled")
        self.button_preactivador.configure(state="disabled")
        self.button_legalizador.configure(state="disabled")
        self.button_portas.configure(state="disabled")
        self.estadopanel = False

    def activar_panel(self):
        self.button_activar_lineas.configure(state="normal")
        self.button_compras.configure(state="normal")
        self.button_equipos.configure(state="normal")
        self.button_preactivador.configure(state="normal")
        self.button_legalizador.configure(state="normal")
        self.button_portas.configure(state="normal")
        self.estadopanel = True
        
    def on_of_panel(self, boolean):
        if boolean is False: self.desactivar_panel()
        else: self.activar_panel()
    
    def main_frames(self):
        self.menu_frame = self.create_frame(self.root, 1,0.15)
        self.interfas_frame = self.create_frame(self.root, 1, 0.85, x=0.15)
        self.menu()
        logo.Logo(self.interfas_frame, self.on_of_panel)

    
    def menu(self):
        self.button_activar_lineas = self.button.create_button(self.menu_frame, "TRIPLETAS", 0.10, 0.0, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.revisar_frame))
        self.button_compras = self.button.create_button(self.menu_frame, "COMPRAS", 0.10, 0.07, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.compras_frame))
        self.button_inventario_postpago = self.button.create_button(self.menu_frame, "INV POSTPAGO", 0.10, 0.14, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.inventario_postpago_frame))
        self.button_actualizar_precios = self.button.create_button(self.menu_frame, "ACT PRECIOS", 0.10, 0.21, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.actualizar_precio__frame))
        self.button_equipos = self.button.create_button(self.menu_frame, "EQUIPOS", 0.10, 0.28, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.equipos_frame))
        self.button_preactivador = self.button.create_button(self.menu_frame, "PREACTIVADOR", 0.10, 0.35, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.preactivador_frame))
        self.button_legalizador = self.button.create_button(self.menu_frame, "LEGALIZADOR", 0.10, 0.42, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.legalizador_frame))
        self.button_portas = self.button.create_button(self.menu_frame, "PORTAS", 0.10, 0.49, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.portas_frame))
        self.button_seriales = self.button.create_button(self.menu_frame, "SERIALES", 0.10, 0.56, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.consulta_seriales_frame))
        self.button_legalizador_sims = self.button.create_button(self.menu_frame, "LEG. SIMCARD", 0.10, 0.63, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.legalizador_sims_frame))
        self.button_recargas = self.button.create_button(self.menu_frame, "RECARGAS", 0.10, 0.70, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.recargas_frame))
        self.button_volantes = self.button.create_button(self.menu_frame, "VOLANTES", 0.10, 0.77, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.volantes_frame))
        # self.button_consulta_seriales = self.button.create_button(self.menu_frame, "CONS SERIALES", 0.10, 0.77, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.consulta_seriales2_frame))
        # self.button_comercial = self.button.create_button(self.menu_frame, "COMERCIAL", 0.10, 0.77, 0.8, 0.05, func= lambda: self.hide_menu_indicators(self.comercial_frame))
        self.canvas = Canvas(self.menu_frame, bg=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), bd=0.1, highlightbackground = getattr(self.colors,f'separador_{str(ctk.get_appearance_mode())}'))
        self.canvas.place(relwidth=0.01, relheight=1, relx=0.99)
        self.version = self.label.create_label(self.menu_frame, self.version, 0.1, 0.85, 0.8, 0.2, 10)
        self.switch_theme = ctk.CTkSwitch(self.menu_frame, text=self.texto_theme, command= lambda :self.change_theme()).place(relx=0.10, rely=0.96)

    
    def hide_menu_indicators(self, func):
        self.button_activar_lineas.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_compras.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_inventario_postpago.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_actualizar_precios.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_equipos.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_preactivador.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_legalizador.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_portas.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_seriales.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_legalizador_sims.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_recargas.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        self.button_volantes.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        # self.button_consulta_seriales.configure(fg_color=getattr(self.colors,f'fondo_{str(ctk.get_appearance_mode())}'), text_color=getattr(self.colors,f'text_{str(ctk.get_appearance_mode())}'))
        
    
        for frame in self.interfas_frame.winfo_children():
                frame.destroy()
        func()
    
    def revisar_frame(self):
        self.button_activar_lineas.configure(fg_color=self.colors.team, text_color='white')
        revisar_equipos.Revisar_equipos(self.interfas_frame, self.on_of_panel)
        self.screen = 'revisar_frame'
    
    def compras_frame(self):
        self.button_compras.configure(fg_color=self.colors.team, text_color='white')
        compras.Compras(self.interfas_frame, self.on_of_panel)
        self.screen = 'gestion_humana_frame'
    
    def inventario_postpago_frame(self):
        self.button_inventario_postpago.configure(fg_color=self.colors.team, text_color='white')
        inventario_postpago.Inventario_postpago(self.interfas_frame, self.on_of_panel)
        self.screen = 'gestion_humana_frame'
    
    def actualizar_precio__frame(self):
        self.button_actualizar_precios.configure(fg_color=self.colors.team, text_color='white')
        actualizar_precios.Actualizar_precios(self.interfas_frame, self.on_of_panel)
        self.screen = 'gestion_humana_frame'

    def equipos_frame(self):
        self.button_equipos.configure(fg_color=self.colors.team, text_color='white')
        equipos.Equipos(self.interfas_frame, self.on_of_panel, self.alertas)
        self.screen = 'contabilidad_frame'

    def preactivador_frame(self):
        self.button_preactivador.configure(fg_color=self.colors.team, text_color='white')
        preactivador.Preactivador(self.interfas_frame, self.on_of_panel, self.alertas)
        self.screen = 'comisiones_frame'

    def legalizador_frame(self):
        self.button_legalizador.configure(fg_color=self.colors.team, text_color='white')
        legalizador.Legalizador(self.interfas_frame, self.on_of_panel, self.alertas)
        self.screen = 'soporte_frame'

    def portas_frame(self):
        self.button_portas.configure(fg_color=self.colors.team, text_color='white')
        portas.Portas(self.interfas_frame, self.on_of_panel, self.alertas)
        self.screen = 'auditoria_frame'

    def consulta_seriales_frame(self):
        self.button_seriales.configure(fg_color=self.colors.team, text_color='white')
        consulta_seriales.Consulta_seriales(self.interfas_frame, self.on_of_panel)
        self.screen = 'consulta_seriales_frame'

    def legalizador_sims_frame(self):
        self.button_legalizador_sims.configure(fg_color=self.colors.team, text_color='white')
        legalizador_simcard.Legalizador_sims(self.interfas_frame, self.on_of_panel)
        self.screen = 'consulta_seriales_frame'

    def recargas_frame(self):
        self.button_recargas.configure(fg_color=self.colors.team, text_color='white')
        # recargas.Recargas(self.interfas_frame, self.on_of_panel)
        recargas.Recargas(self.interfas_frame, self.on_of_panel)
        self.screen = 'consulta_seriales_frame'

    def consulta_seriales2_frame(self):
        self.button_consulta_seriales.configure(fg_color=self.colors.team, text_color='white')
        consulta_seriales2.Consulta_seriales(self.interfas_frame, self.on_of_panel)
        self.screen = 'consulta_seriales_frame'

    def volantes_frame(self):
        self.button_volantes.configure(fg_color=self.colors.team, text_color='white')
        volantes.Volantes(self.interfas_frame, self.on_of_panel)
        self.screen = 'consulta_seriales_frame'

    # def comercial_frame(self):
    #     self.button_comercial.configure(fg_color=self.colors.team, text_color='white')
    #     comercial.Comercial(self.interfas_frame)
    #     self.screen = 'comercial_frame'
    
    def change_theme(self):
        if self.theme == 'dark':
            self.theme = 'light'
            self.texto_theme = 'Modo Dia'
            ctk.set_appearance_mode(self.theme)
        else:
            self.theme = 'dark'
            self.texto_theme = 'Modo Noche'
            ctk.set_appearance_mode(self.theme)

        for frame in self.menu_frame.winfo_children():
            frame.destroy()
        self.menu()
        for frame in self.interfas_frame.winfo_children():
            frame.destroy()
        if self.screen != '':
            screen = getattr(self,f'{self.screen}')
            screen()

    def start(self):
        self.root.mainloop()
    
    def ventana_superior(self, image, func1, func2):
        subventana = ctk.CTkToplevel()
        # subventana.overrideredirect(True)
        imagen = Image.open(image)
        # imagen = imagen.resize((300, 300))
        imagen_tk = ImageTk.PhotoImage(imagen)
        etiqueta_imagen = ctk.CTkLabel(subventana, image=imagen_tk, text='')
        etiqueta_imagen.pack()
        ctk.CTkLabel(subventana, text='').pack()
        boton1 = self.button.create_button(subventana, "Pantallazo", 0, 0, 0, 0, func1, pack=True, teamColor=True)
        ctk.CTkLabel(subventana, text='').pack()
        boton2 = self.button.create_button(subventana, "Continuar", 0, 0, 0, 0, func2, pack=True, teamColor=True)
        ctk.CTkLabel(subventana, text='').pack()
        return subventana
        

