from selenium.webdriver.chrome.service import Service as ChromeService
import chromedriver_autoinstaller
from selenium import webdriver
from tkinter import *
import time
import requests
import urllib.request
import os
import zipfile
from io import BytesIO
from msedge.selenium_tools import Edge, EdgeOptions
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
import random


class Web_Controller:

    def __init__(self, sleeptime):
        global sleep
        sleep = sleeptime
        global aleatorio
        aleatorio = False
        # self.edgedriver()
        # self.openEdge()
    
    def actualizarIntervalo(self, valor, aleatorio_value=False):
        global sleep
        sleep = valor
        global aleatorio
        aleatorio = aleatorio_value

    def script(self, str):
        self.browser.execute_script(str)
    
    def retornarHtml(self):
        return self.browser.page_source

    def chromedriver(self):
        chromedriver_autoinstaller.install()
    
    def edgedriver(self):
        # Obtener la última versión del controlador de Microsoft Edge WebDriver
        response = requests.get('https://msedgewebdriverstorage.blob.core.windows.net/edgewebdriver/LATEST_STABLE')
        latest_version = response.text.strip()
        print(latest_version)
        # latest_version = '119.0.2151.44'
        # print(latest_version)


        # URL de descarga del controlador
        url = f'https://msedgedriver.azureedge.net/{latest_version}/edgedriver_win64.zip'

        # Descargar y extraer el archivo zip del controlador
        response = urllib.request.urlopen(url)
        zipfile.ZipFile(BytesIO(response.read())).extractall(os.getcwd())

        # Agregar el controlador al PATH del sistema
        os.environ['PATH'] += os.pathsep + os.getcwd()
    

    
    def validate(funcion):
        def execute(self,*args, **kwargs):
            proof = True
            contador = 1
            while proof:
                try:
                    data = funcion(self,*args, **kwargs)
                    proof= False
                    if aleatorio:
                        randomTime = round(random.uniform(-0.15,1.15),2)
                    else:
                        randomTime = 0
                    time.sleep(int(float(sleep) + randomTime))
                    return data
                except Exception as err:
                    if contador < 8:
                        print(f'intento numero {contador} {err}')
                        time.sleep(1)
                        contador +=1
                    else:
                        raise('Excedio el numero de intentos')
        return execute
    
    def validateShort(funcion):
        def execute(self,*args, **kwargs):
            proof = True
            contador = 1
            while proof:
                try:
                    data = funcion(self,*args, **kwargs)
                    proof= False
                    time.sleep(int(sleep))
                    return data
                except:
                    if contador < 5:
                        print(f'intento numero {contador}')
                        time.sleep(1)
                        contador +=1
                    else:
                        raise('Excedio el numero de intentos')
        return execute
    
    def validateShort2(funcion):
        def execute(self,*args, **kwargs):
            proof = True
            contador = 1
            while proof:
                try:
                    data = funcion(self,*args, **kwargs)
                    proof= False
                    time.sleep(int(sleep))
                    return data
                except:
                    if contador < 3:
                        print(f'intento numero {contador}')
                        time.sleep(1)
                        contador +=1
                    else:
                        raise('Excedio el numero de intentos')
        return execute
    
    def openEdgeModeExplorer(self):
        options = webdriver.IeOptions()
        # options.file_upload_dialog_timeout = 2000
        # options.set_capability("silent", True)
        # options.add_argument('-private')
        
        driver = webdriver.Ie(options=options)

        # Navegar para Url
        driver.get("http://www.google.com")

        driver.quit()
    
    def openChrome(self):
        service = ChromeService('chromedriver')
        options =  webdriver.ChromeOptions()
        self.browser = webdriver.Chrome(chrome_options= options)
    
    def openEdge(self, headless = False):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("start-maximized")
        if headless:
            options.add_argument("--headless=new")
            options.add_argument('--no-sandbox')
            options.add_argument('--disable-dev-shm-usage')
        self.browser = Edge(executable_path='msedgedriver.exe', options=options)
        self.browserOriginal = self.browser

    def openEdgeModeIE(self, headless = False):
        ieOptions = webdriver.IeOptions()
        ieOptions.add_additional_option("ie.edgechromium", True)
        ieOptions.add_additional_option("ie.edgepath",'C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe')
        self.browser = webdriver.Ie(executable_path='IEDriverServer.exe', options=ieOptions)
        self.browserOriginal = self.browser
    
    def crearNavegador(self):
        options = EdgeOptions()
        options.use_chromium = True
        options.add_argument("start-maximized")
        return Edge(executable_path='msedgedriver.exe', options=options)

    @validateShort2
    def listarElemetos(self, byStr, by='xpath', click=None):
        list_data = []
        if by == "xpath": find = self.browser.find_elements_by_xpath(byStr)
        elif by == "id": find = self.browser.find_elements_by_id(byStr)
        elif by == "name": find = self.browser.find_elements_by_name(byStr)
        if find is not None:
            for item in find:
                name = item.text
                if click is not None:
                    if name == click:
                        item.click()
                        break
                list_data.append(name)
        return list_data

    @validate
    def selectPage(self, link):
        self.browser.get(link)

    def getCookies(self):
        cookies = self.browser.get_cookies()
        if cookies:
            cookie_text = '; '.join([f"{cookie['name']}={cookie['value']}" for cookie in cookies])
        return cookie_text
        
    @validate
    def insert(self, byStr, text, by='xpath', enter =False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.send_keys(text)
            if enter:
                find.send_keys(Keys.ENTER)

    @validate
    def select(self, byStr, text, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            selection = Select(find)
            selection.select_by_value(text)
    
    @validate
    def click(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.click()
    
    @validate
    def click_ctr(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find = None
        if find is not None:
            ActionChains(self.browser).key_down(Keys.CONTROL).click(find).key_up(Keys.CONTROL).perform()
    
    def cambiar_pestaña(self):
        self.browser.switch_to.window(self.browser.window_handles[-1])
    
    def volver_pestaña(self):
        self.browser.switch_to.window(self.browser.window_handles[0])
    
    def cerrar_pestaña(self):
        self.browser.close()
    
    @validateShort2
    def leer_txt(self):
        texto_elemento = self.browser.find_element_by_xpath("/html/body/pre")
        return texto_elemento.text

    @validateShort2
    def readShort2(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        elif by == "class": find = self.browser.find_element_by_class_name(byStr)
        if find is not None:
            return find.text
        else: return "none"
    
    @validateShort
    def readShort(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.text
        else: return "none"
    
    @validate
    def read(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        elif by == "class": find = self.browser.find_element_by_class_name(byStr)
        if find is not None:
            return find.text
        else: return "none"

    @validate
    def readMulty(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_elements_by_xpath(byStr)
        elif by == "id": find = self.browser.find_elements_by_id(byStr)
        elif by == "name": find = self.browser.find_elements_by_name(byStr)
        elif by == "class": find = self.browser.find_elements_by_class_name(byStr)
        if find is not None:
            return [i.text for i in find]
        else: return "none"
    
    @validate
    def value(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.get_attribute('value')
        else: return "none"

    def readNoValidate(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            return find.text
        else: return "none"
    
    @validateShort2
    def waitExist2(self, byStr, by='xpath', write=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise('')

    @validateShort
    def waitExist(self, byStr, by='xpath', write=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            if write:
                find.send_keys('')
            pass
        else: raise('')

    @validate
    def wait(self, byStr, condition ,by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            if find.text is not None:
                if condition in find.text:
                    raise('error')
    
    @validate     
    def erase(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.clear()
    
    @validate   
    def eraseLetter(self, byStr, cantidad, by='xpath', move=False):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            for i in range(0,cantidad):
                if move:
                    find.send_keys(Keys.ARROW_RIGHT)
                find.send_keys(Keys.BACKSPACE)

    @validate   
    def write(self, byStr, keys, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        else: find =None
        if find is not None:
            find.send_keys(keys)
    
    def readonly(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            readonly_value = find.get_attribute('readonly')
            if readonly_value == 'readonly':
                return True
            else:
                return False
        else: return None
    
    def selectDown(self, byStr, by='xpath'):
        if by == "xpath": find = self.browser.find_element_by_xpath(byStr)
        elif by == "id": find = self.browser.find_element_by_id(byStr)
        elif by == "name": find = self.browser.find_element_by_name(byStr)
        if find is not None:
            find.send_keys(Keys.ARROW_DOWN)
            find.send_keys(Keys.ENTER)

    
    def browserGet(self):
        return self.browser
    
    def cerrar(self):
        self.browser.close()
        self.browser.quit()

