import pygame as p
import funcoes as f
from pygame.sprite import Sprite
from random import randint

class Cobra:

    def __init__(self, posicao_inicial_x, posicao_inicial_y, tamanho_inicial, velocidade_inicial, tecla_esquerda, tecla_direita, tecla_cima, tecla_baixo):

        # Atribuindo parametros
        self.pos_x = posicao_inicial_x
        self.pos_y = posicao_inicial_y
        self.tam = tamanho_inicial
        self.vel = velocidade_inicial
        self.esquerda = tecla_esquerda
        self.direita = tecla_direita
        self.cima = tecla_cima
        self.baixo = tecla_baixo

        # Atributos
        self.cobra = []
        self.cabeca = []
        self.movimento_x = self.vel
        self.movimento_y = 0
        self.hitbox = '[INDEFINIDO]'

    def controles(self):
        self.pos_x += self.movimento_x
        self.pos_y -= self.movimento_y
        if p.key.get_pressed()[self.esquerda] and self.movimento_x != self.vel:
            self.movimento_x = -self.vel
            self.movimento_y = 0
        if p.key.get_pressed()[self.direita] and self.movimento_x != -self.vel:
            self.movimento_x = self.vel
            self.movimento_y = 0
        if p.key.get_pressed()[self.baixo] and self.movimento_y != self.vel:
            self.movimento_y = -self.vel
            self.movimento_x = 0
        if p.key.get_pressed()[self.cima] and self.movimento_y != -self.vel:
            self.movimento_y = self.vel
            self.movimento_x = 0

    def desenhar(self):

        # Movimentando a cobra
        self.cabeca.clear()
        self.cabeca.append(self.pos_x)  
        self.cabeca.append(self.pos_y)
        self.cobra.append(self.cabeca[:])
        if len(self.cobra) > self.tam:
            del self.cobra[0]

        # Desenhando a cobra
        for parte in self.cobra:
            f.desenhar_retangulo((185, 152, 20), parte, (20, 20))

        # Movimentando a hitbox
        self.hitbox = f.desenhar_retangulo((185, 152, 20), self.cabeca, (20, 20))

    def aumenta_velocidade(self):
        if self.movimento_x == - self.vel:
            self.vel += 0.1
            self.movimento_x = -self.vel
            self.movimento_y = 0
        else:
            if self.movimento_x == self.vel:
                self.vel += 0.1
                self.movimento_x = self.vel
                self.movimento_y = 0
            else:
                if self.movimento_y == -self.vel:
                    self.vel += 0.1
                    self.movimento_x = 0
                    self.movimento_y = -self.vel
                else:
                    self.vel += 0.1
                    self.movimento_x = 0
                    self.movimento_y = self.vel


