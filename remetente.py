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
    mensagem = "plutao nao e mais planeta!!"
    seq_num = 0
    checksum = calculate_checksum(f"{seq_num}:{mensagem}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    
        
        for i in range(totalpkg):
            # Envia mensagem com número de sequência
<<<<<<< HEAD
            #pacote = json.dumps({'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
            ack = json.dumps({'isACK': True, 'sequencia': seq_num}) 
            #sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
            sock.sendto(ack.encode(), (SERVER_IP, SERVER_PORT))
            #print(f"Enviado: {pacote}")
            print(f"Enviado: {ack}")
            seq_num += 1  # Atualiza o número de sequência para o próximo pacote
=======
            pacote = json.dumps({'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})

            # alterna o numero de seq entre 0 a 1
            if seq_num == 0:
                seq_num = 1
            else:
                seq_num = 0

            
            sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
            print(f"Enviado: {pacote}")
>>>>>>> 58354cf41bd02ab98922294be81d0680897541ec
            #time.sleep(2)

            # Aguarda ACK
            '''resposta, _ = sock.recvfrom(1024)
            resposta = json.loads(resposta.decode())  # Decodifica a resposta recebida
            if resposta.get('atraso'):
                print("ACK atrasado, reenviando...")
                continue

            ack = resposta['sequencia']
            if ack == seq_num:
                print(f"ACK {ack} recebido com sucesso!")
                seq_num += 1  # Atualiza o número de sequência para o próximo pacote
                time.sleep(1)  # Pausa de 1 segundo entre envios (opcional)
                break'''

        mensagem_final = json.dumps({'sequencia': -1, 'mensagem': "FIM", 'checksum': calculate_checksum("-1:FIM")})
        sock.sendto(mensagem_final.encode(), (SERVER_IP, SERVER_PORT))
        print(f"Enviado: {mensagem_final}")

def remetente_manual(): 
    pass



if __name__ == "__main__":
    remetente_aut()

    
