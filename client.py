import sys
import socket
import pygame
import numpy as np
import pickle

#constantes
##tabuleiro
COMPRIMENTO = 600
ALTURA = 700
LINHAS_TABULEIRO = 15
COLUNAS_TABULEIRO = 15
TAMANHO_CASA = 40

##design
ESPESSURA_LINHA_TABULEIRO = 1
ESPESSURA_LINHA_VENCEDOR = 3
COR_FUNDO = (237, 203, 131)
COR_LINHA = (115, 77, 15)

#inicilização do socket
if len(sys.argv) != 3:
    print('%s <ip> <porta>' % sys.argv[0])

ip = sys.argv[1]
porta = int(sys.argv[2])

soquete = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

soquete.connect((ip, porta))

soquete.send('Cliente conectado.'.encode())

pygame.init()

#inicialização do pygame
tela = pygame.display.set_mode((COMPRIMENTO, ALTURA))
pygame.display.set_caption('Gomoku')

fonte = pygame.font.SysFont('Consolas', 20, True)
img_player1 = pygame.image.load("img/player1.png")
img_player2 = pygame.image.load("img/player2.png")

#inicialização do tabuleiro local
tabuleiro = np.zeros((LINHAS_TABULEIRO, COLUNAS_TABULEIRO))

#recebe jogador do servidor
dados = soquete.recv(4096)
jogador = pickle.loads(dados)
print('Sou o jogador ' + str(jogador))

#define qual jogador começa
vez_jogador = 1
game_over = False
tabuleiro_cheio = False

#verifica se a posição é valida para jogada
def posicao_disponivel(tabuleiro, linha, coluna):
    return tabuleiro[linha][coluna] == 0

def desenha_linha_vertical_ganhador(linha, coluna):
    posY = linha * TAMANHO_CASA
    posX = coluna * TAMANHO_CASA + TAMANHO_CASA / 2
    pygame.draw.line(tela, (0, 0, 0), (posX, posY), (posX, posY + TAMANHO_CASA * 5), ESPESSURA_LINHA_VENCEDOR)

def desenha_linha_horizontal_ganhador(linha, coluna):
    posY = linha * TAMANHO_CASA + TAMANHO_CASA / 2
    posX = coluna * TAMANHO_CASA
    pygame.draw.line(tela, (0, 0, 0), (posX, posY), (posX + TAMANHO_CASA * 5, posY), ESPESSURA_LINHA_VENCEDOR)

def desenha_linha_ascdiagonal_ganhador(linha, coluna):
    posY = linha * TAMANHO_CASA
    posX = coluna * TAMANHO_CASA + TAMANHO_CASA
    pygame.draw.line(tela, (0, 0, 0), (posX, posY), (posX - TAMANHO_CASA * 5, posY + TAMANHO_CASA * 5), ESPESSURA_LINHA_VENCEDOR)

def desenha_linha_descdiagonal_ganhador(linha, coluna):
    posY = linha * TAMANHO_CASA
    posX = coluna * TAMANHO_CASA
    pygame.draw.line(tela, (0, 0, 0), (posX, posY), (posX + TAMANHO_CASA * 5, posY + TAMANHO_CASA * 5), ESPESSURA_LINHA_VENCEDOR)

