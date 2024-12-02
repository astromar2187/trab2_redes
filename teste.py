import socket
import select
import time

SERVER_IP = '127.0.0.1'  # IP da máquina intermediária
SERVER_PORT = 7070       # Porta da máquina intermediária
REMETENTE_IP = '127.0.0.1' # Máquina A (remetente)
REMETENTE_PORT = 8080      # Porta da máquina A (remetente)
#TIMEOUT = 2             # Tempo limite para ACK (segundos)


def esperar_pacote(sock_in, timeout):
    print(f"Esperando pacote por {timeout} segundos...")

    start_time = time.time()
    ready = select.select([sock], [], [], timeout)
    
    if ready[0]:
        data, addr = sock_in.recvfrom(1024)
        print(f"Recebido pacote de {addr}: {data.decode()}")
    else:
        print("Tempo esgotado sem receber pacotes.")
    
    sock.close()

# Exemplo de uso: esperar por um pacote UDP por 10 segundos
esperar_pacote(10)

    
