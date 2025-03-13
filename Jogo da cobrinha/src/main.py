import pygame
import random
import os

pygame.init()

# Configurações
LARGURA, ALTURA = 800, 600
TAMANHO_BLOCO = 30
VELOCIDADE = 15
CORES = {'BRANCO': (255, 255, 255)}

tela = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Jogo da Cobrinha - Computação Gráfica")

def carregar_imagem(nome, tamanho=None):
    caminho = os.path.join("assets", nome)
    try:
        imagem = pygame.image.load(caminho).convert_alpha()
    except pygame.error as e:
        print(f"Erro ao carregar imagem {nome}: {e}")
        raise SystemExit
    return pygame.transform.scale(imagem, tamanho) if tamanho else imagem

def mostrar_texto(texto, tamanho, cor, x, y):
    fonte = pygame.font.SysFont('arial', tamanho, bold=True)
    texto_surface = fonte.render(texto, True, cor)
    tela.blit(texto_surface, (x, y))

# Carregar recursos
tela_inicio_img = carregar_imagem("Inicio.png", (LARGURA, ALTURA))
tela_game_over_img = carregar_imagem("game over.png", (LARGURA, ALTURA))
tela_creditos_img = carregar_imagem("creditos.png", (LARGURA, ALTURA))
fundo = carregar_imagem("Grama1.png", (LARGURA, ALTURA))
comida_img = carregar_imagem("comida.jpg", (TAMANHO_BLOCO, TAMANHO_BLOCO))

