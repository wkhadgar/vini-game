import utils
import pygame
import random
import numpy as np
import time

pygame.init()
pygame.font.init()


PRETO = (0,0,0)
CINZA_ESCURO = (50, 50, 50)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AMARELO = (255, 255, 0)
ROXO = (255, 0, 255)
CYAN = (0, 255, 255)

cores = [BRANCO, VERMELHO, VERDE, AZUL, AMARELO, ROXO, CYAN]

class Border:
    def __init__(self, origin_x, origin_y, wid, hei, cor=VERMELHO) -> None:
        self.x_o = origin_x
        self.y_o = origin_y
        self.w = wid
        self.h = hei
        self.cor = cor

    def draw(self):
        pygame.draw.rect(screen, self.cor, ((self.x_o,self.y_o), (self.w, self.h)), 4)

class Button:

    def __init__(self, pos, tamanho=(100,50), cor=(100,100,100), text='', xo=65, yo=5):
        self.pos = pos
        self.tamanho = tamanho
        self.cor = np.array(cor)
        self.foco = 0
        self.texto = text
        self.x_offset = xo
        self.y_offset = yo

    def draw(self, screen):
        self.body = pygame.draw.rect(screen, self.cor-40, (self.pos, self.tamanho), 1)
        if self.body.collidepoint(pygame.mouse.get_pos()):
            self.foco = 1
            pygame.draw.rect(screen, self.cor+40, (self.pos, self.tamanho))
        else:
            self.foco = 0
            pygame.draw.rect(screen, self.cor, (self.pos, self.tamanho))
        
        utils.screen_print(screen, self.texto, PRETO, self.pos[0]+self.x_offset, self.pos[1]+self.y_offset)

