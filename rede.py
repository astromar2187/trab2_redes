import socket
import random
import time
import json 

# ISSO AQUI É A MÁQUINA B
# A MÁQUINA B É A INTERMEDIÁRIA

# constantes 
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BLUE = '\033[94m'

LISTEN_IP = '127.0.0.1'  # Máquina B escuta pacotes do remetente (máquina A)
LISTEN_PORT = 7070       # Porta da máquina B para escutar
REMETENTE_IP = '127.0.0.1' # Máquina A (remetente)
REMETENTE_PORT = 8080      # Porta da máquina A (remetente)
DEST_IP = '127.0.0.1'    # Máquina C (destinatário)
DEST_PORT = 9090         # Porta da máquina C (destinatário)
TAXA_PERDA = 0.1         # Taxa de perda de pacotes. Perda significa decarte, não retransmissão, desconexão, etc. Significa que o pacote não será enviado.
TAXA_ERRO = 0.5          # Taxa de erro de checksum. Erro de checksum significa que o pacote terá seus dados corrompidos, mas será enviado mesmo assim.
TAXA_ATRASO = 0.5        # Taxa de atraso de pacotes. Atraso significa que o pacote será enviado, mas com um atraso. O atraso é aleatório entre 0 e 2 segundos.

# global
__pkt_perdidos = 0
__pkt_corrompidos = 0
__pkt_atrasados = 0
__pkt_normal = 0

def atraso(): # Atrasa o pacote entre 0 e 3 segundos
    tempo_atraso = random.uniform(0, 3)
    print(f"{tempo_atraso} segundos")
    time.sleep(tempo_atraso)

def corromper_pacote(pacote): # Corrompe o pacote trocando os bytes por valores aleatórios
    pacote = json.loads(pacote.decode())  # Decodifica os bytes e converte de volta para dicionário
    seq_num = pacote['sequencia']

    pacote_corrompido = json.dumps({'sequencia': seq_num, 'mensagem': "dados corrompidos!", 'checksum': -1})
    return pacote_corrompido.encode()

def iniciar_sockets():
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((LISTEN_IP, LISTEN_PORT))
    print(f"REDE escutando em {LISTEN_IP}:{LISTEN_PORT}...")
    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"REDE pronta para enviar pacotes...")
    return sock_in, sock_out

def processar_pacote_aut(sock_out, pacote, endereco_origem, endereco_destino): # função que define o que acontecerá com o pacote recebido
    print()
    print(f"REDE recebeu: {pacote.decode()} de {endereco_origem}")

    if random.random() < TAXA_PERDA: # Se for perdido, o pacote não é enviado.
        print(RED, "REDE: pacote perdido!", RESET)

        # contagem
        global __pkt_perdidos
        __pkt_perdidos += 1
        return

    elif random.random() < TAXA_ERRO:  #Se for corrompido, o pacote é enviado mesmo assim.
        # corrupção do pacote
        pacote_corrompido = corromper_pacote(pacote)
        print(RED, "REDE: pacote corrompido!", RESET)
        # envia o pacote corrompido
        enviar_pacote(sock_out, pacote_corrompido, endereco_destino)
        print(BLUE, "REDE: pacote corrompido enviado!", RESET)

        # contagem
        global __pkt_corrompidos
        __pkt_corrompidos += 1
        return

    elif random.random() < TAXA_ATRASO: # Se for atrasado, o pacote é enviado com atraso.
        print(RED, "REDE: atraso no envio do pacote. Tempo de atraso: ", RESET, end='')
        atraso()
        enviar_pacote(sock_out, pacote, endereco_destino)
        print(BLUE, "REDE: pacote enviado com atraso!", RESET)

        # contagem
        global __pkt_atrasados
        __pkt_atrasados += 1
        return

    else:
        # Se não for perdido, corrompido ou atrasado, o pacote é enviado normalmente.
        enviar_pacote(sock_out, pacote, endereco_destino)
        print(GREEN, "REDE: pacote enviado normalmente!", RESET)

        # contagem
        global __pkt_normal
        __pkt_normal += 1
        return


    #tempo_inicial = time.time()


def enviar_pacote(sock_out, pacote, endereco_destino):
    sock_out.sendto(pacote, endereco_destino)
    print(f"REDE enviou: {pacote.decode('latin1')} para {endereco_destino}")


def fechar_sockets(sock_in, sock_out):
    sock_in.close()
    sock_out.close()
    print("REDE: conexão encerrada.")


def modo_manual():
    pass

def modo_automatico():
    sock_in, sock_out = iniciar_sockets()
    for i in range(20):
        pacote, endereco_origem = sock_in.recvfrom(1024)

        if endereco_origem[0] == REMETENTE_IP and endereco_origem[1] == REMETENTE_PORT:
            endereco_destino = (DEST_IP, DEST_PORT)
        else:
            endereco_destino = (REMETENTE_IP, REMETENTE_PORT)

        processar_pacote_aut(sock_out, pacote, endereco_origem, endereco_destino)

    fechar_sockets(sock_in, sock_out)
    print()
    print("---------- RELATÓRIO FINAL ----------")
    print(f"Total de pacotes recebidos: {__pkt_perdidos + __pkt_corrompidos + __pkt_atrasados + __pkt_normal}")
    print(f"Pacotes " + RED + "perdidos" + RESET + f": {__pkt_perdidos}")
    print(f"Pacotes " + BLUE + "corrompidos" + RESET + f": {__pkt_corrompidos}")
    print(f"Pacotes " + BLUE + "atrasados" + RESET + f": {__pkt_atrasados}")
    print(f"Pacotes " + GREEN + "enviados normalmente" + RESET + f": {__pkt_normal}")

    '''with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as sock_in:
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
                print(f"Máquina B repassou ACK para {endereco_remetente}")'''

if __name__ == "__main__":
    modo_automatico()
