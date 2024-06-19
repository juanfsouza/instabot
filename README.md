        chrome_opt.add_argument(f'user-agent={UserAgent}')
        chrome_opt.add_argument("--window-size=1920,1080")
        chrome_opt.add_argument('--ignore-certificate-errors')
        chrome_opt.add_argument('--allow-running-insecure-content')
        #chrome_opt.add_argument("--disable-extensions")
        chrome_opt.add_argument("--proxy-server='direct://'")
        chrome_opt.add_argument("--proxy-bypass-list=*")
        chrome_opt.add_argument("--start-maximized")
        chrome_opt.add_argument('--disable-gpu')
        chrome_opt.add_argument('--disable-dev-shm-usage')
                


                #CAPCHER AUDIO#


         pyautogui.hotkey('tab')

            usleep(1, 2)
            pyautogui.hotkey('enter')
            
            usleep(1, 2)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            
            usleep(1, 2)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')

            usleep(3, 5)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            usleep(1, 2)
            pyautogui.hotkey('enter')

            usleep(1, 2)
            pyautogui.hotkey('enter')

            usleep(3, 5)
            pyautogui.hotkey('ctrl', 'w')
            

            # Caminho para o arquivo de áudio
            caminho_audio = os.path.join(os.path.expanduser("~"), "Downloads", "audio.mp3")

            # Carregar o modelo
            modelo = whisper.load_model("base")

            # Transcrever o áudio
            resposta = modelo.transcribe(caminho_audio)

            # Acessar o texto transcrito usando a chave 'text'
            texto_transcrito = resposta['text']

            # Salvar o texto transcrito em um arquivo de texto
            with open("resp.txt", "w") as file:
                file.write(texto_transcrito)

            # Copiar o texto transcrito para a área de transferência
            pyperclip.copy(texto_transcrito)

            print("Texto transcrito copiado para a área de transferência e salvo em resp.txt:", texto_transcrito)

            # Excluir o arquivo de áudio
            os.remove(caminho_audio)

            # Limpar o arquivo resp.txt
            with open("resp.txt", "w") as file:
                file.write("")

            print("Arquivo de áudio removido e resp.txt limpo.")

            usleep(3, 5)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            usleep(1, 2)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            pyautogui.hotkey('ctrl', 'v')
            usleep(1, 2)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            usleep(1, 2)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            pyautogui.hotkey('enter')
            usleep(1, 2)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')

            pyautogui.hotkey('enter')
            usleep(15, 15)











                        link = "https://google.com/recaptcha/api2/demo"
            navegador.get(link)

            chave_captcha = navegador.find_element(By.CLASS_NAME, 'g-recaptcha').get_attribute('data-sitekey')
            respota = solver.solve_and_return_solution()

            solver = recaptchaV2Proxyless()
            solver.set_verbose(1)
            solver.set_key(chave_api)
            solver.set_website_url(link)
            solver.set_website_key(chave_captcha)

            if respota != 0:
                print(respota)
            else:
                print(solver.err_string)









# Iniciar o demo.py como um processo filho
demo_process = subprocess.Popen(["python", "demo.py"])

sleep(15)

def close_demo():
    print("Fechando demo.py...")
    demo_process.kill()  # Encerra o processo do demo.py












    EXTENSAO ANTI CAPTCHA 

    driver.get('https://chromewebstore.google.com/detail/nopecha-captcha-solver/dknlfmjaanfblgfdfebhijalfmhmjjjo')
            usleep(8888, 5)

            copy_email = driver.find_element(By.XPATH, '//*[@id="yDmH0d"]/c-wiz/div/div/main/div/section[1]/section/div[2]/div/button')
            copy_email.click()
            usleep(3, 5)

            usleep(3, 5)
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')

            usleep(5, 5)
            pyautogui.hotkey('f10')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            usleep(1, 2)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            usleep(1, 2)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            usleep(1, 2)

            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('tab')
            pyautogui.hotkey('enter')
            pyautogui.hotkey('ctrl', 'v')
            usleep(1, 2)

























driver.get(url_atual)

            # Obter o URL atual
            url_atual = driver.current_url

            # Aguardar um tempo para a página recarregar
            time.sleep(5)

            # Obter o novo URL após o recarregamento
            url_apos_recarregamento = driver.current_url

            # Comparar os URLs para verificar se houve recarregamento
            if url_apos_recarregamento != url_atual:
                print("Conta Criada Com Sucesso!")
                # Insira aqui o código para continuar após o recarregamento da página

                usleep(3, 5)
                with open('logs/accounts.txt', 'a') as file:
                        file.write(f"{generated_name}\n{generated_pass}\n")
                    
                print("Usuário e Senha salvos com sucesso em 'logs/accounts.txt'!")

                print("Fechando Bot...!")
                usleep(3, 3)
                print("Trocando Ip...")
                usleep(3, 3)
                # Registrar a função close_demo para ser executada quando o app.py for encerrado
                atexit.register(close_demo)
                driver.quit()
            else:
                print("Falha ao criar a conta no Instagram.")
                print("Verificar se conta tomou ban.")
























                # Aguarde até que o elemento do campo 'Editar perfil' seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//a[contains(text(), 'Editar perfil')]")))

                    # Clique no elemento para focar
                    element.click()
                    usleep(3, 5) 

                    # Aguarde até que o elemento do campo 'Alterar foto' seja clicável
                    element = wait.until(EC.element_to_be_clickable((By.XPATH, "//div[contains(text(), 'Alterar foto')]")))

                    # Clique no elemento para focar
                    element.click()
                    usleep(3, 5) 

                    # Selecione uma foto aleatória dentro da pasta
                    photo_path = select_random_photo(folder_path)
                    if photo_path:
                        pyautogui.typewrite(photo_path)
                        pyautogui.press("enter")
                    else:
                        print("Não foi possível encontrar fotos na pasta selecionada.")
                else:
                    print("Não foi possível encontrar pastas de fotos no diretório especificado.")

                # Aguarde até que o elemento do campo 'Alterar foto' seja clicável novamente
                element = wait.until(EC.element_to_be_clickable((By.XPATH, "//textarea[contains(text(), 'Alterar foto')]")))

                # Clique no elemento para focar
                element.click()
                usleep(3, 5) 

                # Função para remover as duas primeiras linhas do arquivo accounts.txt
                def remover_linhas():
                    with open('logs/accounts.txt', 'r') as file:
                        lines = file.readlines()  # Lê todas as linhas do arquivo
                    with open('logs/accounts.txt', 'w') as file:
                        file.writelines(lines[2:])  # Escreve todas as linhas, exceto as duas primeiras

                # Remover as duas primeiras linhas do arquivo accounts.txt
                remover_linhas()
                print("Duas primeiras linhas removidas do arquivo accounts.txt.")