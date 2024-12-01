import socket
import time
import json  

# ISSO É MÁQUINA C
# A MÁQUINA C É O REMETENTE, ela deve ser capaz de enviar pacotes para a máquina B e aguardar o ACK

SERVER_IP = '127.0.0.1'  # IP da máquina intermediária
SERVER_PORT = 7070       # Porta da máquina intermediária
REMETENTE_IP = '127.0.0.1' # Máquina A (remetente)
REMETENTE_PORT = 8080      # Porta da máquina A (remetente)
TIMEOUT = 2             # Tempo limite para ACK (segundos)

def remetente_aut():
    mensagem = "plutao nao e mais planeta!!"
    seq_num = 0
    checksum = calculate_checksum(f"{seq_num}:{mensagem}")

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
    

        while True:
            # Envia mensagem com número de sequência
            pacote = json.dumps({'sequencia': seq_num, 'mensagem': mensagem, 'checksum': checksum})
            sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))  # Envia o pacote como bytes
            print(f"Enviado: {pacote}")
            time.sleep(2)

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

def remetente_manual(): 
    pass

def calculate_checksum(data):
    return sum(data.encode()) % 256

if __name__ == "__main__":
    remetente()
