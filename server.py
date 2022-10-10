from copyreg import pickle
import pickle
import socket
import numpy as np

NUMERO_JOGADORES = 2
LINHAS_TABULEIRO = 15
COLUNAS_TABULEIRO = 15

ip = ''
porta = 5000
soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soquete.bind((ip, porta))
soquete.listen(NUMERO_JOGADORES)

tabuleiro = np.zeros((LINHAS_TABULEIRO, COLUNAS_TABULEIRO))

clientes = []
jogadores = [1, 2]
jogador_atual = 1

def checa_tabuleiro_cheio():
    for linha in range(LINHAS_TABULEIRO):
        for coluna in range(COLUNAS_TABULEIRO):
            if tabuleiro[linha][coluna] == 0:
                return False

    return True

def checa_ganhador(jogador):
    for linha in range(LINHAS_TABULEIRO):
        for coluna in range(COLUNAS_TABULEIRO):
            if tabuleiro[linha][coluna] != 0:

                #verifica horizontais
                if (coluna <= 10):
                    if tabuleiro[linha][coluna] == tabuleiro[linha][coluna+1] and tabuleiro[linha][coluna] == tabuleiro[linha][coluna+2] and tabuleiro[linha][coluna] == tabuleiro[linha][coluna+3] and tabuleiro[linha][coluna] == tabuleiro[linha][coluna+4]:
                        return (True, linha, coluna, tabuleiro[linha][coluna], 'horizontal')
                
                #verifica verticais
                if (linha <= 10):
                    if tabuleiro[linha][coluna] == tabuleiro[linha+1][coluna] and tabuleiro[linha][coluna] == tabuleiro[linha+2][coluna] and tabuleiro[linha][coluna] == tabuleiro[linha+3][coluna] and tabuleiro[linha][coluna] == tabuleiro[linha+4][coluna]:
                        return (True, linha, coluna, tabuleiro[linha][coluna], 'vertical')

                #verifica diagonais desc
                if (coluna <= 10 and linha <= 10):
                    if tabuleiro[linha][coluna] == tabuleiro[linha+1][coluna+1] and tabuleiro[linha][coluna] == tabuleiro[linha+2][coluna+2] and tabuleiro[linha][coluna] == tabuleiro[linha+3][coluna+3] and tabuleiro[linha][coluna] == tabuleiro[linha+4][coluna+4]:
                        return (True, linha, coluna, tabuleiro[linha][coluna], 'diag_desc')

                #verifica diagonais asc
                if (coluna >= 4 and linha <= 10):
                    if tabuleiro[linha][coluna] == tabuleiro[linha+1][coluna-1] and tabuleiro[linha][coluna] == tabuleiro[linha+2][coluna-2] and tabuleiro[linha][coluna] == tabuleiro[linha+3][coluna-3] and tabuleiro[linha][coluna] == tabuleiro[linha+4][coluna-4]:
                        return (True, linha, coluna, tabuleiro[linha][coluna], 'diag_asc')

    return (False, 0, 0, 0, '')

for i in range(NUMERO_JOGADORES):
    c, cliente = soquete.accept()
    clientes.append(c)
    dados = clientes[i].recv(4096).decode()
    print('%s' % dados)


for i in range(NUMERO_JOGADORES):
    dados = pickle.dumps(jogadores[i])
    clientes[i].send(dados)

while True:

    dados = clientes[jogador_atual - 1].recv(4096)
    (linha, coluna, jogador) = pickle.loads(dados)
    print((linha, coluna))

    tabuleiro[linha][coluna] = jogador

    game_over = checa_ganhador(jogador)
    tabuleiro_cheio = checa_tabuleiro_cheio()

    dados = pickle.dumps((tabuleiro, game_over, tabuleiro_cheio))
    clientes[jogador_atual % 2].send(dados)
    clientes[jogador_atual - 1].send(dados)

    jogador_atual = jogador_atual % 2 + 1