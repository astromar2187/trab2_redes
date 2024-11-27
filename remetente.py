import socket
import time

# ISSO É MAQUINA C
# A MÁQUINA C É O REMETENTE, ela deve ser capaz de enviar pacotes para a máquina B e aguardar o ACK
# Segue protocolo pare e espere (stop-and-wait)

SERVER_IP = '127.0.0.1'  # IP da máquina intermediária
SERVER_PORT = 8080       # Porta da máquina intermediária
TIMEOUT = 2              # Tempo limite para ACK (segundos)

def remetente():
    mensagem = "Hello, RDT 3.0!"
    seq_num = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.settimeout(TIMEOUT)

        while True:
            # Envia mensagem com número de sequência
            pacote = f"{seq_num}:{mensagem}"
            sock.sendto(pacote.encode(), (SERVER_IP, SERVER_PORT))
            print(f"Enviado: {pacote}")

            try:
                # Aguarda ACK
                resposta, _ = sock.recvfrom(1024)
                ack = int(resposta.decode())

                if ack == seq_num:
                    print(f"ACK {ack} recebido com sucesso!")
                    seq_num += 1
                    time.sleep(1)
                else:
                    print("ACK errado, retransmitindo...")
            except socket.timeout:
                print("Timeout! Retransmitindo...")

if __name__ == "__main__":
    remetente()
