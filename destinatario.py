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
            pacote, endereco = sock.recvfrom(1024)
            pacote = json.loads(pacote.decode())  # Decodifica os bytes e converte de volta para dicionário
            print(f"Destinatário recebeu: {pacote}")
    


        while False:
            # Recebe pacote
            pacote, endereco = sock.recvfrom(1024)
            pacote = json.loads(pacote.decode())  # Decodifica os bytes e converte de volta para dicionário
            seq_num = pacote['sequencia']
            mensagem = pacote['mensagem']
            valor_checksum = pacote['checksum']

            checksum_calculado = calculate_checksum(f"{expected_seq_num}:{mensagem}")

            # Verifica se o checksum está correto
            if valor_checksum == checksum_calculado:
                print(f"Checksum correto! Mensagem: '{mensagem}' com checksum {checksum_calculado}")
            else:
                print(f"Erro no checksum! Mensagem: '{mensagem}' com checksum {checksum_calculado}")

            # Verifica se o número de sequência está correto
            if seq_num == expected_seq_num:
                print(f"Mensagem recebida com SEQ {seq_num}: '{mensagem}'")
                # Envia ACK
                res = {'sequencia': seq_num, 'atraso': False}
                res = json.dumps(res)
                sock.sendto(res.encode(), endereco)
                print(f"ACK {seq_num} enviado para {endereco}")
                expected_seq_num += 1  # Atualiza número de sequência esperado
            elif seq_num < expected_seq_num:
                print(f"Recebido pacote duplicado com SEQ {seq_num}, descartando...")
                # Envia ACK
                res = {'sequencia': seq_num, 'atraso': False}
                res = json.dumps(res)
                sock.sendto(res.encode(), endereco)
                print(f"ACK {seq_num} enviado para {endereco}")
                

def calculate_checksum(data):
    return sum(data.encode()) % 256

if __name__ == "__main__":
    destinatario()
