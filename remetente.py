import socket
import time
import json  

# ISSO É MÁQUINA C
# A MÁQUINA C É O REMETENTE, ela deve ser capaz de enviar pacotes para a máquina B e aguardar o ACK

# Formato de mensagens:
# Dados: {'isACK': False, 'sequencia': int, 'mensagem': string, 'checksum': int}
# ACK: {'isACK': True, 'sequencia': int}

SERVER_IP = '127.0.0.1'  # IP da máquina intermediária
SERVER_PORT = 7070       # Porta da máquina intermediária
REMETENTE_IP = '127.0.0.1' # Máquina A (remetente)
REMETENTE_PORT = 8080      # Porta da máquina A (remetente)
#TIMEOUT = 2             # Tempo limite para ACK (segundos)

timeout = 2
totalpkg = 30

#mensagem_final = json.dumps({'sequencia': -1, 'mensagem': "FIM", 'checksum': calculate_checksum("-1:FIM")})

def temporizador(tempo):
    print("Temporizador iniciado")
    while tempo > 0:
        tempo -= 1
        time.sleep(1)
    return True
    
def calculate_checksum(data):
    return sum(data.encode()) % 256

def remetente_aut():
    mensagem = "Mensagem automatica"
    seq_num = 0

    checksum = calculate_checksum(f"{seq_num}:{mensagem}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((REMETENTE_IP, REMETENTE_PORT))  # Garante que está escutando no mesmo endereço
        for i in range(totalpkg):
            # Envia mensagem com número de sequência
            pacote = json.dumps({'isACK': False, 'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
            sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
            print(f"Enviado: {pacote}")
            #time.sleep(2)

            # Aguarda ACK
            resposta, _ = sock.recvfrom(1024)
            resposta = json.loads(resposta.decode())  # Decodifica a resposta recebida
            if resposta.get('atraso'):
                print("ACK atrasado, reenviando...")
                continue

            ack = resposta['sequencia']
            if ack == seq_num:
                
                # alterna o numero de seq entre 0 a 1
                if seq_num == 0:
                    seq_num = 1
                else:
                    seq_num = 0
                print(f"ACK {ack} recebido com sucesso!")
                time.sleep(1)  # Pausa de 1 segundo entre envios (opcional)
                break
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
                pacote = json.dumps({'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
                sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
                print(f"Enviado: {pacote}")





                # Aguarda ACK
                resposta, _ = sock.recvfrom(1024)
                resposta = json.loads(resposta.decode())  # Decodifica a resposta recebida


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
                                break

                else:
                    print(f"Erro no ack! {resposta['ERROR']}")
                    print("Reenviando pacote...")
                    continue



if __name__ == "__main__":
    while True:
        print("Digite 0 para sair")
        print("Digite 1 para enviar uma mensagem manualmente")
        print("Digite 2 para enviar uma mensagem automaticamente")
        escolha = int(input())
        if escolha == 0:
            break
        elif escolha == 1:
            remetente_manual()
        elif escolha == 2:
            remetente_aut()
        else:
            print("Escolha inválida")
            continue
    
        

   


    
