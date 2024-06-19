import atexit
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

from montador import get_browser_window_size

def close_demo(driver):
    driver.quit()

def usleep(a, b):
    sleep(uniform(a, b))

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
    # Create a UserAgent instance
    user_agent = UserAgent()

    # Get a random user agent
    user_string = user_agent.random

    # Set Chrome options
    options = uc.ChromeOptions()

    # Set the user agent... make sure to use '--' to flag the args
    options.add_argument(f'--user-agent={user_string}')

    # Emulate a touch-supported mobile device
    options.add_argument('--touch-events=enabled')

    try:
         # Limpar o conteúdo do arquivo de log
            with open("app_log.txt", "w") as log_file:
                log_file.write("")

            sys.stdout.reconfigure(line_buffering=True)
            sys.stdout.reconfigure(encoding='utf-8')

            # [1] save settings file as a variable

            #instructions = initialize_VPN(area_input=['Brazil']) # <-- Be aware: the area_input parameter expects a list, not a string

           # rotate_VPN(instructions) #refer to the instructions variable here
            #print('\n Rotacao de IPS BR Gerados Com Sucesso!\n')
            #sleep(15)

            # Inicializar o navegador Chrome
            driver = uc.Chrome(options=options)
            print('\nIniciando Bot\n')

            class BaseTestCase(BaseCase):
                def setUp(self):
                    super().setUp()
                    stealth(self.driver)

            # Defina listas de opções para cada configuração do Selenium Stealth
            languages_options = [["pt-BR", "pt"]]
            platform_options = ["Win32", "Win64"]
            webgl_vendor_options = ["Qualcomm"]
            intel_renderer_options = ["Adreno(TM) 640"]
            nvidia_renderer_options = [
                "Adreno(TM) 640",
                "Adreno(TM) 405",
                "Adreno(TM) 620",
                "Adreno(TM) 512",
                "Adreno(TM) 618",
                "Adreno(TM) 308",
                "Adreno(TM) 506",
                "Adreno(TM) 505",
                "Adreno(TM) 620",
            ]

            # Escolha aleatoriamente uma opção para cada configuração móvel
            random_languages = random.choice(languages_options)
            random_platform = random.choice(platform_options)
            random_webgl_vendor = random.choice(webgl_vendor_options)
            random_renderer = ""

            # Verifica se é um dispositivo móvel
            if random_platform.startswith("Win"):
                random_platform = "Win32"  # Defina como Win32 para simular um dispositivo móvel
                random_vendor = "Qualcomm"  # Defina o fornecedor para Qualcomm
                random_renderer = random.choice(intel_renderer_options + nvidia_renderer_options)
            else:
                # Neste caso, não é um dispositivo móvel
                random_vendor = ""  # Não especificado

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
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.80 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.80 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.118 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.118 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.118 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.90 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.6312.99 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.6367.82 Mobile Safari/537.36",
                "Mozilla/5.0 (Linux; Android 10; K) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.6261.119 Mobile Safari/537.36",
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
            new_width = 500  # Coloque o valor desejado para a largura da janela
            new_height = 750  # Coloque o valor desejado para a altura da janela

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
            conectar_warp()
            usleep(3, 5)

            driver.get('https://mohmal.com/pt/inbox')
            usleep(99995, 5)

            # Copy the email
            copy_email = driver.find_element(By.CSS_SELECTOR, '#ajax-html > div.bg-cloud.text-light.py-3.py-md-4 > div > div > div.flex-grow-1 > div.box-index.p-3.text-center.rounded-3 > div.d-flex.justify-content-center.flex-wrap.pt-1.py-3.position-relative > button:nth-child(1)')
            copy_email.click()

            # Switch to the new tab
            handles = driver.window_handles
            driver.switch_to.window(handles[-1])

            driver.execute_script("window.open('https://www.instagram.com/','_blank');")
            usleep(3, 5)

            element = WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mount_0_0_4d']/div/div/div[2]/div/div/div[1]/section/main/article/div/div/div/div/div[2]/div[3]/button[2]")))
            element.click()

            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='mount_0_0_4d']/div/div/div[2]/div/div/div[1]/section/main/div[2]/div/div[1]/span[2]"))).click()
            usleep(3, 5)

            WebDriverWait(driver, 20).until(EC.element_to_be_clickable((By.XPATH, "//*[@id='fc2592d8391c4e898']"))).click()

            # Close the driver after actions are done
            close_demo(driver)
             
    except Exception as e:
        print(f"An error occurred: {str(e)}")
        print("\nRestarting the bot...\n")
        print("\nTrocando Ip...\n")
        usleep(3, 3)
        # Desconecta do Cloudflare Warp
        desconectar_warp()
        log_file.close()
        driver.quit()
    finally:
        # Certifique-se de que o driver seja fechado, independentemente de quaisquer exceções
        try:
            desconectar_warp()
            log_file.close()
            driver.quit()
        except:
            pass
