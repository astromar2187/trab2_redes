import random

def corromper_pacote(pacote):
    pacote_corrompido = bytearray(pacote)
    for i in range(len(pacote_corrompido)):
        pacote_corrompido[i] = random.randint(0, 255)
    return bytes(pacote_corrompido)

msg_original = "plutao nao e mais planeta!!"
pacote = msg_original.encode()
pacote_corrompido = corromper_pacote(pacote)
print(pacote_corrompido.decode('latin1'))