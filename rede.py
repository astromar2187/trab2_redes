import socket
import random
import time

# ISSO AQUI É A MÁQUINA B
# A MÁQUINA B É A INTERMEDIÁRIA, ela deve ser capaz de receber pacotes do remetente e repassar para o destinatário e vice-versa.
# Alternativamente, ela deve poder interferir na comunicação, podendo simular a perda, corrupção ou atraso de pacotes

LISTEN_IP = '127.0.0.1'  # Máquina B escuta pacotes do remetente
LISTEN_PORT = 8080       # Porta da máquina B para escutar
DEST_IP = '127.0.0.1'    # Máquina C (destinatário)
DEST_PORT = 9090         # Porta da máquina C

def modo_automatico():
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_in:
        sock_in.bind((LISTEN_IP, LISTEN_PORT))
        print(f"Máquina B escutando em {LISTEN_IP}:{LISTEN_PORT}...")

        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_out:
            while True:
                # Recebe pacote do remetente
                pacote, endereco_remetente = sock_in.recvfrom(1024)
                print(f"Máquina B recebeu: {pacote.decode()}")

                # Simular intervenções (perda ou atraso)
                if random.random() < 0.1:  # 10% chance de perder o pacote
                    print("Máquina B: pacote perdido!")
                    continue
                if random.random() < 0.2:  # 20% chance de atrasar o pacote
                    print("Máquina B: atraso no envio...")
                    time.sleep(1)

                # Repassa pacote para o destinatário
                sock_out.sendto(pacote, (DEST_IP, DEST_PORT))
                print(f"Máquina B enviou para {DEST_IP}:{DEST_PORT}")

                # Recebe ACK do destinatário
                resposta, endereco_destinatario = sock_out.recvfrom(1024)
                print(f"Máquina B recebeu ACK: {resposta.decode()} de {endereco_destinatario}")

                # Repassa o ACK para o remetente
                sock_in.sendto(resposta, endereco_remetente)
                print(f"Máquina B repassou ACK para {endereco_remetente}")

#def modo_manual():

if __name__ == "__main__":
    modo_automatico()
