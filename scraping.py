from bs4 import BeautifulSoup



class Scraping:

    def __init__(self,html):
        self.soup = BeautifulSoup(html, 'html.parser')

    def extrarDataTablas(self):
        tabla = self.soup.find('table')

        if tabla:
            filas = tabla.find_all('tr')
            datos_tabla = []
            for fila in filas:
                celdas = fila.find_all('td')
                datos_fila=[]
                for celda in celdas:
                    datos_fila.append(celda.get_text())
                datos_tabla.append(datos_fila)
        return datos_tabla