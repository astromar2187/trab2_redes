import socket
import time
import json  
import select

# ISSO É MÁQUINA C
# A MÁQUINA C É O REMETENTE, ela deve ser capaz de enviar pacotes para a máquina B e aguardar o ACK

# Formato de mensagens:
# Dados: {'isACK': False, 'sequencia': int, 'mensagem': string, 'checksum': int}
# ACK: {'isACK': True, 'sequencia': int}

RED = '\033[91m'
BLUE = '\033[94m'
RESET = '\033[0m'
SERVER_IP = '127.0.0.1'  # IP da máquina intermediária
SERVER_PORT = 7070       # Porta da máquina intermediária
REMETENTE_IP = '127.0.0.1' # Máquina A (remetente)
REMETENTE_PORT = 8080      # Porta da máquina A (remetente)
#TIMEOUT = 2             # Tempo limite para ACK (segundos)

timeout = 8
totalpkg = 10

#mensagem_final = json.dumps({'sequencia': -1, 'mensagem': "FIM", 'checksum': calculate_checksum("-1:FIM")})
def calculate_checksum(data):
    return sum(data.encode()) % 256

def esperar_pacote(sock, timeout): # se nao receber o ack, retorna None
    print(f"Esperando pacote por {timeout} segundos...")

    start_time = time.time()
    ready = select.select([sock], [], [], timeout)
    
    if ready[0]: # se tiver algo para ler
        data, addr = sock.recvfrom(1024)
        print()
        print(f"Recebido pacote de {addr}: {data.decode()}")
        return data, addr # na hora que receber, retorna o pacote
    else: 
        print(f"{RED}Tempo esgotado sem receber pacotes.{RESET}")
        return None, None
    
def calculate_checksum(data):
    return sum(data.encode()) % 256

def enviar_pacote(sock, pacote): #envia e espera o ack
    sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
    print()
    print(f"Enviado: {pacote}")
    resposta, _ = esperar_pacote(sock, timeout)
    return resposta

def is_ack_valid(response, ack_num):
    if response['isACK'] == True and response['sequencia'] == ack_num:
        return True
    return False

