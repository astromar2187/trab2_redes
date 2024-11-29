# trab2_redes
RDT-3.0 com simulação de interferência da rede (perda e descarte de pacotes, atrasos e retransmissões)

## Modos de execução
Esse programa permite dois modos de simulação de protocolo RDT 3.0: manual e automático. No modo manual o usuário de 'rede.py' pode selecionar o que acontece com cada pacote que chega a rede, incluindo dados e acks. Nesse modo, as perdas, corrupções e atrasos de pacotes são definidas pelo usuário, que poderá observar o comportamento do protocolo para cada situação desejada.
Já o modo automático não requer nenhuma interação do usuário, pois define perdas, corrupções e atrasos com base em probabilidades pré-definidas. 

### Constantes do Modo automático
- TAXA_PERDA: Indica a probabilidade da rede perder um pacote. Aqui, perda pode significar decarte, não retransmissão, desconexão, etc. Perda implica que o pacote não será enviado.
- TAXA_ERRO: Indica a probabilidade de um pacote ter seus bits alterados. Caso aconteça, significa que o pacote terá seus dados corrompidos, mas será enviado mesmo assim.
- TAXA_ATRASO:  Indica a probabilidade de um pacote ser eviado com atraso pela rede. Aqui, simulamos os diversos tipos de atraso que podem acontecer, como atraso de processamento, transmissão, fila, e propagação. Esse caso significa que o pacote será enviado, mas com um atraso. O tempo de atraso é definido aleatoriamente entre 0 e TIMEOUT+1 segundos para cada pacote, ou seja, alguns pacotes podem ser enviados com atraso maior que o estouro de temporizador do remetente.


