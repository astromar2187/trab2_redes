import socket

# ISSO É MÁQUINA A

LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 9090

def destinatario():
    expected_seq_num = 0

    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((LISTEN_IP, LISTEN_PORT))
        print(f"Destinatário escutando em {LISTEN_IP}:{LISTEN_PORT}...")

        while True:
            # Recebe pacote
            pacote, endereco = sock.recvfrom(1024)
            pacote = pacote.decode()
            seq_num, mensagem = pacote.split(":", 1)
            seq_num = int(seq_num)

            if seq_num == expected_seq_num:
                print(f"Recebido: {mensagem} com SEQ {seq_num}")
                # Envia ACK
                sock.sendto(str(seq_num).encode(), endereco)
                print(f"ACK {seq_num} enviado!")
                expected_seq_num += 1  # Atualiza número de sequência esperado
            else:
                print("Número de sequência inesperado, ignorando mensagem.")

if __name__ == "__main__":
    destinatario()