def remetente_aut():
    mensagem = "Mensagem automatica"
    seq_num = 0
    checksum = calculate_checksum(f"{seq_num}:{mensagem}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((REMETENTE_IP, REMETENTE_PORT))  # Garante que está escutando no mesmo endereço
        for i in range(totalpkg):
            # Envia mensagem com número de sequência 0 inicialmente
            pacote = json.dumps({'isACK': False, 'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
            resposta = enviar_pacote(sock, pacote) # Liga o tempo e aguarda o ACK 0
            # Envia mensagem com número de sequência
            pacote = json.dumps({'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
            sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
            print(f"Enviado: {pacote}")



            sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
            print(f"Enviado: {pacote}")
            #time.sleep(2)

            while resposta is None: # Se o tempo esgotar e o ack não chegar, reenvia o pacote
                print("Erro no ack! Tempo esgotado")
                print("Reenviando pacote...")
                resposta = enviar_pacote(sock, pacote)
                continue

            # Se o ack chegar, verifica se é o ack correto e se a mensagem foi corrompida
            resposta = json.loads(resposta.decode())  # Decodifica a resposta recebida
            if not is_ack_valid(resposta, seq_num): # Se o ack não for o esperado, ignora a mensagem
                print(f"{RED} Erro no ack: ack não esperado. Ignorando...{RESET}") 
                continue # aqui ta dando um problema: a mensagem tá sendo reenviada antes do temporizador acabar

            # COMENTADO POIs Um ack corrompido é o mesmo que um ack não esperado
            '''if resposta['checksum'] != calculate_checksum(f"{isAck}{seq_num}"): # Se a mensagem foi corrompida, ignora a mensagem
                print(f"{BLUE} Erro no checksum: ack corrompido. Ignorando...{RESET}")
                continue'''
            
            # Se o ack chegou e a mensagem não foi corrompida, alterna o número de sequência
            # alterna o numero de seq entre 0 a 1
            print(f"ACK {seq_num} recebido com sucesso!")
            if seq_num == 0:
                seq_num = 1
            else:
                seq_num = 0
            
            time.sleep(1)  # Pausa de 1 segundo entre envios (opcional)
        #mensagem_final = json.dumps({'sequencia': -1, 'mensagem': "FIM", 'checksum': calculate_checksum("-1:FIM")})
        #sock.sendto(mensagem_final.encode(), (SERVER_IP, SERVER_PORT))
        #print(f"Enviado: {mensagem_final}")

def remetente_manual(): 
    mensagem = input("Digite a mensagem a ser enviada: ")
    seq_num = 0
    checksum = calculate_checksum(f"{seq_num}:{mensagem}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((REMETENTE_IP, REMETENTE_PORT))  # Garante que está escutando no mesmo endereço
        
        while True:
            # Envia mensagem com número de sequência
            pacote = json.dumps({'isACK': False, 'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
            resposta = sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT)) # NAO TEM TEMPORIZADOR NO MODO MANUAL

            while resposta is None: # Se o tempo esgotar e o ack não chegar, reenvia o pacote
                print("Erro no ack! Tempo esgotado")
                print("Reenviando pacote...")
                resposta = sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))
                continue

            # Se o ack chegar, verifica se é o ack correto e se a mensagem foi corrompida
            resposta = json.loads(resposta.decode())  # Decodifica a resposta recebida
            if not is_ack_valid(resposta, seq_num): # Se o ack não for o esperado, ignora a mensagem
                print(f"{RED} Erro no ack: ack não esperado. Ignorando...{RESET}") 
                continue # aqui ta dando um problema: a mensagem tá sendo reenviada antes do temporizador acabar

            # COMENTADO POIs Um ack corrompido é o mesmo que um ack não esperado
            '''if resposta['checksum'] != calculate_checksum(f"{isAck}{seq_num}"): # Se a mensagem foi corrompida, ignora a mensagem
                print(f"{BLUE} Erro no checksum: ack corrompido. Ignorando...{RESET}")
                continue'''
            
            # Se o ack chegou e a mensagem não foi corrompida, alterna o número de sequência
            # alterna o numero de seq entre 0 a 1
            print(f"ACK {seq_num} recebido com sucesso!")
            if seq_num == 0:
                seq_num = 1
            else:
                seq_num = 0
            
            time.sleep(1)  # Pausa de 1 segundo entre envios (opcional)
            print('quer enviar mais uma mensagem? [s/n]')
            continuar = input()
            if continuar == 's':
                mensagem = input("Digite a mensagem a ser enviada: ")
                checksum = calculate_checksum(f"{seq_num}:{mensagem}")
                terminar = False
            
                # Envia mensagem com número de sequência
                pacote = json.dumps({'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum, 'timeout': True})
                sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
                print(f"Enviado: {pacote}")


                # Aguarda ACK
                resposta, _ = sock.recvfrom(1024)
                resposta = json.loads(resposta.decode())  # Decodifica a resposta recebida


'''
                if resposta['ERROR'] == 'Sucesso':
                    ack = resposta['sequencia']
                    if ack == seq_num:
                        print(f"ACK {ack} recebido com sucesso!")
                        
                        # alterna o numero de seq entre 0 a 1
                        if seq_num == 0:
                            seq_num = 1
                        else:
                            seq_num = 0

                        while True:
                            print('quer enviar mais uma mensagem? [s/n]')
                            continuar = input()
                            if continuar == 's':
                                mensagem = input("Digite a mensagem a ser enviada: ")
                                checksum = calculate_checksum(f"{seq_num}:{mensagem}")
                                break
                            elif continuar == 'n':
                                terminar = True
                                break
                        if terminar:
                            break

                else:
                    print(f"Erro no ack! {resposta['ERROR']}")
                    print("Reenviando pacote...")
                    continue'''



if __name__ == "__main__":
    while True:
        print("Digite 0 para sair")
        print("Digite 1 para enviar uma mensagem manualmente")
        print("Digite 2 para enviar uma mensagem automaticamente")
        escolha = int(input("Digite uma opção: "))
        if escolha == 0:
            break
        elif escolha == 1:
            remetente_manual()
        elif escolha == 2:
            remetente_aut()
        else:
            print("Escolha inválida")
            continue
    
        

   


    
