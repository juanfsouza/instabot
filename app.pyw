from math import prod
import re
import subprocess
import sys
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
from seleniumbase import BaseCase
from selenium.webdriver.common.action_chains import ActionChains
from unidecode import unidecode
from selenium.webdriver.common.proxy import Proxy, ProxyType

from asyncio import wait
import pygetwindow as gw
from pydub import AudioSegment
import pandas as pd
import pyperclip
import random
import pyautogui
from time import sleep, time


# Define a log file
log_file = open("app_log.txt", "a")

# Redirect stdout and stderr to the log file
sys.stdout = log_file
sys.stderr = log_file

def usleep(a, b):
    sleep(uniform(a, b))


# Função para verificar se a janela do navegador está em primeiro plano
def is_browser_window_focused(browser_title="Chrome"):
    active_window = gw.getWindowsWithTitle(browser_title)
    if active_window:
        return active_window[0].isActive
    return False

# Função para gerar um par de coordenadas de localização aleatórias (latitude e longitude)
def generate_random_location():
    latitude = round(randint(-90, 90) + randint(0, 999999) / 1000000, 6)
    longitude = round(randint(-180, 180) + randint(0, 999999) / 1000000, 6)
    return f"{latitude}, {longitude}"

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
# Lista de proxies
proxies = [
    {"ip": "191.242.111.195", "porta": "8080"},
    {"ip": "131.196.42.95", "porta": "667"},
    {"ip": "189.3.69.230", "porta": "8080"},
    {"ip": "200.174.198.236", "porta": "8888"},
    {"ip": "45.238.118.156", "porta": "27234"},
    {"ip": "187.44.211.118", "porta": "4153"},
    {"ip": "187.19.200.217", "porta": "8090"},
    {"ip": "170.244.0.179", "porta": "4145"},
    {"ip": "179.189.219.98", "porta": "4145"},
    {"ip": "187.95.80.141", "porta": "3629"},
    # Adicione mais proxies conforme necessário
]

# Selecionar um proxy aleatório
proxy_info = random.choice(proxies)
proxy_ip = proxy_info["ip"]
proxy_porta = proxy_info["porta"]

# Configuração do Proxy
proxy = Proxy()
proxy.proxy_type = ProxyType.MANUAL
proxy.http_proxy = f"{proxy_ip}:{proxy_porta}"
proxy.ssl_proxy = f"{proxy_ip}:{proxy_porta}"


