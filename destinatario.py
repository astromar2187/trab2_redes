import socket
import json 

# ISSO É MÁQUINA A

LISTEN_IP = '127.0.0.1'
LISTEN_PORT = 9090
SERVER_IP = '127.0.0.1'  # IP da máquina intermediária
SERVER_PORT = 7070       # Porta da máquina intermediária

def destinatario():
    expected_seq_num = 0
    num_seq_anterior = 1
    m = 'Sucesso'
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock:
        sock.bind((LISTEN_IP, LISTEN_PORT))
        print(f"Destinatário escutando em {LISTEN_IP}:{LISTEN_PORT}...")

        while True:
            pacote, endereco = sock.recvfrom(1024)
            pacote = json.loads(pacote.decode())  # Decodifica os bytes e converte de volta para dicionário
            
            print(f"Destinatário recebeu: {pacote}")
            seq_num = pacote['sequencia']
            mensagem = pacote['mensagem']
            valor_checksum = pacote['checksum']

            checksum_calculado = calculate_checksum(f"{expected_seq_num}:{mensagem}")

            # Verifica se o checksum está correto
            if valor_checksum == checksum_calculado:
                print(f"Checksum correto! Mensagem: '{mensagem}' com checksum {checksum_calculado}")

                if seq_num == expected_seq_num:
                    print(f"Número de sequência correto! Mensagem: '{mensagem}'")

                    # tem uma forma de deixar esses ifs mais simplificados, mas deixei assim pra ter uma visualizacao melhor
                    if pacote['timeout']:
                        if expected_seq_num == 0 and num_seq_anterior == 1:
                            expected_seq_num = 1
                            num_seq_anterior = 0
                        elif expected_seq_num == 1 and num_seq_anterior == 0:
                            expected_seq_num = 0
                            num_seq_anterior = 1
                        else:  
                            print("Erro na sequência de pacotes")
                            ack = json.dumps({'isACK': True, 'sequencia': seq_num, 'ERROR': 'sequencia de pacotes errada!'}) 
                            sock.sendto(ack.encode(), (SERVER_IP, SERVER_PORT))
                            print(f"Enviado: {ack}")
                            m = 'Erro de timeout! enviado ack novamente...'                
                
                # Envia ACK
                ack = json.dumps({'isACK': True, 'sequencia': seq_num, 'ERROR': 'Sucesso'}) 
                sock.sendto(ack.encode(), (SERVER_IP, SERVER_PORT))
                print(f"Enviado: {ack}")
            else:
                print(f"Erro no checksum! Mensagem: '{mensagem}' com checksum {checksum_calculado}")
                # nao mandar ack e esperar o remetente reenviar
                continue
            
            # Verifica se o número de sequência está correto
            if seq_num == num_seq_anterior:
                    print("Erro na sequência de pacotes")
                    # nao envia ack e espera o remetente reenviar
                    break  
                ack = json.dumps({'isACK': True, 'sequencia': seq_num, 'ERROR': 'checksum invalido! mensagem corrompida'}) 
                sock.sendto(ack.encode(), (SERVER_IP, SERVER_PORT))
                print(f"Enviado: {ack}")

               

def calculate_checksum(data):
    return sum(data.encode()) % 256

if __name__ == "__main__":
    destinatario()
