#invoca os módulos necessários
import os                                                                      #para operações de BASH
import requests                                                                #para fazer requisições a sítios da internet
from requests.exceptions import ConnectTimeout                                 #necessário para gestão de erros de requests. 
from bs4 import BeautifulSoup                                                  #para extrair dados de sítios da internet
import logging                                                                 #para gerar arquivos log
from datetime import datetime                                                  #para fazer o query de data para o nome do log

# Configurar o logger
logging.basicConfig(filename=f"{datetime.now().strftime('%Y-%m-%d')}.log", level=logging.INFO, format='%(asctime)s - %(message)s', datefmt='%Y-%m-%d %H:%M:%S')


#cria o array de objetos

urlsParaChecar = [
                {
                'nome': '',
                'url':'',
                'ip': '',
                'tituloEsperado': '',
                'tituloEncontrado': '' #placeholder
                }
            ]


#Arquivo

def paraArquivo(urlsParaChecar):
    for url in urlsParaChecar:
        try:
            response = requests.get(url['url'], timeout=30)                                                     # Se alguma impressora não responder, aumentar o Timeout
            soup = BeautifulSoup(response.content, 'html.parser')                                               # Inicia o parser
            title_tag = soup.find('title')                                                                      # Procura o <title>
            if title_tag:                                                                                       # Booleana TRUE
                url['tituloEncontrado'] = title_tag.get_text(strip=True)                                        # Atribui o SN à propriedade do objeto sem espaços
                logging.info(f"Número de série encontrado para {url['nome']}: {url['tituloEncontrado']}")

                if url['tituloEncontrado'] == url['tituloEsperado']:
                    logging.info("")                                                                            # Pula uma linha
                    logging.info(f"Não há erros com a {url['nome']}.")
                    logging.info("")
                else:
                    logging.warning("")                                                                         # Pula uma linha
                    logging.warning("!!!" + "*"*150 + "!!!" )                                                   # Desenha linha separadora de erro
                    logging.warning(f"Número de série esperado da {url['nome']} é {url['tituloEsperado']}. O que encontrei foi {url['tituloEncontrado']}.")
                    logging.warning("!!!" + "*"*150 + "!!!" )
                    logging.warning("")
            else:
                logging.warning("")
                logging.warning("!!!" + "*"*150 + "!!!" )
                logging.warning(f"Não encontrei o número de série no HTML da {url['nome']}.")
                logging.warning("!!!" + "*"*150 + "!!!" )
                logging.warning("")
                continue                                                                                        # O iterador segue
         
        except ConnectTimeout as e:
            # Mensagem de erro do módulo requests
            logging.error("")                                                                                   # Pula uma linha
            logging.error("!!!" + "*"*150 + "!!!" )                                                             # Desenha linha separadora de erro
            error_message_requests = f"Timeout ao tentar se conectar a {url['url']} referente à {url['nome']}: {str(e)}"
            logging.error(error_message_requests)
            logging.error("")
            # Mensagem de erro personalizada
            error_message_custom = f"Não há impressora conectada ao ponto de rede {url['ip']}, onde deveria estar a {url['nome']}."
            logging.error(error_message_custom)
            logging.error("!!!" + "*"*150 + "!!!" )
            logging.error("")
            continue                                                                                                    # O iterador segue
        except requests.exceptions.RequestException as e:
            logging.error("")
            logging.error("!!!" + "*"*150 + "!!!" )
            logging.error(f"Erro ao fazer solicitação para {url['url']}: {str(e)}. Verifique as configurações da {url['nome']}. Serviço servidor WEB desabilitado.")
            logging.error("")
            logging.error("!!!" + "*"*150 + "!!!" )
            continue                                                                                                    # O iterador segue
        except Exception as e:                                                                                          # Captura qualquer outra exceção inesperada
            logging.error("")
            logging.error("!!!" + "*"*150 + "!!!" )
            logging.error(f"Erro inesperado ao processar {url['nome']} em {url['ip']}: {str(e)}")
            logging.error("")
            logging.error("!!!" + "*"*150 + "!!!" )
            continue                                                                                                    # O iterador segue

    input("Pressione ENTER para voltar ao menu.")                                                                       # fim da função. Retorno para main()

#Tela