class Player:
    def __init__(self, name, cor, width, height):
        self.x = random.randint(width//2.5, width//1.6)
        self.y = random.randint(height//2.5, height/1/1.6)
        self.name = name
        self.cor = cor
        self.hited = False
        self.go_down = random.randint(0,1)
        self.go_right = random.randint(0,1)
        self.speed = 0.5
        self.size = min(height, width) / 15
        self.health = 10
        self.defeat_time = 0
        self.bordem_listaer = random.choice(cores)
        self.power_up = 0

    def draw(self, x, y):
        self.body = pygame.draw.circle(screen, self.cor, (x, y), self.size, 0)
        pygame.draw.circle(screen, self.bordem_listaer, (x, y), self.size, 2)

class PowerUp(Player):
    def __init__(self, name, cor, width, height):
        super().__init__(name, cor)
        self.x = random.randint(30, width-30)
        self.y = random.randint(30, height-30)
        self.size = 20
        self.health = 5

    def draw(self, players):
        speed = 2
        self.x += random.choice(np.linspace(-1,1)) * speed
        self.y += random.choice(np.linspace(-1,1)) * speed
        self.body = pygame.draw.rect(screen, AMARELO, ((self.x, self.y), (self.size, self.size)))
        for player in players:
            if self.body.colliderect(player.body):
                print("ai")
                player.power_up += 1
                self.size = 0
                  

def move_handler(Border, player, timer, phase, phase_last):
    

    if player.go_down:
        player.y += player.speed
    else:
        player.y -= player.speed
    
    if player.go_right:
        player.x += player.speed
    else:
        player.x -= player.speed

    if player.x < Border.x_o+player.size:
        player.go_right = True
        player.hited = 1
    if player.y < Border.y_o+player.size:
        player.go_down = True
        player.hited = 2
    if player.x > (Border.x_o+Border.w)-player.size:
        player.go_right = False
        player.hited = 3
    if player.y > (Border.y_o+Border.h)-player.size:
        player.go_down = False
        player.hited = 4
    
    if player.hited:
        player.health -= 1
        player.size *= 0.8
        player.speed *= 0.7
        player.hited = 0

        if player.health == 0:
            player.speed = 0
            player.size = 0
            player.defeat_time = float(f"{timer: .2f}")
            player.health = -1

    if player.power_up:
        previous = player.health
        if phase == phase_last:
            player.health = 100
        else:
            player.power_up -= 1
            player.health = previous 
            
    player.draw(player.x, player.y)
    player.speed *= 1.0005

    return(player.x, player.y)


fps = 120
clock = pygame.time.Clock()
screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)
width, height = screen.get_size()



n_players = 1
jogadores = []
if n_players > 1:
    for i in range(1, n_players+1):
        jogadores.append(Player((f"Jogador {i}").strip().capitalize(), random.choice(cores), width, height))
else:
    jogadores.append(Player("", random.choice(cores), width, height))


edge = Border(0,0, width, height)
teste = Button((width/2-100,height-100), tamanho=(200,50), text="teste")
teste2 = Button((width/2-100,height-200), tamanho=(200,50), text="eu sou o 2", xo=25)
all_botoes = [teste, teste2]


run = True
playing = True
start =  False
first_return = True
defeat_triggers = [False]*len(jogadores)
inicio = time.time()
tempo_pausa = 0
timer = 0
debuffs = {2: "voce vai ficar maior!", 3: "voce vai acelerar! (e muito)", 5: "voce vai morrer :("}
level_triggers = [True]*100
clicado = 0

last = 1

while run:

    screen.fill(PRETO)
    agora = time.time()

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                run = False
            elif event.key == pygame.K_RETURN:
                start = not start
                if first_return:
                    inicio = time.time()
                    iniciobkp = inicio
                    first_return = False
                elif not start:
                    iniciobkp = agora
                if not first_return and start:
                    tempo_pausa += agora - iniciobkp
            if start:
                if event.key == pygame.K_w: # WASD jogador 1
                    jogadores[0].go_down = False
                elif event.key == pygame.K_s:
                    jogadores[0].go_down = True
                if event.key == pygame.K_a:
                    jogadores[0].go_right = False
                elif event.key == pygame.K_d:
                    jogadores[0].go_right = True

                if len(jogadores) > 1: # arrow keys jogador 2
                    if event.key == pygame.K_UP:
                        jogadores[1].go_down = False
                    elif event.key == pygame.K_DOWN:
                        jogadores[1].go_down = True
                    if event.key == pygame.K_LEFT:
                        jogadores[1].go_right = False
                    elif event.key == pygame.K_RIGHT:
                        jogadores[1].go_right = True

                if len(jogadores) > 2: # UHJK jogador 3
                    if event.key == pygame.K_u:
                        jogadores[2].go_down = False
                    elif event.key == pygame.K_j:
                        jogadores[2].go_down = True
                    if event.key == pygame.K_h:
                        jogadores[2].go_right = False
                    elif event.key == pygame.K_k:
                        jogadores[2].go_right = True
                

                if len(jogadores) > 3: # 8456 jogador 4
                    if event.key == pygame.K_8:
                        jogadores[3].go_down = False
                    elif event.key == pygame.K_5:
                        jogadores[3].go_down = True
                    if event.key == pygame.K_4:
                        jogadores[3].go_right = False
                    elif event.key == pygame.K_6:
                        jogadores[3].go_right = True

        if event.type == pygame.MOUSEBUTTONDOWN:
            for i, but in enumerate(all_botoes):
                if but.foco:
                    print(f"clicou no botão {i+1}")
                    clicado = i+1


        if event.type == pygame.QUIT:
            run = False

    if start:
        timer = (agora-inicio) - tempo_pausa
        if playing:
            edge.draw()
            phase = int((round(timer) - round(timer)%10)/10) + 1
            
            if level_triggers[phase]:
                if phase == 4:

                    edge.x_o = 300
                    edge.y_o = 300
                    edge.w -= 600
                    edge.h -= 600

                if phase == 6:
                    for player in jogadores:
                        player.health = 0
                if phase == 2:
                    for player in jogadores:
                        player.size *= 2.5
                    
                if phase == 3:
                    for player in jogadores:
                        player.speed *= 4

                level_triggers[phase] = False
            

            if phase+1 in [2,3,5]:
                utils.screen_print(screen, debuffs[phase+1], BRANCO, width/2-100, 40)
            utils.screen_print(screen, f"{timer:.2f}", BRANCO, width-100, 10)            
            utils.screen_print(screen, f"Fase {phase}", BRANCO, width/2-50, 10)

            ordem_lista = 0
            for p in jogadores:
                ordem_lista += 1
                utils.screen_print(screen, "VIDAS:", BRANCO, 10, 10)
                if not defeat_triggers[ordem_lista-1]:
                    utils.screen_print(screen, f"{p.name}", (255,255,255), p.x-p.size, p.y-p.size-20, 15)
                if p.health > 0:
                    utils.screen_print(screen, f"{p.name} "+f"{p.health} "+"♥ "*p.health, p.cor, 10, 40*ordem_lista+10)
                else:
                    defeat_triggers[ordem_lista-1] = True
                    utils.screen_print(screen, f"{p.name} derrotado em {p.defeat_time}", p.cor, 10, 40*ordem_lista+10)
                
            for p in jogadores:
                move_handler(edge, p, timer, phase, last)
                if last != phase:
                    last = phase
            
            if all(defeat_triggers):
                playing = False

            
        else:
             #endgame state
            final_scores = []
            utils.screen_print(screen, "FIM DE JOGO", BRANCO, (width/2)-190, (height/4)-30, 60)
            utils.screen_print(screen, "PLACAR FINAL", BRANCO, (width/2)-105, (height/3), 30)
            for p in jogadores:
                final_scores.append([p.defeat_time, p.cor, p.name])
            final_scores.sort(reverse=True)
            ordem_lista = 0
            for score in final_scores:
                ordem_lista += 1
                utils.screen_print(screen, f"{ordem_lista}º: {score[2]} - {score[0]}", score[1], (width/2)-100, (height/2.8)+40*ordem_lista, 30)
    else:
        for but in all_botoes:
            but.draw(screen)

        if clicado == 1:
            start = True
            clicado = 0
        if clicado == 2:
            run = False
    pygame.display.update()
    clock.tick(fps)

pygame.quit()