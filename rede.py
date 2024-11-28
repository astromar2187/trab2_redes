import socket
import random
import time
import json 

# ISSO AQUI É A MÁQUINA B
# A MÁQUINA B É A INTERMEDIÁRIA

LISTEN_IP = '127.0.0.1'  # Máquina B escuta pacotes do remetente (máquina A)
LISTEN_PORT = 8080       # Porta da máquina B para escutar
DEST_IP = '127.0.0.1'    # Máquina C (destinatário)
DEST_PORT = 9090         # Porta da máquina C (destinatário)

def modo_automatico():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_in:
        sock_in.bind((LISTEN_IP, LISTEN_PORT))
        print(f"Máquina B escutando em {LISTEN_IP}:{LISTEN_PORT}...")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_out:
            while True:
                # Recebe pacote do remetente (Máquina C)
                pacote, endereco_remetente = sock_in.recvfrom(1024)
                print(f"Máquina B recebeu: {pacote.decode()}")

                # por algum motivo isso aqui buga quando eu tento fazer um loop infinito
                # ou seja, quando o atraso do pacote é random.random() < 1
                # ajeitar isso com mt reza veio
               # if random.random() < 0.1:  # 10% chance de perder o pacote
                #    print("Máquina B: pacote perdido!")
                 #   continue
                    

                tempo_inicial = time.time()
                # Repassa pacote para o destinatário (Máquina A)
                sock_out.sendto(pacote, (DEST_IP, DEST_PORT))
                print(f"Máquina B enviou para {DEST_IP}:{DEST_PORT}")

                # Recebe ACK do destinatário
                resposta, endereco_destinatario = sock_out.recvfrom(1024)
                print(f"Máquina B recebeu ACK: {resposta.decode()} de {endereco_destinatario}")

                # Simula um atraso de 20% de chance de atrasar o pacote
                if random.random() < 1:
                    print("Máquina B: atraso no envio do ACK...")
                    time.sleep(2)

                # Marcar se houve atraso
                tempo_final = time.time()
                resposta = json.loads(resposta.decode())
                if tempo_final - tempo_inicial >= 2:
                    resposta['atraso'] = True
                else:
                    resposta['atraso'] = False

                # Repassa o ACK para o remetente (Máquina C)
                resposta = json.dumps(resposta)
                sock_in.sendto(resposta.encode(), endereco_remetente)
                print(f"Máquina B repassou ACK para {endereco_remetente}")

if __name__ == "__main__":
    modo_automatico()