if __name__ == "__main__":
    while True:  # Start an infinite loop
        # Configurando opções para o Chrome
        chrome_opt = uc.ChromeOptions()
                        
        options = uc.ChromeOptions()
        #options.add_argument("--headless")
        #chrome_opt.add_argument("--incognito")  

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
        chrome_opt.add_argument('--disable-dev-shm-usage')
        chrome_opt.add_argument("--no-sandbox")
        #chrome_opt.add_argument("--disable-webrtc")  # Desativa o WebRTC
        #chrome_opt.add_argument("--disable-notifications")  # Desabilitar notificações
        #chrome_opt.add_argument("--disable-infobars")  # Desabilitar infobars

        # Desabilitar o gerenciador de senhas
        prefs = {"credentials_enable_service": False, "profile.password_manager_enabled": False}
        chrome_opt.add_experimental_option("prefs", prefs)

        # Adding argument to disable the AutomationControlled flag 
        options.add_argument("--disable-blink-features=AutomationControlled")      
        # Exclude the collection of enable-automation switches 
        options.add_experimental_option("excludeSwitches", ["enable-automation"])     
        options.add_argument('--disable-dev-shm-usage')
        options.add_argument('--disable-blink-features=AutomationControlled')
        #options.add_experimental_option('useAutomationExtension', True)
        #chrome_opt.add_argument('--load-extension=C:/Users/juan/Desktop/Appinsta/ext.crx')

        # Adicionar configuração do proxy ao ChromeOptions
        chrome_opt.add_argument(f"--proxy-server=http://{proxy_ip}:{proxy_porta}")
        
        try:
            # Limpar o conteúdo do arquivo de log
            with open("app_log.txt", "w") as log_file:
                log_file.write("")

            sys.stdout.reconfigure(line_buffering=True)
            sys.stdout.reconfigure(encoding='utf-8')

            # [1] save settings file as a variable

            instructions = initialize_VPN(area_input=['Brazil']) # <-- Be aware: the area_input parameter expects a list, not a string

            rotate_VPN(instructions) #refer to the instructions variable here
            print('\n Rotacao de IPS BR Gerados Com Sucesso!\n')
            sleep(15)

            # Inicializar o navegador Chrome
            driver = uc.Chrome(options=chrome_opt)
            print('\nIniciando Bot\n')

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
            new_width = 700  # Coloque o valor desejado para a largura da janela
            new_height = 850  # Coloque o valor desejado para a altura da janela

            # Redimensione a janela do navegador
            driver.set_window_size(new_width, new_height)

            # Obtenha as dimensões da janela do navegador
            window_width, window_height = get_browser_window_size(driver)

            # Exemplo de como limitar as ações do PyAutoGUI às dimensões da janela
            pyautogui.moveTo(window_width // 2, window_height // 2)  # Movimenta o cursor para o centro da janela do navegador
           
            ################## CLOUD VPN #############################


            def conectar_warp():
                # Comando para conectar ao Cloudflare Warp
                comando_conectar = "warp-cli.exe connect"

                try:
                    # Conecta ao Cloudflare Warp
                    subprocess.run(comando_conectar, shell=True, check=True)
                    print("Conectado ao Cloudflare Warp com sucesso!")
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao conectar ao Cloudflare Warp: {e}")
                    # Se houver erro, é importante lidar com isso aqui

        
            def desconectar_warp():
                # Comando para desconectar do Cloudflare Warp
                comando_desconectar = "warp-cli.exe disconnect"

                try:
                    # Desconecta do Cloudflare Warp
                    subprocess.run(comando_desconectar, shell=True, check=True)
                    print("Desconectado do Cloudflare Warp com sucesso!")
                except subprocess.CalledProcessError as e:
                    print(f"Erro ao desconectar do Cloudflare Warp: {e}")
                    # Se houver erro, é importante lidar com isso aqui


            ################## CLOUD VPN ########################

            # CONECTAR VPN
            #conectar_warp()
            #usleep(3, 5)

            driver.get('https://chromewebstore.google.com/detail/nopecha-captcha-solver/dknlfmjaanfblgfdfebhijalfmhmjjjo')
            usleep(3, 5)

            copy_email = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/main/div/section[1]/section/div[2]/div/button')
            copy_email.click()
            usleep(1, 1)

            usleep(1, 1)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')

            usleep(5, 5)
            pyautogui.hotkey('f10')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            usleep(1, 1)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            usleep(1, 1)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            usleep(1, 1)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            
            usleep(1, 1)
            # Abre o arquivo github.txt
            with open("github.txt", "r") as file:
                # Lê a primeira linha do arquivo
                primeira_linha = file.readline().strip()
                
            pyperclip.copy(primeira_linha)

            pyautogui.hotkey('ctrl', 'v')
            usleep(1, 2)

            driver.get('https://mohmal.com/pt/inbox')
            usleep(3, 3)

            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='email']/div[1]")))

            # Clique no elemento para focar
            element.click()
            usleep(1, 3)
            

            pyautogui.hotkey('f10')
            pyautogui.hotkey('f10')

            # Abre uma nova aba
            driver.execute_script("window.open('https://www.instagram.com/accounts/emailsignup/','_blank');")
            usleep(2, 3)

            # Obter todas as alças de aba
            handles = driver.window_handles
            # Mudar o foco para a nova aba
            driver.switch_to.window(handles[1])
            
            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='emailOrPhone']")))

            # Clique no elemento para focar
            element.click()
            usleep(1, 3)

            pyautogui.hotkey('ctrl', 'v')

            print("\nEmail Digitado!\n")
            
            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='fullName']")))

            # Clique no elemento para focar
            element.click()
            usleep(1, 3)

            # Função para ler uma linha aleatória do arquivo de texto e retornar
            def ler_linha_aleatoria(nome_arquivo):
                with open(nome_arquivo, 'r', encoding='utf-8') as arquivo:
                    linhas = arquivo.readlines()
                    linha_aleatoria = random.choice(linhas)
                    return linha_aleatoria.strip()  # Remove espaços em branco e quebras de linha

            # Função para colar o texto da área de transferência
            def colar_texto(texto):
                pyperclip.copy(texto)  # Copia o texto para a área de transferência

            # Arquivo de texto que será lido
            nome_arquivo = 'C:\\Users\\juan\\Desktop\\Appinsta\\list\\names.txt'

            # Lê uma linha aleatória do arquivo de texto
            linha_aleatoria = ler_linha_aleatoria(nome_arquivo)

            # Simule a digitação letra por letra usando ActionChains
            actions = ActionChains(driver)
            for letra in linha_aleatoria:
                actions.send_keys(letra)
                actions.pause(random.uniform(0.0, 0.3))  # Pausa de 0.2 segundos entre cada letra
            actions.perform()
            usleep(1, 3)

                        # Cola o texto da linha aleatória onde necessário
            colar_texto(linha_aleatoria)

            print("\nNome Gerado com sucesso!\n")

           # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='username']")))

            # Clique no elemento para focar
            element.click()

            # Get only the first name from clipboard and remove accents
            clipboard_content = pyperclip.paste()
            first_name = clipboard_content.split()[0]
            first_name = unidecode(first_name)

            # Generate 7 random lowercase letters
            random_letters = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(7))

            # Concatenate the first name and random letters
            generated_name = first_name + random_letters

                # Simule a digitação letra por letra usando ActionChains
            actions = ActionChains(driver)
            for letra in generated_name:
                actions.send_keys(letra)
                actions.pause(random.uniform(0.0, 0.3))  # Pausa de 0.2 segundos entre cada letra
            actions.perform()
            usleep(1, 3)

            print("\nUsername Gerado com sucesso!\n")

            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//input[@name='password']")))

            # Clique no elemento para focar
            element.click()
            usleep(1, 3)

            # Generate 3 random letters
            random_letters = ''.join(random.choice('abcdefghijklmnopqrstuvwxyz') for _ in range(3))
            usleep(1, 3)

            # Generate 7 random digits
            random_digits = ''.join(random.choice('0123456789') for _ in range(7))

            # Concatenate the first senha, random letters, and random digits
            generated_pass = first_name + random_letters + random_digits

                # Simule a digitação letra por letra usando ActionChains
            actions = ActionChains(driver)
            for letra in generated_pass:
                actions.send_keys(letra)
                actions.pause(random.uniform(0.0, 0.3))  # Pausa de 0.2 segundos entre cada letra
            actions.perform()
            usleep(1, 3)


            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Cadastre-se')]")))

            # Clique no elemento para focar
            element.click()
            usleep(1, 3)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            # Pressionar a seta para cima ou para baixo um número aleatório de vezes entre 0 e 10
            num_presses = random.randint(0, 4)
            for _ in range(num_presses):
                usleep(0, 0.2)
                if random.choice([True, False]):
                    pyautogui.press('up')
                else:
                    pyautogui.press('down')

            usleep(1, 2)
            pyautogui.hotkey('tab')

            # Pressionar a seta para cima ou para baixo um número aleatório de vezes entre 0 e 10
            num_presses = random.randint(0, 4)
            for _ in range(num_presses):
                usleep(0, 0.2)
                if random.choice([True, False]):
                    pyautogui.press('up')
                else:
                    pyautogui.press('down')

            usleep(1, 2)
            pyautogui.hotkey('tab')
            
            # Pressionar a seta para cima ou para baixo um número aleatório de vezes entre 0 e 10
            num_presses = random.randint(18, 25)
            for _ in range(num_presses):
                usleep(0, 0.1)
                pyautogui.press('down')
            
            # Crie uma instância de WebDriverWait
            wait = WebDriverWait(driver, 20)

            # Aguarde até que o elemento do campo de usuário seja clicável
            element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Avançar')]")))

            # Clique no elemento para focar
            element.click()
            usleep(2, 3)

            print("\nVerificando se tem captcha!\n")
            usleep(1, 3)

            print("\nTem Captcher!\n")
            print("\nResolvendo Captcha!\n")

            ############## CAPTCHA ########################

            print("\nCaptcha Resolvido!\n")

            # Defina o número máximo de tentativas
            max_ = 6
            tentativas_ = 0

            #### Loop ####
            while tentativas_ < max_:
                # Se não for a primeira tentativa, espere um tempo fixo antes de tentar novamente
                if tentativas_ > 0:
                    sleep(10)  # Espera 10 segundos entre as tentativas

                # Tentar encontrar botao
                try:
                    # Crie uma instância de WebDriverWait
                    wait = WebDriverWait(driver, 20)

                    # Aguarde até que o elemento do campo de usuário seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Avançar')]")))

                    # Clique no elemento para focar
                    element.click()
                    sleep(3)  # Aguarda 3 segundos após o clique
                    print("\nCaptcha Resolvido com Sucesso!\n")
                    break  # Sair do loop se o elemento for encontrado com sucesso
                except:
                    tentativas_ += 1
                    print(f"\nTentativa {tentativas_} de {max_}: Elemento não encontrado. Tentando novamente...\n")

            if tentativas_ == max_:
                print("\nNúmero máximo de tentativas alcançado. O elemento não foi encontrado.\n")
                print("\nFalha ao Fazer Captcha\n")
                print("\nFechando Bot...\n")
                print("\nTrocando Ip...\n")
                # Desconecta do Cloudflare Warp
                #desconectar_warp()
                driver.quit()

            ############## CAPTCHA ########################
        
            usleep(15, 15)
            pyautogui.hotkey('ctrl', 'tab')
            pyautogui.hotkey('f5')

            # Defina o número máximo de tentativas
            max_tentativas = 3
            tentativas = 0
            
                    # Loop enquanto o elemento re_email não for encontrado e não ultrapassar o número máximo de tentativas
            while tentativas < max_tentativas:
                # Se não for a primeira tentativa, espere um tempo fixo antes de tentar novamente
                if tentativas > 0:
                    usleep(5, 5)  # Espera 10 segundos entre as tentativas
                    
                # Se for a primeira tentativa, atualize a página
                if tentativas == 0:
                    pyautogui.hotkey('f5')
                    usleep(1, 2)  # Aguardar 5 segundos após a atualização
                
                # Obter todas as alças de aba
                handles = driver.window_handles
                # Mudar o foco para a nova aba
                driver.switch_to.window(handles[0])

                # Tentar encontrar o email recebido
                try:
                    pyautogui.hotkey('f5')
                    wait = WebDriverWait(driver, 20)

                    # Aguarde até que o elemento do campo de usuário seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//*[@id='inbox-table']/tbody/tr")))

                    # Clique no elemento para focar
                    element.click()
                    usleep(20, 20)
                    pyautogui.hotkey('tab')
                    pyautogui.hotkey('tab')
                    pyautogui.hotkey('tab')
                    pyautogui.hotkey('tab')
                    usleep(1, 2)
                    pyautogui.hotkey('ctrl', 'a')
                    pyautogui.hotkey('ctrl', 'c')
                    # Encontrar o texto desejado e copiar os seis números após a palavra "app"
                    text = pyperclip.paste()  # Cole o texto copiado
                    with open("text.txt", "w") as arquivo:
                        arquivo.write(text)  # Salva o texto em um arquivo chamado "text.txt"
                        
                    match = re.search(r'app:\s*(\d{6})', text)  # Procura por "app" seguido de seis números
                    if match:
                        numero = match.group(1)
                        print("Número encontrado:", numero)
                        pyperclip.copy(numero)  # Copia os seis números para a área de transferência
                        # Apaga o texto após os números encontrados
                        text = text.replace(match.group(0), '')
                    else:
                        print("\nTexto não contém o padrão 'app: XXXXXX'\n")
                    break
                except:
                    tentativas += 1
                    print(f"\nTentativa {tentativas} de {max_tentativas}: Elemento não encontrado. Tentando novamente...\n")

            if tentativas == max_tentativas:
                print("\nNúmero máximo de tentativas alcançado. O elemento não foi encontrado.\n")
                print("\nFechando Bot...!\n")
                print("\nTrocando Ip...\n")
                # Desconecta do Cloudflare Warp
                #desconectar_warp()
                log_file.close()
                driver.quit()
        
            # Switch back to the original tab
            pyautogui.hotkey('ctrl', 'tab')
            usleep(1, 3)

            # Obter todas as alças de aba
            handles = driver.window_handles
            # Mudar o foco para a nova aba
            driver.switch_to.window(handles[1])

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            usleep(1, 3)

            # Input email from clipboard
            pyautogui.hotkey('ctrl', 'v')
            usleep(1, 3)

            pyautogui.hotkey('tab')
            usleep(1, 3)

            pyautogui.hotkey('enter')
            usleep(15, 15)

            # HTML da página
            html = '''
            <span class="x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928w xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm xkmlbd1 x2b8uid x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj" dir="auto" style="line-height: var(--base-line-clamp-line-height); --base-line-clamp-line-height: 18px;">Esse código não é válido. Você pode solicitar um novo.</span>
            '''

            # Código a ser verificado
            codigo_a_verificar = '\nEsse código não é válido. Você pode solicitar um novo.\n'

            # Parseando o HTML
            soup = BeautifulSoup(html, 'html.parser')

            # Encontrando todas as ocorrências de <span> com a classe especificada
            spans = soup.find_all('span', class_='x1lliihq x1plvlek xryxfnj x1n2onr6 x193iq5w xeuugli x1fj9vlw x13faqbe x1vvkbs x1s928w xhkezso x1gmr53x x1cpjm7i x1fgarty x1943h6x x1i0vuye xvs91rp xo1l8bm xkmlbd1 x2b8uid x1tu3fi x3x7a5m x10wh9bi x1wdrske x8viiok x18hxmgj')

            # Verificando se o código está presente
            codigo_presente = any(span.text.strip() == codigo_a_verificar for span in spans)

            print("\nConta Criada Com Sucesso!\n")
            # Insira aqui o código para continuar após o recarregamento da página

            usleep(10, 10)
            with open('logs/accounts.txt', 'a') as file:
                    file.write(f"{generated_name}\n{generated_pass}\n")
                
            print("\nUsuário e Senha salvos com sucesso em 'logs/accounts.txt'!\n")

            print("\nFechando Bot...!\n")
            print("\nTrocando Ip...\n")
            # Desconecta do Cloudflare Warp
            #desconectar_warp()
            log_file.close()
            driver.quit()
             
        except Exception as e:
            print(f"An error occurred: {str(e)}")
            print("\nRestarting the bot...\n")
            print("\nTrocando Ip...\n")
            usleep(3, 3)
            # Desconecta do Cloudflare Warp
            #desconectar_warp()
            log_file.close()
            driver.quit()
            continue  # Reinicie o loop   
        finally:
            if driver:
                driver.quit()  # Ensure the driver is always closed