def paraTela(urlsParaChecar):
    for url in urlsParaChecar:
        try:
            response = requests.get(url['url'], timeout=10)                                                     # Se alguma impressora não responder, aumentar o Timeout
            soup = BeautifulSoup(response.content, 'html.parser')                                               # Inicia o parser
            title_tag = soup.find('title')                                                                      # Procura o <title>
            if title_tag:                                                                                       # Booleana TRUE
                url['tituloEncontrado'] = title_tag.get_text(strip=True)                                        # Atribui o SN à propriedade do objeto sem espaços
                print(f"Número de série encontrado para {url['nome']}: {url['tituloEncontrado']}")

                if url['tituloEncontrado'] == url['tituloEsperado']:
                    print("")                                                                            # Pula uma linha
                    print(f"Não há erros com a {url['nome']}.")
                    print("")
                else:
                    print("")                                                                         # Pula uma linha
                    print("!!!" + "*"*142 + "!!!" )                                                   # Desenha linha separadora de erro
                    print(f"Número de série esperado da {url['nome']} é {url['tituloEsperado']}. O que encontrei foi {url['tituloEncontrado']}.")
                    print("!!!" + "*"*142 + "!!!" )
                    print("")
            else:
                print("")
                print("!!!" + "*"*142 + "!!!" )
                print(f"Não encontrei o número de série no HTML da {url['nome']}.")
                print("!!!" + "*"*142 + "!!!" )
                print("")
                continue                                                                                        # O iterador segue
         
        except ConnectTimeout as e:
           
           '''
            # Mensagem de erro do módulo requests
            print("")                                                                                   # Pula uma linha
            print("!!!" + "*"*150 + "!!!" )                                                             # Desenha linha separadora de erro
            error_message_requests = f"Timeout ao tentar se conectar a {url['url']} referente à {url['nome']}: {str(e)}"
            print(error_message_requests)
            print("")
            '''
           # Mensagem de erro personalizada
           print("")
           print("!!!" + "*"*142 + "!!!" )
           error_message_custom = f"Não há impressora conectada ao ponto de rede {url['ip']}, onde deveria estar a {url['nome']}."
           print(error_message_custom)
           print("!!!" + "*"*142 + "!!!" )
           print("")
           input("Pressione ENTER para continuar")
           continue                                                                                                    # O iterador segue
        
        except requests.exceptions.RequestException as e:
            print("")
            print("!!!" + "*"*142 + "!!!" )
            print(f"Erro ao fazer solicitação para {url['url']}: {str(e)}. Verifique as configurações da {url['nome']}. Serviço servidor WEB desabilitado.")
            print("")
            print("!!!" + "*"*142 + "!!!" )
            continue                                                                                                    # O iterador segue
        except Exception as e:                                                                                          # Captura qualquer outra exceção inesperada
            print("")
            print("!!!" + "*"*142 + "!!!" )
            print(f"Erro inesperado ao processar {url['nome']} em {url['ip']}: {str(e)}")
            print("")
            print("!!!" + "*"*142 + "!!!" )
            continue                                                                                                    # O iterador segue

    input("Pressione ENTER para voltar ao menu.")                                                                       # fim da função. Retorno para main()


#cria o menu

def criarMenu():
    #limpa a tela
    os.system("cls")

    # Linhas do topo e da parte de baixo da moldura
    linha_superior = "+" + "-" * 44 + "+"
    linha_inferior = "+" + "-" * 44 + "+"
    
    # Array do menu
    opcoes = [
        "| 1. Exibir resultados apenas no terminal    |",
        "| 2. Gravar em arquivo de log na mesma pasta |",
        "| 3. Sair                                    |"
    ]
    
    # Imprime a moldura e as opções do menu
    print(linha_superior)
    print(opcoes[0])
    print(opcoes[1])
    print(opcoes[2])
    print(linha_inferior)




def main():
    while True:
        criarMenu()
        opcao = input("Digite o número da opção desejada: ")

        if opcao == '1':
            paraTela(urlsParaChecar)
            
        elif opcao == '2':
            paraArquivo(urlsParaChecar)
            
        elif opcao == '3':
            print("")
            print("2024-02-29 --- Versão 1.0 --- Eder Castro: design, pesquisa e código -  &  - Everton Souza: design, pesquisa e testes")
            print("")
            input("Pressione ENTER para encerrar o programa")
            break
        else:
            print("Opção inválida. Por favor, escolha uma opção válida.")
            print("")
            input("Pressione ENTER para retornar ao menu")
            

if __name__ == "__main__":                                                          # necessário para o interpretador entender de que se trata de um script primário
    main()                                                                          # loop inicial