def atualiza_tela(jogador):

    tela.fill(COR_FUNDO)

    #escreve player
    texto = fonte.render('Player ' + str(jogador), True, (0, 0, 0))
    posicao_texto = texto.get_rect(center=(65, 600))
    tela.blit(texto, posicao_texto)

    #escreve turno
    if (jogador != vez_jogador):
        texto = fonte.render('Aguardando jogada do oponente', True, (0, 0, 0))
        posicao_texto = texto.get_rect(center=(420, 600))
        tela.blit(texto, posicao_texto)
    else:
        texto = fonte.render('Sua vez', True, (0, 0, 0))
        posicao_texto = texto.get_rect(center=(540, 600))
        tela.blit(texto, posicao_texto)

    #desenha linhas
    #desenha linhas horizontais
    for posicao in range(TAMANHO_CASA, COMPRIMENTO + 1, TAMANHO_CASA):
        pygame.draw.line(tela, COR_LINHA, (0 + TAMANHO_CASA / 2, posicao - TAMANHO_CASA / 2), (COMPRIMENTO - TAMANHO_CASA / 2, posicao - TAMANHO_CASA / 2), ESPESSURA_LINHA_TABULEIRO)
    #desenha lihhas verticais
        pygame.draw.line(tela, COR_LINHA, (posicao - TAMANHO_CASA / 2, 0 + TAMANHO_CASA / 2), (posicao - TAMANHO_CASA / 2, ALTURA - 100 - TAMANHO_CASA / 2), ESPESSURA_LINHA_TABULEIRO)

    #desenha jogador
    for linha in range(LINHAS_TABULEIRO):
        for coluna in range(COLUNAS_TABULEIRO):
            if tabuleiro[linha][coluna] == 1:
                tela.blit(img_player1, (int(coluna * TAMANHO_CASA + 4),int(linha * TAMANHO_CASA) + 4))
                
            elif tabuleiro[linha][coluna] == 2:
                tela.blit(img_player2, (int(coluna * TAMANHO_CASA + 4),int(linha * TAMANHO_CASA) + 4))

def fim_jogo(vencedor, linha, coluna, tabuleiro_cheio):

    if tabuleiro_cheio:
        texto = fonte.render('Empate', True, (0, 0, 0))
        posicao_texto = texto.get_rect(center=(COMPRIMENTO/2, 650))
        tela.blit(texto, posicao_texto)
    else:
        if orientacao == 'horizontal':
            desenha_linha_horizontal_ganhador(linha, coluna)
        elif orientacao == 'vertical':
            desenha_linha_vertical_ganhador(linha, coluna)
        elif orientacao == 'diag_desc':
            desenha_linha_descdiagonal_ganhador(linha, coluna)
        elif orientacao == 'diag.asc':
            desenha_linha_ascdiagonal_ganhador(linha, coluna)

        texto = fonte.render('Player ' + str(int(vencedor)) + ' ganhou!', True, (0, 0, 0))
        posicao_texto = texto.get_rect(center=(COMPRIMENTO/2, 650))
        tela.blit(texto, posicao_texto)

def envia_coordenadas():
    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            soquete.close()
            sys.exit()

        if event.type == pygame.MOUSEBUTTONDOWN:

            mouseX = event.pos[0]
            mouseY = event.pos[1]
                                    
            linha_clicada = int(mouseY // TAMANHO_CASA)
            coluna_clicada = int(mouseX // TAMANHO_CASA)

            if (linha_clicada < 15 and coluna_clicada < 15 and posicao_disponivel(tabuleiro, linha_clicada, coluna_clicada)):

                print('Enviando coordenadas...')
                dados = pickle.dumps((linha_clicada,coluna_clicada, jogador))
                soquete.send(dados)

                return True
    return False

while True:

    atualiza_tela(jogador)

    if game_over or tabuleiro_cheio:
        fim_jogo(vencedor, linha, coluna, tabuleiro_cheio)

    pygame.display.update()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            soquete.close()
            sys.exit()

    if not game_over:
        
        if vez_jogador == jogador:
            while True:
                if envia_coordenadas():
                    dados = soquete.recv(4096)
                    (tabuleiro, (game_over, linha, coluna, vencedor, orientacao), tabuleiro_cheio) = pickle.loads(dados)
                    print((game_over, linha, coluna, vencedor, orientacao), tabuleiro_cheio)
                    break
        
        else:
            try:
                soquete.setblocking(False)
                dados = soquete.recv(4096)
                (tabuleiro, (game_over, linha, coluna, vencedor, orientacao), tabuleiro_cheio) = pickle.loads(dados)
                print((game_over, linha, coluna, vencedor, orientacao), tabuleiro_cheio)
                soquete.setblocking(True)
            except:
                continue

        vez_jogador = vez_jogador % 2 + 1