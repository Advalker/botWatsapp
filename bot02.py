from selenium import webdriver
import time
import os
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys

# Configurações do WebDriver e WhatsApp Web
dir_path = os.getcwd()
chrome_options2 = Options()
chrome_options2.add_argument(r"user-data-dir=" + os.path.join(dir_path, "profile/zap"))
driver = webdriver.Chrome(options=chrome_options2)
driver.get('https://web.whatsapp.com/')

time.sleep(15)  # Aguarda o carregamento do WhatsApp Web

# Perguntas a serem feitas durante a coleta de informações
perguntas = [
    "Olá! para facilitar vou precisar de algumas informações. OK?",
    "Agora, por favor, me diga o seu nome.",
    "Como posso ajudar você hoje?",
    "Entendi. Por favor, me informe o número de série do equipamento.",
    "Por favor, envie mais detalhes.",
]

def enviar_mensagem(mensagem):
    """Envia uma mensagem no chat ativo."""
    caixa_texto = driver.find_element(By.CLASS_NAME, '_ak1l')  # Classe CSS da caixa de entrada de texto
    caixa_texto.click()
    caixa_texto.send_keys(mensagem + Keys.ENTER)

def aguardar_resposta(ultima_mensagem_enviada, timeout=30):
    """Aguarda a resposta do usuário e retorna o texto da última mensagem recebida após a última mensagem enviada."""
    start_time = time.time()
    while True:
        time.sleep(2)  # Aguarda 2 segundos antes de verificar novamente
        todas_as_msg = driver.find_elements(By.CLASS_NAME, '_akbu')  # Classe CSS das mensagens
        if todas_as_msg:
            msg_recebida = todas_as_msg[-1].text.strip().lower()
            if msg_recebida != ultima_mensagem_enviada.lower() and msg_recebida:  # Verifica se a mensagem recebida é diferente da última mensagem enviada
                print(f"Mensagem recebida: {msg_recebida}")
                return msg_recebida
        if time.time() - start_time > timeout:
            enviar_mensagem("Conversa encerrada por falta de diálogo. Se precisar de algo mais, estou à disposição.")
            return None  # Retorna None se o tempo limite for atingido

def coletar_informacoes():
    """
    Coleta informações do usuário através de uma série de perguntas.
    Envia as perguntas e aguarda as respostas do usuário.
    """
    nome_usuario = None  # Variável para armazenar o nome do usuário
    for pergunta in perguntas:
        enviar_mensagem(pergunta)
        resposta = aguardar_resposta(pergunta)

        if resposta is None:
            return nome_usuario, None  # Retorna None para sinalizar que a coleta de informações foi interrompida

        # Verifica se a pergunta é sobre o nome e armazena a resposta
        if "nome" in pergunta.lower():
            nome_usuario = resposta.capitalize()  # Armazena o nome do usuário com a primeira letra maiúscula

    return nome_usuario, perguntas

def revisar_informacoes(nome_usuario):
    """
    Exibe as informações coletadas para o usuário verificar e confirma se estão corretas.
    Permite ao usuário refazer alguma parte se necessário.
    """
    while True:
        # Exibe as informações coletadas para o usuário em uma única mensagem
        resumo = "Aqui estão as informações que eu coletei:\n"
        resumo += f"Nome: {nome_usuario}\n" if nome_usuario else "Nome não fornecido.\n"
        resumo += "\nAs informações estão corretas? Responda 'sim' para confirmar ou 'não' para refazer algo."

        enviar_mensagem(resumo)

        resposta = aguardar_resposta(resumo)

        if resposta is None:
            enviar_mensagem("Desculpe, não consegui obter uma resposta. A conversa será encerrada.")
            break

        if "sim" in resposta:
            enviar_mensagem("Ótimo! As informações foram confirmadas. Aguarde um de nossos atendentes.")
            break
        elif "não" in resposta:
            enviar_mensagem("Qual informação você gostaria de refazer? Por favor, informe o número correspondente.")
            resposta = aguardar_resposta("Qual informação você gostaria de refazer?")

            if resposta is None:
                enviar_mensagem("Desculpe, não consegui obter uma resposta. A conversa será encerrada.")
                break

            try:
                indice = int(resposta) - 1
                if 0 <= indice < len(perguntas):
                    # Refaz a pergunta correspondente
                    enviar_mensagem(f"Vamos refazer a pergunta {indice + 1}. {perguntas[indice]}")
                    nova_resposta = aguardar_resposta(perguntas[indice])

                    if nova_resposta is None:
                        enviar_mensagem("Desculpe, não consegui obter uma resposta. A conversa será encerrada.")
                        break

                    # Atualiza a informação (se necessário)
                    if "nome" in perguntas[indice].lower():
                        nome_usuario = nova_resposta.capitalize()
                else:
                    enviar_mensagem("Número inválido. Tente novamente.")
            except ValueError:
                enviar_mensagem("Por favor, responda com um número válido.")
        else:
            enviar_mensagem("Não entendi. Por favor, responda 'sim' ou 'não'.")

    return nome_usuario

def bot():
    try:
        # Procurar por novas notificações (bolinha verde de nova mensagem)
        bolinhas = driver.find_elements(By.CLASS_NAME, '_ahlk')  # Classe CSS de notificação de nova mensagem
        if bolinhas:
            print("Nova notificação encontrada.")
            ultima_bolinha = bolinhas[-1]
            ultima_bolinha.click()  # Clica na bolinha para abrir o chat com nova mensagem
            
            nome_usuario, perguntas = coletar_informacoes()
            if nome_usuario is not None:
                nome_usuario = revisar_informacoes(nome_usuario)
            
            # Mensagem final usando o nome do usuário
            if nome_usuario:
                mensagem_final = f"Obrigado {nome_usuario}! As informações foram confirmadas. Aguarde um de nossos atendentes."
            else:
                mensagem_final = "Obrigado! As informações foram confirmadas. Aguarde um de nossos atendentes."

            enviar_mensagem(mensagem_final)
            print(f"Informações revisadas e confirmadas: {nome_usuario}")

    except Exception as e:
        print(f'Erro ao buscar novas notificações: {e}')

# Loop contínuo para verificar novas mensagens
while True:
    bot()
    time.sleep(5)  # Aguarda 5 segundos antes de verificar novamente
