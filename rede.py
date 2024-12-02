import socket
import random
import time
import json 

# ISSO AQUI É A MÁQUINA B
# A MÁQUINA B É A INTERMEDIÁRIA

# Formato de mensagens:
# Dados: {'isACK': False, 'sequencia': int, 'mensagem': string, 'checksum': int}
# ACK: {'isACK': True, 'sequencia': int}

# constantes 
RED = '\033[91m'
GREEN = '\033[92m'
RESET = '\033[0m'
BLUE = '\033[94m'
YELLOW = '\033[93m'
MAGENTA = '\033[95m'

LISTEN_IP = '127.0.0.1'  # Máquina B escuta pacotes do remetente (máquina A)
LISTEN_PORT = 7070       # Porta da máquina B para escutar
REMETENTE_IP = '127.0.0.1' # Máquina A (remetente)
REMETENTE_PORT = 8080      # Porta da máquina A (remetente)
DEST_IP = '127.0.0.1'    # Máquina C (destinatário)
DEST_PORT = 9090         # Porta da máquina C (destinatário)
TAXA_PERDA = 0.1         # Taxa de perda de pacotes. Perda significa decarte, não retransmissão, desconexão, etc. Significa que o pacote não será enviado.
TAXA_ERRO = 0.2          # Taxa de erro de checksum. Erro de checksum significa que o pacote terá seus dados corrompidos, mas será enviado mesmo assim.
TAXA_ATRASO = 0.2        # Taxa de atraso de pacotes. Atraso significa que o pacote será enviado, mas com um atraso. O atraso é aleatório entre 0 e 2 segundos.
ATRASO_MAX = 10           # Tempo máximo de atraso de pacotes

# global
pkt_perdidos = 0
pkt_corrompidos = 0
pkt_atrasados = 0
pkt_normal = 0
totalpkg = 10
timeout = 2

def incrementar_contador(contador):
    if contador == 'pkt_perdidos':
        global pkt_perdidos
        pkt_perdidos += 1

    elif contador == 'pkt_corrompidos':
        global pkt_corrompidos
        pkt_corrompidos += 1

    elif contador == 'pkt_atrasados':
        global pkt_atrasados
        pkt_atrasados += 1

    elif contador == 'pkt_normal':
        global pkt_normal
        pkt_normal += 1

def atraso(): # Atrasa o pacote entre 0 e ATRASO_MAX segundos
    tempo_atraso = random.uniform(0, ATRASO_MAX)
    print(f"{tempo_atraso} segundos")
    time.sleep(tempo_atraso)
    return tempo_atraso

def corromper_pacote(pacote): # Corrompe o pacote trocando os bytes por valores aleatórios
    pacote = json.loads(pacote.decode())  # Decodifica os bytes e converte de volta para dicionário
    seq_num = pacote['sequencia']
    is_ack = pacote['isACK'] # Verifica se o pacote é um ACK, toda mensagem tem que ter esse campo
    checksum = pacote['checksum']

    if is_ack:
        if seq_num == 0:
            pacote_corrompido = json.dumps({'isACK': is_ack, 'sequencia': 1, 'checksum': checksum})
        else:
            pacote_corrompido = json.dumps({'isACK': is_ack, 'sequencia': 0, 'checksum': checksum})
    else:
        pacote_corrompido = json.dumps({'isACK': is_ack, 'sequencia': seq_num, 'mensagem': "dados corrompidos!", 'checksum': checksum})
    return pacote_corrompido.encode()

def iniciar_sockets():
    sock_in = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sock_in.bind((LISTEN_IP, LISTEN_PORT))
    print(f"REDE escutando em {LISTEN_IP}:{LISTEN_PORT}...")
    sock_out = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    print(f"REDE pronta para receber e enviar pacotes...")
    return sock_in, sock_out

def processar_pacote_aut(sock_out, pacote, endereco_origem, endereco_destino): # função que define o que acontecerá com o pacote recebido
    print()
    print(f"REDE recebeu: {pacote.decode()} de {endereco_origem}")

    if random.random() < TAXA_PERDA: # Se for perdido, o pacote não é enviado.
        print(RED, "REDE: pacote perdido!", RESET)
        
        incrementar_contador('pkt_perdidos')
        return 0

    elif random.random() < TAXA_ERRO:  #Se for corrompido, o pacote é enviado mesmo assim.
        # corrupção do pacote
        pacote_corrompido = corromper_pacote(pacote)
        print(RED, "REDE: pacote corrompido!", RESET)
        # envia o pacote corrompido
        enviar_pacote(sock_out, pacote_corrompido, endereco_destino)
        print(BLUE, "REDE: pacote corrompido enviado!", RESET)

        incrementar_contador('pkt_corrompidos')
        return 1

    elif random.random() < TAXA_ATRASO: # Se for atrasado, o pacote é enviado com atraso.
        print(RED, "REDE: atraso no envio do pacote. Tempo de atraso: ", RESET, end='')
        atraso()
        enviar_pacote(sock_out, pacote, endereco_destino)
        print(BLUE, "REDE: pacote enviado com atraso!", RESET)

        incrementar_contador('pkt_atrasados')
        return 2

    else:
        # Se não for perdido, corrompido ou atrasado, o pacote é enviado normalmente.
        enviar_pacote(sock_out, pacote, endereco_destino)
        print(GREEN, "REDE: pacote enviado normalmente!", RESET)

        incrementar_contador('pkt_normal')
        return 3


    #tempo_inicial = time.time()

