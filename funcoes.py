import os
import pygame as p
from classes import *
from pygame.locals import *

def diretorio(nome_pasta, nome_arquivo):

    # Definindo os diretorios
    dir_principal = os.path.dirname(__file__)
    dir_sprites = os.path.join(dir_principal, 'sprites')
    dir_sons = os.path.join(dir_principal, 'sons')

    # Retornando o diretorio de acordo com os parametros
    if nome_pasta == 'sprites':
        return os.path.join(dir_sprites, nome_arquivo)
    if nome_pasta == 'sons':
        return os.path.join(dir_sons, nome_arquivo)

def inicializar():
    p.init()
    p.display.set_mode((1000, 600))
    p.display.set_caption('Jogo da cobrinha')
    p.mixer.music.load(diretorio('sons', 'musica.mp3'))
    p.mixer.music.set_volume(0.4)
    p.mixer.music.play(-1)

def desenhar_retangulo(tupla_cor, tupla_posicao, tupla_dimensoes):
    tela = p.display.get_surface()
    return p.draw.rect(tela, tupla_cor, (tupla_posicao[0], tupla_posicao[1], tupla_dimensoes[0], tupla_dimensoes[1]), 0, 5)

def atualizar_tela(relogio):
    relogio.tick(60)
    p.display.flip()

def eventos():
    for evento in p.event.get():
        if evento.type == QUIT:
            p.quit()
            exit()

def som(nome_som):
    
    # Carregando os sons
    chomp = p.mixer.Sound(diretorio('sons', 'chomp.ogg'))
    impacto = p.mixer.Sound(diretorio('sons', 'impacto.wav'))

    # Ajustando o volume dos sons
    p.mixer.Sound.set_volume(chomp, 0.6)
    p.mixer.Sound.set_volume(impacto, 0.9)

    # Tocando o som de acordo com os parametros
    if nome_som == 'chomp':
        chomp.play()
    if nome_som == 'impacto':
        impacto.play()

def desenhar_sprites(lista_objetos_Sprite):
    tela = p.display.get_surface()
    sprites = p.sprite.Group()
    for valor in lista_objetos_Sprite:
        sprites.add(valor)
    sprites.update()
    sprites.draw(tela)

def agrupar_sprites(nome_arquivo, numero_sprites):
    lista_sprites = []
    for i in range(0, numero_sprites):
        lista_sprites.append(diretorio('sprites', '{}{}.png'.format(nome_arquivo, i)))
    return lista_sprites

def desenhar(algo, tupla_posicao):
    tela = p.display.get_surface()
    tela.blit(algo, tupla_posicao)

def menu():

    # Criando o background
    background = Background(agrupar_sprites('background_menu', 9), 0.1, 9)

    # Criando um relogio para estabilizar o FPS
    relogio = p.time.Clock()

    # Loop
    loop = True
    while loop:
        atualizar_tela(relogio)
        eventos()
        desenhar_sprites([background])

        # Inicia o jogo se a tecla espaco for pressionada
        if p.key.get_pressed()[K_SPACE]:
            loop = False

    gameplay()

def gameplay():

    # Criando objetos
    cobra = Cobra(100, 100, 10, 3, K_a, K_d, K_w, K_s)
    rato = Rato(agrupar_sprites('rato', 5), 0.02, (32, 32), 1.5, (20, 30), (randint(50, 950), randint(75, 550)))

    # Criando o background
    background = p.image.load(diretorio('sprites', 'background_gameplay.jpeg')).convert_alpha()

    # Criando uma lista de objetos da classe Sprite
    lista = []
    lista.append(rato)

    # Criando um relogio para estabilizar o FPS
    relogio = p.time.Clock()

    # Pontuacao
    fonte = p.font.SysFont('consolas', 30, True, True)
    pontos = 0

    # Criando o tempo para a contagem
    tempo = 0

    # Criando uma lista de obstaculos
    obstaculos = []

    # Loop
    loop = True
    while loop:
        atualizar_tela(relogio)
        eventos()
        desenhar(background, (0, 0))
        desenhar(fonte.render('Pontuação: {}'.format(pontos), True, (0, 0, 0)), (30, 20))
        cobra.controles()
        cobra.desenhar()
        desenhar_sprites(lista)

        # Contagem para adicionar obtaculos
        tempo += 1/60
        if tempo >= 5:
            tempo = 0
            obstaculo = Obstaculo((randint(75, 925), randint(100, 525)), (50, 50), agrupar_sprites('obstaculo', 4), (32, 32), 1)
            lista.append(obstaculo)
            obstaculos.append(obstaculo)

        # Permite que os obstaculos caiam
        for obstaculo in obstaculos:
            obstaculo.cair()

        # Colisao do rato com o obstaculo
        for obstaculo in obstaculos:
            if obstaculo.hitbox.colliderect(rato.hitbox):
                lista.remove(rato)
                rato = Rato(agrupar_sprites('rato', 5), 0.02, (32, 32), 1.5, (20, 30), (randint(50, 950), randint(75, 550)))
                lista.append(rato)
                som('impacto')                

        # Colisao da cobra com o rato
        if cobra.hitbox.colliderect(rato.hitbox):
            lista.remove(rato)
            rato = Rato(agrupar_sprites('rato', 5), 0.02, (32, 32), 1.5, (20, 30), (randint(50, 950), randint(75, 550)))
            lista.append(rato)
            pontos += 1
            cobra.aumenta_velocidade()
            cobra.tam += 5
            som('chomp')

        # Colisao da cobra com o obstaculo
        for obstaculo in obstaculos:
            if cobra.hitbox.colliderect(obstaculo.hitbox):
                if obstaculo.caiu == True:
                    loop = False
            
        # Colisao da cobra com ela mesma
        if cobra.cobra.count(cobra.cabeca) > 1:
            loop = False

        # Colisao da cobra com a borda
        if cobra.cabeca[0] < 18 or cobra.cabeca[0] > 962 or cobra.cabeca[1] < 60 or cobra.cabeca[1] > 562:
            loop = False

    som('impacto')
    gameover(pontos)

def gameover(pontos):
    
    # Criando o background
    background = Background(agrupar_sprites('background_gameover', 6), 0.1, 6)

    # Criando um relogio para estabilizar o FPS
    relogio = p.time.Clock()

    # Fonte da pontuacao
    fonte = p.font.SysFont('consolas', 30, True, True)

    # Loop
    loop = True
    while loop:
        atualizar_tela(relogio)
        eventos()
        desenhar_sprites([background])
        desenhar(fonte.render('Pontuação: {}'.format(pontos), True, (0, 0, 0)), (30, 20))
    
        # Reinicia o jogo se a tecla espaco for pressionada
        if p.key.get_pressed()[K_SPACE]:
            loop = False

    gameplay()