class RecursosCobra:
    def __init__(self):
        self.cabeca = {
            'UP': carregar_imagem("cabeca_up.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'DOWN': carregar_imagem("cabeca_down.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'LEFT': carregar_imagem("cabeca_left.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'RIGHT': carregar_imagem("cabeca_right.png", (TAMANHO_BLOCO, TAMANHO_BLOCO))
        }
        self.cauda = {
            'UP': carregar_imagem("cauda_up.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'DOWN': carregar_imagem("cauda_down.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'LEFT': carregar_imagem("cauda_left.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'RIGHT': carregar_imagem("cauda_right.png", (TAMANHO_BLOCO, TAMANHO_BLOCO))
        }
        self.corpo = {
            'VERTICAL': carregar_imagem("corpo_down.png", (TAMANHO_BLOCO, TAMANHO_BLOCO)),
            'HORIZONTAL': carregar_imagem("corpo_right.png", (TAMANHO_BLOCO, TAMANHO_BLOCO))
        }

def tela_inicio():
    while True:
        tela.blit(tela_inicio_img, (0, 0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    return True   # Iniciar jogo
                elif event.key == pygame.K_2: 
                    tela_creditos()  # Mostrar créditos
                elif event.key == pygame.K_3: 
                    return False  # Fechar jogo

def tela_creditos():
    while True:
        tela.blit(tela_creditos_img, (0, 0))
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    return  # Voltar para tela inicial
                elif event.key == pygame.K_2: 
                    pygame.quit()
                    return

def tela_game_over(pontos):
    while True:
        tela.blit(tela_game_over_img, (0, 0))
        mostrar_texto(f"Pontuação: {pontos}", 40, CORES['BRANCO'], 10, 10)
        pygame.display.update()
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return 'sair'
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1: 
                    return 'reiniciar'
                elif event.key == pygame.K_2: 
                    tela_creditos()
                elif event.key == pygame.K_3: 
                    return 'menu'  # Alterado para retornar 'menu'

def main():
    while True:
        # Tela inicial
        inicio = tela_inicio()
        if not inicio:
            break  # Fechar jogo
        
        # Loop do jogo
        while True:
            pontuacao = jogo_principal()
            resultado = tela_game_over(pontuacao)
            
            if resultado == 'reiniciar':
                continue  # Reinicia o jogo
            elif resultado == 'menu':
                break  # Volta para o menu inicial
            elif resultado == 'sair':
                pygame.quit()
                return

class Cobra:
    def __init__(self):
        self.recursos = RecursosCobra()
        self.reset()
    
    def reset(self):
        self.corpo = [
            [LARGURA//2, ALTURA//2],
            [LARGURA//2 - TAMANHO_BLOCO, ALTURA//2],
            [LARGURA//2 - 2*TAMANHO_BLOCO, ALTURA//2]
        ]
        self.direcoes = ['RIGHT', 'RIGHT', 'RIGHT']
        self.direcao = 'RIGHT'
        self.comprimento = 3
    
    def mover(self):
        movimentos = {
            'LEFT': (-TAMANHO_BLOCO, 0),
            'RIGHT': (TAMANHO_BLOCO, 0),
            'UP': (0, -TAMANHO_BLOCO),
            'DOWN': (0, TAMANHO_BLOCO)
        }
        dx, dy = movimentos[self.direcao]
        nova_cabeca = [self.corpo[0][0] + dx, self.corpo[0][1] + dy]
        self.corpo.insert(0, nova_cabeca)
        self.direcoes.insert(0, self.direcao)
        if len(self.corpo) > self.comprimento:
            self.corpo.pop()
            self.direcoes.pop()
    
    def desenhar(self):
        for i, (pos, dir) in enumerate(zip(self.corpo, self.direcoes)):
            if i == 0:
                img = self.recursos.cabeca[dir]
            elif i == len(self.corpo)-1:
                img = self.recursos.cauda[self.direcoes[-1]]
            else:
                img = self.recursos.corpo['HORIZONTAL' if dir in ['LEFT', 'RIGHT'] else 'VERTICAL']
            tela.blit(img, pos)

class Comida:
    def __init__(self, cobra_corpo):
        self.posicao = [0, 0]
        self.reposicionar(cobra_corpo)
    
    def desenhar(self): 
        tela.blit(comida_img, self.posicao)
    
    def reposicionar(self, cobra_corpo):
        while True:
            self.posicao = [
                random.randrange(0, LARGURA - TAMANHO_BLOCO + 1, TAMANHO_BLOCO),
                random.randrange(0, ALTURA - TAMANHO_BLOCO + 1, TAMANHO_BLOCO)
            ]
            comida_rect = pygame.Rect(self.posicao[0], self.posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
            colisao = False
            for segmento in cobra_corpo:
                segmento_rect = pygame.Rect(segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
                if comida_rect.colliderect(segmento_rect):
                    colisao = True
                    break
            if not colisao:
                break

def jogo_principal():
    cobra = Cobra()
    comida = Comida(cobra.corpo)
    relogio = pygame.time.Clock()
    pontuacao = 0
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                return pontuacao
            
            if event.type == pygame.KEYDOWN:
                teclas = {
                    pygame.K_LEFT: 'LEFT' if cobra.direcao != 'RIGHT' else None,
                    pygame.K_RIGHT: 'RIGHT' if cobra.direcao != 'LEFT' else None,
                    pygame.K_UP: 'UP' if cobra.direcao != 'DOWN' else None,
                    pygame.K_DOWN: 'DOWN' if cobra.direcao != 'UP' else None
                }
                if event.key in teclas and teclas[event.key]:
                    cobra.direcao = teclas[event.key]
        
        cobra.mover()
        
        cabeca = cobra.corpo[0]
        cabeca_rect = pygame.Rect(cabeca[0], cabeca[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
        
        # Colisão com bordas
        if (cabeca_rect.left < 0 or cabeca_rect.right > LARGURA or
            cabeca_rect.top < 0 or cabeca_rect.bottom > ALTURA):
            return pontuacao
        
        # Colisão com corpo
        for segmento in cobra.corpo[1:]:
            segmento_rect = pygame.Rect(segmento[0], segmento[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
            if cabeca_rect.colliderect(segmento_rect):
                return pontuacao
        
        # Colisão com comida
        comida_rect = pygame.Rect(comida.posicao[0], comida.posicao[1], TAMANHO_BLOCO, TAMANHO_BLOCO)
        if cabeca_rect.colliderect(comida_rect):
            comida.reposicionar(cobra.corpo)
            cobra.comprimento += 1
            pontuacao += 1
        
        # Renderização
        tela.blit(fundo, (0, 0))
        mostrar_texto(f"Pontuação: {pontuacao}", 30, CORES['BRANCO'], 10, 10)
        comida.desenhar()
        cobra.desenhar()
        pygame.display.update()
        relogio.tick(VELOCIDADE)

def main():
    while True:
        # Tela inicial
        inicio = tela_inicio()
        if not inicio:
            break  # Fechar jogo
        
        # Loop do jogo
        while True:
            pontuacao = jogo_principal()
            resultado = tela_game_over(pontuacao)
            
            if resultado == 'reiniciar':
                continue  # Reinicia o jogo
            else:
                break  # Sai ou volta ao menu
            
        if resultado == 'sair':
            break  # Fecha o jogo totalmente

    pygame.quit()

if __name__ == "__main__":
    main()