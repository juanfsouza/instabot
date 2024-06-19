import os
from ssl import Options
import sys
import traceback
from turtle import window_height, window_width
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from undetected_chromedriver import ChromeOptions
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
import undetected_chromedriver as uc
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from random import uniform, choice, randint
from string import ascii_letters
from fake_useragent import UserAgent
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from nordvpn_switcher import initialize_VPN, rotate_VPN
from selenium_stealth import stealth
from selenium.webdriver.common.action_chains import ActionChains
from seleniumbase import BaseCase

from asyncio import wait
import pygetwindow as gw
from pydub import AudioSegment
import pandas as pd
import pyperclip
import random
import pyautogui
from time import sleep, time


def usleep(a, b):
    sleep(uniform(a, b))

# Função para verificar se a janela do navegador está em primeiro plano
def is_browser_window_focused(browser_title="Chrome"):
    active_window = gw.getWindowsWithTitle(browser_title)
    if active_window:
        return active_window[0].isActive
    return False

# Função para gerar uma resolução de tela aleatória
def generate_random_screen_resolution():
    resolutions = [
        "1920x1080", "1280x720", "2560x1440", "1680x1050", "1440x900", "1600x900"
    ]
    return choice(resolutions)

# Função para obter as dimensões da janela do navegador
def get_browser_window_size(driver):
    window_size = driver.execute_script("return [window.outerWidth - window.innerWidth + arguments[0], "
                                        "window.outerHeight - window.innerHeight + arguments[1]];", 0, 0)
    return window_size


                    # Função para selecionar uma pasta aleatória dentro do diretório de fotos
def select_random_folder(directory):
    folders = [folder for folder in os.listdir(directory) if os.path.isdir(os.path.join(directory, folder))]
    return os.path.join(directory, random.choice(folders)) if folders else None

def select_random_photo(folder):
    photos = [photo for photo in os.listdir(folder) if os.path.isfile(os.path.join(folder, photo))]
    return os.path.join(folder, random.choice(photos)) if photos else None
            

def copiar_primeiras_linhas_e_apagar_arquivo(origem, destino, num_linhas=2):
    try:
        # Abrir o arquivo de origem para leitura
        with open(origem, 'r') as arquivo_origem:
            # Ler todas as linhas do arquivo
            linhas = arquivo_origem.readlines()
        
        # Verificar se há linhas suficientes para copiar
        if len(linhas) < num_linhas:
            print(f"Nao existe contas em {origem}")
            return
        
        # As primeiras linhas que serão copiadas
        primeiras_linhas = linhas[:num_linhas]
        
        # Escrever as primeiras linhas no arquivo de destino
        with open(destino, 'a') as arquivo_destino:
            arquivo_destino.writelines(primeiras_linhas)
        
        # As linhas restantes que serão mantidas no arquivo de origem
        linhas_restantes = linhas[num_linhas:]
        
        # Escrever as linhas restantes de volta no arquivo de origem
        with open(origem, 'w') as arquivo_origem:
            arquivo_origem.writelines(linhas_restantes)
        
        print(f"A conta {num_linhas} foi copiada {origem} para {destino} e removidas do arquivo original.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar copiar e colocar a conta: {e}")

def copiar_primeiras_linhas_e_apagar_arquivo_(origem, destino, num_linhas=2):
    try:
        # Abrir o arquivo de origem para leitura
        with open(origem, 'r') as arquivo_origem:
            # Ler todas as linhas do arquivo
            linhas = arquivo_origem.readlines()
        
        # Verificar se há linhas suficientes para copiar
        if len(linhas) < num_linhas:
            print(f"Nao existe contas em {origem}")
            return
        
        # As primeiras linhas que serão copiadas
        primeiras_linhas = linhas[:num_linhas]
        
        # Escrever as primeiras linhas no arquivo de destino
        with open(destino, 'a') as arquivo_destino:
            arquivo_destino.writelines(primeiras_linhas)
        
        # As linhas restantes que serão mantidas no arquivo de origem
        linhas_restantes = linhas[num_linhas:]
        
        # Escrever as linhas restantes de volta no arquivo de origem
        with open(origem, 'w') as arquivo_origem:
            arquivo_origem.writelines(linhas_restantes)
        
        print(f"A conta {num_linhas} foi copiada {origem} para {destino} e removidas do arquivo original.")
    except Exception as e:
        print(f"Ocorreu um erro ao tentar copiar e colocar a conta: {e}")