def enviar_pacote(sock_out, pacote, endereco_destino):
    sock_out.sendto(pacote, endereco_destino)
    print(f"REDE enviou: {pacote.decode('latin1')} para {endereco_destino}")

def fechar_sockets(sock_in, sock_out):
    sock_in.close()
    sock_out.close()
    print("REDE: conexão encerrada.")

def menu_inicial():
    print("Selecione o modo de operação:")
    print("1 - Modo manual")
    print("2 - Modo automático")
    print("3 - Sair")
    opcao = input("Opção: ")
    while opcao not in ['1', '2', '3']:
        print("Opção inválida! Tente novamente.")
        opcao = menu_inicial()
    return opcao

def menu_manual():
    print("Selecione uma opção: ")
    print("1 - Enviar pacote")
    print("2 - Descartar pacote")
    print("3 - Corromper pacote")
    print("4 - Atrasar pacote (Tempo aleatório entre 0 e 3 segundos)")
    print("5 - Atrasar pacote (Tempo customizado)")
    print("6 - Sair")
    opcao = input("Opção: ")
    while opcao not in ['1', '2', '3', '4', '5', '6']:
        print("Opção inválida! Tente novamente.")
        opcao = menu_manual()
    return opcao

def modo_manual():
    print("\nModo manual iniciado...")
    tempoizador = True
    sock_in, sock_out = iniciar_sockets()

    while True:
        pacote, endereco_origem, endereco_destino = receber_pacote(sock_in)
        print(f"REDE recebeu: {pacote.decode()} de {endereco_origem}")
        print("Pacote recebido! O que deseja fazer com ele?")
        print()

        opcao = menu_manual()

        if opcao == '1':  # Enviar pacote normalmente
            tempoizador = True  # Marcar como positivo para indicar sucesso
            enviar_pacote(sock_out, pacote, endereco_destino)
            

        elif opcao == '2':  # Descartar pacote, não enviar ack
            tempoizador = True
            print("Pacote descartado!")
            #valor_ack = False  # Marcar como negativo para indicar perda

            #seq = random.randint(0, 1)
            # Atualizar ACK com o valor atual de valor_ack
            #ack = {'isACK': True, 'sequencia': seq, 'ERROR': 'Pacote descartado!'}
            #ack = json.dumps(ack).encode()

            # Enviar ACK de volta ao remetente
            sock_out.sendto(ack, endereco_origem)
            print(f"REDE enviou ACK atualizado: {ack.decode()} para {endereco_origem}")
            print('recebendo pacote novamente...')
            continue  # Voltar ao início do loop sem enviar o pacote pro dest

        elif opcao == '3':  # Corromper pacote
            tempoizador = True       
            pacote_corrompido = corromper_pacote(pacote)
            enviar_pacote(sock_out, pacote_corrompido, endereco_destino)
            print(f"REDE enviou pacote corrompido para {endereco_destino}")
            print('recebendo pacote novamente...')

        elif opcao == '4':  # Atrasar pacote por tempo aleatório
            tempo_atraso = atraso()

            if tempo_atraso > timeout:
                tempoizador = False  # Marcar como negativo se ultrapassar timeout

            print(f"Atrasando pacote por {tempo_atraso:.2f} segundos...")
            time.sleep(tempo_atraso)
            enviar_pacote(sock_out, pacote, endereco_destino)
            


        elif opcao == '5':  # Atrasar pacote por tempo customizado
            endereco_destino = (DEST_IP, DEST_PORT)
            tempo_atraso = float(input("Digite o tempo de atraso em segundos: "))

            if tempo_atraso > timeout:
                tempoizador = False

            print(f"Atrasando pacote por {tempo_atraso:.2f} segundos...")
            time.sleep(tempo_atraso)
            enviar_pacote(sock_out, pacote, endereco_destino)

        elif opcao == '6':  # Sair
            print("Encerrando conexão...")
            fechar_sockets(sock_in, sock_out)
            print("Fim do programa.")
            break

        # Receber ACK do destinatário
    
        ack, endereco_destino = sock_in.recvfrom(1024)
        print(f"REDE recebeu ACK: {ack.decode()} de {endereco_destino}")
        if tempoizador == False:
            ack = json.loads(ack.decode())
            ack['ERROR'] = 'Timeout excedido!'
            ack = json.dumps(ack).encode()

        # Enviar ACK de volta ao remetente
        sock_out.sendto(ack, endereco_origem)
        print(f"REDE enviou ACK atualizado: {ack.decode()} para {endereco_origem}")
        if tempoizador == False:
            print('recebendo pacote novamente...')
            

