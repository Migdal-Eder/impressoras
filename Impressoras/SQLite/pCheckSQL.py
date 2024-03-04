import os                                                                                       #para operacoes de bash
import requests                                                                                 #para fazer requisicoes a sitios de internet
from requests.exceptions import ConnectTimeout                                                  #necessário para gestão de erros de requests
from bs4 import BeautifulSoup                                                                   #para extrair dados de sítios da internet
import logging                                                                                  #para gerar arquivos log
from datetime import datetime                                                                   #para fazer o query de data para o nome do log
import sqlite3                                                                                  #para mudancas persistentes via DB

# Configurar o logger
logging.basicConfig(filename=f"{datetime.now().strftime('%Y-%m-%d')}.log", level=logging.INFO,  #configura o nome do arquivo
                    format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')            #configura o conteudo do arquivo

# Conectar ao banco de dados SQLite
conn = sqlite3.connect('impressoras.db')                                                        #conecta o DB
c = conn.cursor()                                                                               #ativa o operador-cursor

# Verificar se a tabela existe, se não, criar a tabela
c.execute('''CREATE TABLE IF NOT EXISTS impressoras
             (nome TEXT, url TEXT, tituloEsperado TEXT, tituloEncontrado TEXT)''')              #na mesma pasta do script ou executavel

# Função para exibir resultados apenas no terminal
def paraTela():
    c.execute('SELECT * FROM impressoras')                                                      #seleciona todas os itens do DB
    urlsParaChecar = c.fetchall()                                                               #atribui o resultado a variavel
    for url in urlsParaChecar:                                                                  #inicia o iterador
        try:                                                                                    #gestao de erros de timeout
            response = requests.get(url[1])                                                     #busca a url da impressora
            response.raise_for_status()                                                         #verifica a resposta da impressora
            if response.status_code == 200:                                                     #200 a 299 é o range ideal
                soup = BeautifulSoup(response.content, 'html.parser')                           #inicia o parser
                title_tag = soup.find('title')                                                  #busca o <title> dentro do HTML
                if title_tag:                                                                   #se o acha...
                    titulo_encontrado = title_tag.get_text(strip=True)                          #atribui a variavel sem espacos em branco
                    print(f"Número de série encontrado para {url[0]}: {titulo_encontrado}")
                    if titulo_encontrado == url[2]:                                             #os numeros entre [] nao sao indexes de array, mas de tuplas. por isto a numeracao diferente no codigo base do iterador
                        print(f"Não há erros com a {url[0]}.")
                    else:
                        print(f"Número de série esperado da {url[0]} é {url[2]}. O que encontrei foi {titulo_encontrado}.")
                else:
                    print(f"Não encontrei o número de série no HTML de {url[0]}.")
            else:
                print(f"Falha de comunicação com {url[0]}.")                                    #ocorre apenas num erro tipo 404
        except ConnectTimeout as e:                                                             #para erros de timeout, que crashavam o script antes do try, pois o modulo request nao os comporta
            print(f"Timeout ao tentar se conectar a {url[1]}: {e}")
            continue
        except requests.exceptions.RequestException as e:                                       #exclusivo para requests
            print(f"Erro ao fazer solicitação para {url[1]}: {e}")
            continue
        except Exception as e:                                                                  #para demais excecoes
            print(f"Erro inesperado ao processar {url[0]}: {e}")
            continue
    input("Pressione ENTER para voltar ao menu.")

# Função para gravar em arquivo de log na mesma pasta
def paraArquivo():
    c.execute('SELECT * FROM impressoras')
    urlsParaChecar = c.fetchall()
    for url in urlsParaChecar:
        try:
            response = requests.get(url[1])
            response.raise_for_status()
            if response.status_code == 200:
                soup = BeautifulSoup(response.content, 'html.parser')
                title_tag = soup.find('title')
                if title_tag:
                    titulo_encontrado = title_tag.get_text(strip=True)
                    logging.info(f"Número de série encontrado para {url[0]}: {titulo_encontrado}")  #o logging e o mudolo de escrita no arquivo configurado no cabecalho do script
                    if titulo_encontrado == url[2]:
                        logging.info(f"Não há erros com a {url[0]}.")
                    else:
                        logging.warning(f"Número de série esperado da {url[0]} é {url[2]}. O que encontrei foi {titulo_encontrado}.")
                else:
                    logging.warning(f"Não encontrei o número de série no HTML de {url[0]}.")
            else:
                logging.error(f"Falha de comunicação com {url[0]}.")
        except ConnectTimeout as e:
            logging.error(f"Timeout ao tentar se conectar a {url[1]}: {e}")
            continue
        except requests.exceptions.RequestException as e:
            logging.error(f"Erro ao fazer solicitação para {url[1]}: {e}")
            continue
        except Exception as e:
            logging.exception(f"Erro inesperado ao processar {url[0]}: {e}")
            continue
    print("")
    print(f"Arquivo de log gravado com sucesso.")
    print("")
    input("Pressione ENTER para voltar ao menu.")

# Função para adicionar uma impressora
def adicionarURL():
    print("Antes de adicionar uma impressora para validação a este programa, certifique-se de tê-la pingado antes e")
    print("de ter verificado se a tag <title> no HTML contem o dado desejado.")
    print("")
    input("Pressione ENTER para continuar")
    print("")
    nome = input("Digite o nome da impressora: ")
    url = input("Digite a URL da impressora: ")
    tituloEsperado = input("Digite o número de série esperado como ele aparece na tag <title>: ")

    # Inserir os dados no banco de dados SQLite
    c.execute("INSERT INTO impressoras VALUES (?, ?, ?, ?)", (nome, url, tituloEsperado, ''))                                   #cria a tupla com as variaveis atribuidas pelo input                                 
    conn.commit()                                                                                                               #grava a tupla no DB         
    print("")
    print("Nova impressora adicionada com sucesso!")
    print("")
    input("Pressione ENTER para retornar ao menu.")

# Função para criar o menu
def criarMenu():
    os.system("cls")
    linha_superior = "+" + "-" * 44 + "+"                                                                                        #moldura
    linha_inferior = "+" + "-" * 44 + "+"                                                                                        #moldura
    opcoes = [
        "| 1. Exibir resultados apenas no terminal    |",
        "| 2. Gravar em arquivo de log na mesma pasta |",
        "| 3. Adicionar uma impressora                |",
        "| 4. Exibir banco de dados                   |",
        "| 5. Excluir impressora                      |",
        "| 6. Sair                                    |"
    ]
    print(linha_superior)
    for opcao in opcoes:
        print(opcao)
    print(linha_inferior)

# Função para exibir o conteúdo do banco de dados na tela
def exibirBancoDados():
    try:
        c.execute('SELECT * FROM impressoras')  # Executa uma consulta SQL para selecionar todos os registros da tabela
        registros = c.fetchall()  # Recupera todos os registros retornados pela consulta
        if registros:  # Verifica se existem registros para exibir
            print("Conteúdo do banco de dados:")
            for registro in registros:
                print(registro)  # Imprime cada registro na tela
        else:
            print("O banco de dados está vazio.")
    except sqlite3.Error as e:
        print(f"Erro ao tentar exibir o banco de dados: {e}")
    input("pressione ENTER para retornar ao menu")

# Função para excluir uma impressora do banco de dados
def excluirImpressora():
    try:
        nome_excluir = input("Digite o nome da impressora que deseja excluir: ")
        # Exclui a impressora do banco de dados
        c.execute("DELETE FROM impressoras WHERE nome = ?", (nome_excluir,))
        conn.commit()
        print("Impressora excluída com sucesso.")
    except sqlite3.Error as e:
        print(f"Erro ao tentar excluir a impressora: {e}")
    input("pressione ENTER para retornar ao menu")

# Função principal
def main():
    while True:
        criarMenu()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            paraTela()
        elif opcao == '2':
            paraArquivo()
        elif opcao == '3':
            adicionarURL()
        elif opcao == '4':
            exibirBancoDados()  # Chama a função para exibir o banco de dados na tela
        elif opcao == '5':
            excluirImpressora()  # Chama a função para excluir impressoras
        elif opcao == '6':
            print("")
            print("2024-02-27 --- Versão 1.1 --- Eder Castro")
            print("")
            input("Pressione ENTER para encerrar o programa")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print("")
            input("Pressione ENTER para retornar ao menu")

if __name__ == "__main__":
    main()