if __name__ == "__main__":
    while True:  # Start an infinite loop
        try:
            # Configurando opções para o Chrome
            chrome_opt = uc.ChromeOptions()                       
            options = uc.ChromeOptions()

            # Definir a resolução de tela aleatória
            random_resolution = generate_random_screen_resolution()
            print("Screen Resolution:", random_resolution)
            chrome_opt.add_argument(f"--window-size={random_resolution}")
            chrome_opt.add_argument(f'user-agent={UserAgent}')
            chrome_opt.add_argument("--window-size=1920,1080")
            chrome_opt.add_argument('--ignore-certificate-errors')
            chrome_opt.add_argument('--allow-running-insecure-content')
            #chrome_opt.add_argument("--disable-extensions")
            chrome_opt.add_argument("--proxy-server='direct://'")
            chrome_opt.add_argument("--proxy-bypass-list=*")
            chrome_opt.add_argument("--start-maximized")
            #chrome_opt.add_argument('--disable-gpu')
            #chrome_opt.add_argument('--disable-dev-shm-usage')
            chrome_opt.add_argument("--no-sandbox")
            #chrome_opt.add_argument("--disable-webrtc")  # Desativa o WebRTC
            #chrome_opt.add_argument("--disable-notifications")  # Desabilitar notificações
            chrome_opt.add_argument("--disable-infobars")  # Desabilitar infobars
            #chrome_opt.add_argument("--incognito")  

            # Desabilitar o gerenciador de senhas
            prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
            chrome_opt.add_experimental_option("prefs", prefs)

            # Adding argument to disable the AutomationControlled flag 
            chrome_opt.add_argument("--disable-blink-features=AutomationControlled")      
            # Exclude the collection of enable-automation switches 
            #chrome_opt.add_experimental_option("excludeSwitches", ["enable-automation"])     
            #options.add_argument('--disable-dev-shm-usage')
            #chrome_opt.add_argument('--load-extension=C:/Users/juan/Desktop/Appinsta/ext.crx')
            #chrome_opt.add_argument('--headless')
            #chrome_opt.add_argument("--disable-javascript")
            chrome_opt.add_argument('referer=https://www.instagram.com/')
            chrome_opt.add_argument('accept-language=pt=BR,pt;q=0.9')
            chrome_opt.add_argument('--disable-features=WebRtcHideLocalIpsWithMdns')
            # Limpar o conteúdo do arquivo de log
            with open("app_log.txt", "w") as log_file:
                log_file.write("")

            sys.stdout.reconfigure(line_buffering=True)
            sys.stdout.reconfigure(encoding='utf-8')

            # Inicializar o navegador Chrome
            driver = uc.Chrome(options=chrome_opt)

            class BaseTestCase(BaseCase):
                def setUp(self):
                    super().setUp()
                    stealth(self.driver)

                # Defina listas de opções para cada configuração do Selenium Stealth
                languages_options = [["pt-BR", "pt"]]
                platform_options = ["Win32", "Win64"]
                webgl_vendor_options = ["Google Inc. (Intel)", "Google Inc. (AMD)", "Google Inc. (NVIDIA)"]
                intel_renderer_options = ["Intel Iris OpenGL Engine"]
                nvidia_renderer_options = [
                    "ANGLE (NVIDIA, NVIDIA GeForce GTX 750 Ti Direct3D9Ex vs_3_0 ps_3_0, nvd3dumx.dll-22.21.13.8541)",
                    "ANGLE (NVIDIA, NVIDIA GeForce 210 Direct3D11 vs_4_1 ps_4_1, D3D11)",
                    "ANGLE (NVIDIA, NVIDIA Quadro P620 Direct3D11 vs_5_0 ps_5_0, D3D11)",
                    "ANGLE (NVIDIA, NVIDIA GeForce 8400GS Direct3D11 vs_4_1 ps_4_1, D3D11-9.18.13.4174)",
                    "ANGLE (NVIDIA, NVIDIA GeForce GTX 1050 Ti Direct3D11 vs_5_0 ps_5_0, D3D11-27.21.14.6627)",
                    "ANGLE (NVIDIA, NVIDIA GeForce GT 730 Direct3D11 vs_5_0 ps_5_0, D3D11-23.21.13.9135)",
                    "ANGLE (NVIDIA, NVIDIA GeForce GT 1030 Direct3D11 vs_5_0 ps_5_0, D3D11-23.21.13.8813)",
                ]
                amd_renderer_options = [
                    "ANGLE (AMD, AMD Radeon Series Direct3D11 vs_5_0 ps_5_0, D3D11-25.20.15003.5010)",
                    "ANGLE (AMD, AMD 760G (Microsoft Corporation WDDM 1.1) Direct3D9Ex vs_3_0 ps_3_0, D3D9Ex)",
                    "ANGLE (AMD, AMD Radeon(TM) R7 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-23.20.15002.11)",
                    "ANGLE (AMD, AMD Radeon(TM) Vega 8 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.1032.2)",
                    "ANGLE (AMD, AMD Radeon(TM) RX Vega 11 Graphics Direct3D11 vs_5_0 ps_5_0, D3D11)",
                    "ANGLE (AMD, AMD Radeon(TM) Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.1022.2001)",
                ]
                intel_renderer_options = [
                    "ANGLE (Intel, Intel(R) HD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.100.7925)",
                    "ANGLE (Intel, Intel(R) HD Graphics 520 Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.7988)",
                    "ANGLE (Intel, Intel(R) HD Graphics Family Direct3D9Ex vs_3_0 ps_3_0, aticfx32.dll-8.17.10.1119)",
                    "ANGLE (Intel, Intel(R) HD Graphics 530 Direct3D11 vs_5_0 ps_5_0, D3D11-21.20.16.4860)",
                    "ANGLE (Intel, Intel(R) UHD Graphics 620 Direct3D11 vs_5_0 ps_5_0, D3D11-26.20.100.7261)",
                    "ANGLE (Intel, Intel(R) HD Graphics 3000 Direct3D11 vs_4_1 ps_4_1, D3D11-21.21.13.7748)",
                    "ANGLE (Intel, Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0, D3D11-20.19.15.5171)",
                    "ANGLE (Intel, Intel(R) UHD Graphics 630 Direct3D11 vs_5_0 ps_5_0, D3D11-23.20.16.4982)",
                    "ANGLE (Intel, Intel(R) HD Graphics 4400 Direct3D11 vs_5_0 ps_5_0, D3D11-10.18.14.4578)",
                    "ANGLE (Intel, Intel(R) UHD Graphics Direct3D11 vs_5_0 ps_5_0, D3D11-27.20.100.8935)",
                ]

                # Escolha aleatoriamente uma opção para cada configuração
                random_languages = random.choice(languages_options)
                random_platform = random.choice(platform_options)
                random_webgl_vendor = random.choice(webgl_vendor_options)

                # Inicialize o renderizador como uma string vazia
                random_renderer = ""

                # Se o WebGL gerado for da NVIDIA, configure o fornecedor como "NVIDIA Corporation"
                if random_webgl_vendor == "Google Inc. (NVIDIA)":
                    random_vendor = "Google Inc. (NVIDIA)"
                    random_renderer = random.choice(nvidia_renderer_options)
                # Se o WebGL gerado for da ATI (AMD), configure o fornecedor como "ATI Technologies Inc."
                elif random_webgl_vendor == "Google Inc. (AMD)":
                    random_vendor = "Google Inc. (AMD)"
                    random_renderer = random.choice(amd_renderer_options)
                # Caso contrário, escolha aleatoriamente entre outros fornecedores
                else: 
                    random_webgl_vendor == "Google Inc. (Intel)"
                    random_vendor = "Google Inc. (Intel)"
                    random_renderer = random.choice(intel_renderer_options)

                # Inicialize o navegador com as opções aleatórias
                stealth(driver,
                    languages=random_languages,
                    vendor=random_vendor,
                    platform=random_platform,
                    webgl_vendor=random_webgl_vendor,
                    renderer=random_renderer,
                    fix_hairline=True,  # Esta configuração não precisa de valores aleatórios
                )


            # Initializing a list with two Useragents 
            useragentarray = [ 
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.78 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.87 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.61 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.86 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.111 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.95 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.112 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.128 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.59 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.58 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.123 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.123 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.69 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.61 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.69 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.87 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.59 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.156 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.156 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.123 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.201 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.59 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/125.0.6422.76 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.59 Safari/537.36",
                "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.207 Safari/537.36",
            ]   

            for i in range(len(useragentarray)): 
                # Setting user agent iteratively as Chrome 108 and 107 
                driver.execute_cdp_cmd("Network.setUserAgentOverride", {"userAgent": useragentarray[i]}) 
                driver.get("https://www.httpbin.org/headers")

            # Obter as coordenadas da janela do navegador após a inicialização do driver
            browser_window = driver.get_window_rect()
            browser_x, browser_y = browser_window['x'], browser_window['y']
            browser_width, browser_height = browser_window['width'], browser_window['height']

            # Definir a região de interesse para as ações do PyAutoGUI com base nas coordenadas da janela do navegador
            pyautogui.PAUSE = 0.5  # Atraso entre as operações (opcional)
            pyautogui.FAILSAFE = True  # Ativar o modo de segurança para parar as operações quando o cursor atingir o canto superior esquerdo

            # Definir a região de interesse
            region = (browser_x, browser_y, browser_width, browser_height)
            pyautogui.FAILSAFE = False  # Desativar o modo de segurança para permitir movimentos fora da região de interesse 

            # Defina o tamanho desejado para a janela do navegador
            new_width = 1500  # Coloque o valor desejado para a largura da janela
            new_height = 1700  # Coloque o valor desejado para a altura da janela

            # Redimensione a janela do navegador
            driver.set_window_size(new_width, new_height)

            # Obtenha as dimensões da janela do navegador
            window_width, window_height = get_browser_window_size(driver)

            # Exemplo de como limitar as ações do PyAutoGUI às dimensões da janela
            pyautogui.moveTo(window_width // 2, window_height // 2)  # Movimenta o cursor para o centro da janela do navegador

            driver.get('https://instagram.com/')
            usleep(3, 5)

            ### Atualize a página ###
            # driver.refresh()

            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))

            # Clique no elemento para focar
            element.click()

            # Ler a primeira linha do arquivo accounts.txt
            def ler_primeira_linha():
                with open('logs/accounts.txt', 'r') as file:
                    primeira_linha = file.readline().strip()  # Lê a primeira linha e remove espaços em branco
                return primeira_linha

            # Obtenha o texto da primeira linha
            primeira_linha = ler_primeira_linha()
            print("Primeira linha:", primeira_linha)

            # Simule a digitação letra por letra usando ActionChains
            actions = ActionChains(driver)
            for letra in primeira_linha:
                actions.send_keys(letra)
                actions.pause(random.uniform(0.1, 0.5))  # Pausa de 0.2 segundos entre cada letra
            actions.perform()
            usleep(3, 5)
            
            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))

            # Clique no elemento para focar
            element.click()

            # Função para ler a segunda linha do arquivo accounts.txt
            def ler_segunda_linha():
                with open('logs/accounts.txt', 'r') as file:
                    segunda_linha = file.readline().strip()  # Lê a segunda linha e remove espaços em branco
                    segunda_linha = file.readline().strip()  # Lê a segunda linha novamente para obter a próxima linha
                return segunda_linha
            
                        # Ler a segunda linha do arquivo accounts.txt
            segunda_linha = ler_segunda_linha()
            print("Segunda linha:", segunda_linha)

                        # Simule a digitação letra por letra usando ActionChains
            actions = ActionChains(driver)
            for letra in segunda_linha:
                actions.send_keys(letra)
                actions.pause(random.uniform(0.1, 0.5))  # Pausa de 0.2 segundos entre cada letra
            actions.perform()
            usleep(3, 5)

            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Entrar')]")))

            # Clique no elemento para focar
            element.click()
            usleep(3, 5)

            # Diretório onde as fotos estão localizadas
            photos_directory = r"C:\Users\juan\Desktop\foto\Nova pasta"

            # Variável para controlar o número de repetições
            count = 0
            num = 0
            
            while count <= 8:
                # Repetir o processo de seleção de pasta e foto aleatória sete vezes
                for _ in range(7):
                    # Crie uma instância de WebDriverWait
                    wait = WebDriverWait(driver, 20)

                    # Aguarde até que o elemento do campo de usuário seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Criar')]")))

                    # Clique no elemento para focar
                    element.click()
                    usleep(3, 5)

                    # Crie uma instância de WebDriverWait
                    wait = WebDriverWait(driver, 20)

                    # Aguarde até que o elemento do campo de usuário seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Selecionar do computador')]")))

                    # Clique no elemento para focar
                    element.click()
                    usleep(5, 10)                
                    
                    while num < 1:
                        folder_path = select_random_folder(photos_directory)
                        if folder_path:
                            pyautogui.typewrite(folder_path)
                            pyautogui.press("enter")
                            # Aguarde um curto período para a pasta ser aberta
                            usleep(1, 5)
                        else:
                            print("Não foi possível encontrar pastas de fotos no diretório especificado.")
                        
                        num += 1

                    photo_path = select_random_photo(folder_path)
                    if photo_path:
                        pyautogui.typewrite(photo_path)
                        usleep(5, 5)
                        pyautogui.press("enter")
                    else:
                        print("Não foi possível encontrar pastas de fotos no diretório especificado.")    

                    # Crie uma instância de WebDriverWait
                    wait = WebDriverWait(driver, 20)

                    # Aguarde até que o elemento do campo de usuário seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Avançar')]")))

                    # Clique no elemento para focar
                    element.click()

                    usleep(3, 5)

                    # Aguarde até que o elemento do campo de usuário seja clicável novamente
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Avançar')]")))

                    # Clique no elemento para focar
                    element.click()

                    usleep(3, 5)

                    # Aguarde até que o elemento do campo de 'Compartilhar' seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Compartilhar')]")))

                    # Clique no elemento para focar
                    element.click()
                    usleep(3, 5)

                    pyautogui.press("f5")

                    count += 1
                ############################### END #######################################   

                # Crie uma instância de WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Aguarde até que o elemento do campo de usuário seja clicável
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Perfil')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5)

                # Crie uma instância de WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Aguarde até que o elemento do campo de usuário seja clicável
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Editar perfil')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5)

                pyautogui.press("f5")

                # Crie uma instância de WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Aguarde até que o elemento do campo de usuário seja clicável
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Alterar foto')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5)
                
                photo_path = select_random_photo(folder_path)
                if photo_path:
                    pyautogui.typewrite(photo_path)
                    usleep(5, 5)
                    pyautogui.press("enter")
                else:
                    print("Não foi possível encontrar pastas de fotos no diretório especificado.")

                # Caminho para a pasta onde os arquivos de texto estão localizados
                folder_path = r'C:\Users\juan\Desktop\Appinsta\bios'

                # Função para selecionar um arquivo de texto aleatório e ler seu conteúdo
                def get_random_file_content(folder_path):
                    files = [f for f in os.listdir(folder_path) if f.endswith('.txt')]
                    if not files:
                        raise FileNotFoundError("No .txt files found in the directory.")
                    random_file = random.choice(files)
                    with open(os.path.join(folder_path, random_file), 'r', encoding='utf-8') as file:
                        content = file.read()
                    return content
                
                # Obter o conteúdo de um arquivo de texto aleatório
                file_content = get_random_file_content(folder_path)

                # Copiar o conteúdo para a área de transferência
                pyperclip.copy(file_content)

                pyautogui.press("tab")
                usleep(3, 5)
                pyautogui.hotkey('ctrl', 'v')

                # Crie uma instância de WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Aguarde até que o elemento do campo de usuário seja clicável
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Prefiro não informar')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5)

                # Crie uma instância de WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Aguarde até que o elemento do campo de usuário seja clicável
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//span[contains(text(), 'Feminino')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5)

                # Crie uma instância de WebDriverWait
                wait = WebDriverWait(driver, 20)

                # Aguarde até que o elemento do campo de usuário seja clicável
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Enviar')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5)

                
                # Caminhos dos arquivos
                origem = 'logs/accounts.txt'
                destino_ = 'C:\\Users\\juan\\Desktop\\Appinsta\\montados\\contas.txt'

                # Executa a função
                copiar_primeiras_linhas_e_apagar_arquivo(origem, destino_)
                usleep(3, 5)
                print("Restarting the bot...")
                
                if driver:
                    log_file.quit()
                    driver.quit()

        except Exception as e:
            # Caminhos dos arquivos
            origem = 'logs/accounts.txt'
            destino = 'C:\\Users\\juan\\Desktop\\Appinsta\\descartaveis\\descartaveis.txt'

            # Executa a função
            copiar_primeiras_linhas_e_apagar_arquivo(origem, destino)
            usleep(3, 5)
            print("Restarting the bot...")

            # Reinicie o loop
            continue
        finally:
            if driver:
                driver.quit()  # Ensure the driver is always closed
               