def receber_pacote(sock_in):
    pacote, endereco_origem = sock_in.recvfrom(1024)

    if endereco_origem[0] == REMETENTE_IP and endereco_origem[1] == REMETENTE_PORT:
        endereco_destino = (DEST_IP, DEST_PORT)
    else:

        endereco_destino = (REMETENTE_IP, REMETENTE_PORT)

    return pacote, endereco_origem, endereco_destino

def calculate_checksum(data):
    return sum(data.encode()) % 256

def modo_automatico():
    print()
    print("Modo automático iniciado...")
    sock_in, sock_out = iniciar_sockets()

    for i in range(totalpkg):
        pacote, endereco_origem, endereco_destino = receber_pacote(sock_in)
        pacote_decod = json.loads(pacote.decode())
        seq = pacote_decod['sequencia']

        if pacote_decod['sequencia'] == -1: # Verifica se é o pacote de finalização
            break
        else:
            pacote = json.dumps(pacote_decod).encode()
            returned = processar_pacote_aut(sock_out, pacote, endereco_origem, endereco_destino)

            if returned == 0: # Se o pacote foi perdido, não envia ack
                continue
            elif returned == 1: # Se o pacote foi corrompido, envia ack corrompido
                if seq == 1:
                    seq = 0
                else:
                    seq = 1
            elif returned == 2: # Se o pacote foi atrasado, envia atrasado
                pass
            res = {'isACK': True, 'sequencia': seq} # Cria o ACK falso
            res = json.dumps(res).encode()
            enviar_pacote(sock_out, res, (REMETENTE_IP, REMETENTE_PORT)) # Envia o ACK falso

    fechar_sockets(sock_in, sock_out)
    relatorio_final()

def relatorio_final():
    print()
    print("---------- RELATÓRIO FINAL ----------")
    print(f"Total de pacotes recebidos: {pkt_perdidos + pkt_corrompidos + pkt_atrasados + pkt_normal}")
    print(f"Pacotes " + RED + "perdidos" + RESET + f": {pkt_perdidos}")
    print(f"Pacotes " + BLUE + "corrompidos" + RESET + f": {pkt_corrompidos}")
    print(f"Pacotes " + BLUE + "atrasados" + RESET + f": {pkt_atrasados}")
    print(f"Pacotes " + GREEN + "enviados normalmente" + RESET + f": {pkt_normal}")
    print("---------------------- FIM ----------------------")


if __name__ == "__main__":
    print(YELLOW, "----------------------------------------------", RESET)
    print(MAGENTA, "BEM-VINDO AO PROGRAMA DE SIMULAÇÃO DE RDT 3.0", RESET)
    print(YELLOW, "----------------------------------------------", RESET)
    print("Este programa simula o envio de pacotes entre um remetente e um destinatário, \ncom a presença de uma máquina intermediária controlando envios, perdas, corrupções e atrasos de pacotes.")
    print("Essa simulação pode ser feita de forma manual ou automática.")
    print()
    print(BLUE, "MODO MANUAL", RESET)
    print("No modo manual, você pode escolher o que fazer com cada pacote recebido. Ao receber um pacote, selecione uma opção \npara definir o que acontecerá com ele. O pacote será enviado (ou não) para o destinatário após a sua escolha e \nnenhum temporizador será iniciado até uma escolha ser feita.")
    print()
    print(GREEN, "MODO AUTOMÁTICO", RESET)
    print("No modo automático, os pacotes são enviados automaticamente entre remetente e destinatário. A máquina intermediária \ncontrola o envio, perdas, corrupções e atrasos de pacotes baseado em probabilidade pré-definidas e que podem ser \nconfiguradas no código-fonte.")
    print()
    print("Independente da escolha, ao final da simulação, um relatório será gerado com a quantidade de pacotes enviados, \nperdidos, corrompidos e atrasados.")
    print()
    print(f"{YELLOW}Vamos começar!{RESET}")
    opcao = menu_inicial()
    if opcao == '1':
        modo_manual()
    elif opcao == '2':
        modo_automatico()
    elif opcao == '3':
        print("Fim do programa.")
        exit()