class Rato(Sprite):

    def __init__(self, lista_sprites_diretorio, velocidade_animacao, tupla_dimensoes_sprites, tamanho_imagem, tupla_dimensoes_hitbox, tupla_posicao):
        
        # Herdando a classe mae
        Sprite.__init__(self)

        # Atribuindo parametros
        self.lista = lista_sprites_diretorio
        self.vel = velocidade_animacao
        self.dim_sprites = tupla_dimensoes_sprites
        self.tam = tamanho_imagem
        self.dim = tupla_dimensoes_hitbox
        self.pos = tupla_posicao

        # Atributos
        self.animacao = randint(0, 3)
        self.sprite_atual = 0
        self.hitbox = f.desenhar_retangulo((214, 28, 28), self.pos, self.dim)
        self.sprites = []

        # Carregando os sprites
        for valor in self.lista:
            self.sprites.append(p.image.load(valor))

        # Criando a imagem
        self.image = self.sprites[self.sprite_atual]

        # Criando um retangulo para posicionar a imagem
        self.rect = self.image.get_rect()
        self.rect.center = (self.pos[0], self.pos[1])

    def update(self):

        # Animacao 1
        if self.animacao == 0:
            self.sprite_atual += self.vel
            if self.sprite_atual >= 3:
                self.sprite_atual = 0
            self.image = self.sprites[int(self.sprite_atual)]
        else:

            # Animacao 2
            if self.animacao == 1:
                self.sprite_atual += self.vel
                if self.sprite_atual >= 1 and self.sprite_atual < 2:
                    self.sprite_atual = 2
                if self.sprite_atual >= 3:
                    self.sprite_atual = 0
                self.image = self.sprites[int(self.sprite_atual)]
            else:

                # Animacao 3
                if self.animacao == 2:
                    self.sprite_atual += self.vel
                    if self.sprite_atual >= 1 and self.sprite_atual < 3:
                        self.sprite_atual = 3
                    if self.sprite_atual >= 4:
                        self.sprite_atual = 0
                    self.image = self.sprites[int(self.sprite_atual)]
                else:

                    # Animacao 4
                    self.sprite_atual += self.vel
                    if self.sprite_atual < 2:
                        self.sprite_atual = 2
                    if self.sprite_atual >= 3 and self.sprite_atual < 4:
                        self.sprite_atual = 4
                    if self.sprite_atual >= 5:
                        self.sprite_atual = 2
                    self.image = self.sprites[int(self.sprite_atual)]

        # Tamanho da imagem
        self.image = p.transform.scale(self.image, (self.dim_sprites[0] * self.tam, self.dim_sprites[1] * self.tam))


class Obstaculo(Sprite):

    def __init__(self, tupla_posicao, tupla_dimensoes, lista_sprites_diretorio, tupla_dimensoes_sprites, tamanho_imagem):

        # Herdando a classe mae
        Sprite.__init__(self)

        # Atribuindo parametros
        self.pos = tupla_posicao
        self.dim = tupla_dimensoes
        self.lista = lista_sprites_diretorio
        self.dim_sprites = tupla_dimensoes_sprites
        self.tam = tamanho_imagem
        
        # Atributos
        self.tempo = 0
        self.caiu = False
        self.tipo = randint(0, 1)
        self.sprites = []
        self.hitbox = f.desenhar_retangulo((184, 31, 10), self.pos, self.dim)

        # Carregando os sprites
        for valor in self.lista:
            self.sprites.append(p.image.load(valor))

        # Criando a imagem
        self.image = self.sprites[0]

        # Criando o retangulo de posicionamento da imagem
        self.rect = self.image.get_rect()

        # Definindo as coordenadas do retangulo
        self.rect = (self.pos[0], self.pos[1])

    def cair(self):
        self.tempo += 1/60
        if self.tempo >= 3 and self.caiu == False:
            self.caiu = True
            f.som('impacto')

    def update(self):
        
        # Condicao para selecionar o sprite atual
        if self.caiu == True:
            if self.tipo == 1:
                self.image = self.sprites[1]
            else:
                self.image = self.sprites[2]
        else:
            self.image = self.sprites[0]

        # Tamanho da imagem
        self.image = p.transform.scale(self.image, (self.dim[0] * self.tam, self.dim[1] * self.tam))


class Background(Sprite):

    def __init__(self, lista_diretorio_sprites, velocidade_animacao, numero_sprites):

        # Herdando a classe mae
        Sprite.__init__(self)
        
        # Atribuindo parametros
        self.lista = lista_diretorio_sprites
        self.vel = velocidade_animacao
        self.num = numero_sprites

        # Atributos
        self.sprites = []
        self.sprite_atual = 0

        # Carregando os sprites
        for valor in self.lista:
            self.sprites.append(p.image.load(valor))

        # Criando a imagem
        self.image = self.sprites[0]

        # Criando o retangulo de posicionamento da imagem
        self.rect = self.image.get_rect()
        self.rect = (0, 0)

    def update(self):
        self.sprite_atual += self.vel
        if self.sprite_atual >= (self.num):
            self.sprite_atual = 0
        self.image = self.sprites[int(self.sprite_atual)]
