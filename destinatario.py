import socket
import json 

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
            pacote = json.loads(pacote.decode())  # Decodifica os bytes e converte de volta para dicionário
            seq_num = pacote['sequencia']
            mensagem = pacote['mensagem']
            valor_checksum = pacote['checksum']

            checksum_calculado = calculate_checksum(f"{expected_seq_num}:{mensagem}")


            if valor_checksum == checksum_calculado:
                print(f"teste de checksum \nMensagem: '{mensagem}' com checksum {checksum_calculado}")
                print('integridade do pacote conferida com sucesso por meio do checksum! o pacote foi corretamente recebido!')
            else:
                print(f"teste de checksum \nMensagem: '{mensagem}' com checksum {checksum_calculado}")
                print("erro na integridade do pacote! checksum inesperado!")
           

            if seq_num == expected_seq_num:
                print(f"teste de sequencia: Mensagem: '{mensagem}' com SEQ {seq_num}")
                print('numero de sequencia correto! mensagem corretamente recebida!')
                # Envia ACK
                sock.sendto(str(seq_num).encode(), endereco)
                print(f"ACK {seq_num} enviado!")
                expected_seq_num += 1  # Atualiza número de sequência esperado
            else:
                print("Número de sequência inesperado, ignorando mensagem.")


def calculate_checksum(data):
    return sum(data.encode()) % 256

if __name__ == "__main__":
    destinatario()
