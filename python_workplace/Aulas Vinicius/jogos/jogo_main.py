import utils
import pygame
import random
import sys
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

width, height =  1800, 1000

 
class Menu:
    def __init__(self, screen_size) -> None:
        self.xsize, self.ysize = screen_size
        self.onfocus = 0
        self.menu_dims = ((100,100), (self.xsize-200, self.ysize-200))
        self.xsize = self.xsize-100
        self.ysize = self.ysize-100

    def draw_button(self, name, origin):
        self.button_size = ((origin[0], origin[1]), (origin[0]+20, origin[1]+10))
        button1 = pygame.draw.rect(screen, (0, 32, 0), (self.button_size))
        return (button1, name)

    def draw(self, timer):
        self.skeleton = pygame.draw.rect(screen, (94, 119, 104), self.menu_dims)
        pygame.draw.rect(screen, (90, 149, 90), self.menu_dims, 4)
        utils.screen_print(screen, "PARA INICIAR O JOGO", BRANCO, (self.xsize/2)-310, (self.ysize/4)-30, 60)
        utils.screen_print(screen, f"APERTE ENTER {timer: .2f}", BRANCO, (self.xsize/2)-285, (self.ysize/3)-30, 60)

        op1 = self.draw_button("op1", (100, 100))
        op2 = self.draw_button("op2", (self.xsize, self.ysize))

class Player:
    def __init__(self, name, cor):
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
        self.border = random.choice(cores)
    def draw(self, x, y):
        self.body = pygame.draw.circle(screen, self.cor, (x, y), self.size, 0)
        pygame.draw.circle(screen, self.border, (x, y), self.size, 2)
        

def move_handler(player, timer):
    
    if player.go_down:
        player.y += player.speed
    else:
        player.y -= player.speed
    
    if player.go_right:
        player.x += player.speed
    else:
        player.x -= player.speed

    if player.x < player.size:
        player.go_right = True
        player.hited = 1
    if player.y < player.size:
        player.go_down = True
        player.hited = 2
    if player.x > width-player.size:
        player.go_right = False
        player.hited = 3
    if player.y > height-player.size:
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

            
    player.draw(player.x, player.y)
    player.speed *= 1.0005

    return(player.x, player.y)



fps = 120
clock = pygame.time.Clock()

n_players = int(input("quantos jogadores: "))
jogadores = []
if n_players > 1:
    for i in range(n_players):
        jogadores.append(Player(input(f"Jogador {i+1}: ").strip().capitalize(), random.choice(cores)))
else:
    jogadores.append(Player("", random.choice(cores)))

screen = pygame.display.set_mode((width, height))
main_menu = Menu((width, height))

run = True
playing = True
start =  False
first_return = True
defeat_triggers = [False]*len(jogadores)
inicio = time.time()
tempo_pausa = 0
timer = 0

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

                if len(jogadores) > 1: # UHJK jogador 2
                    if event.key == pygame.K_u:
                        jogadores[1].go_down = False
                    elif event.key == pygame.K_j:
                        jogadores[1].go_down = True
                    if event.key == pygame.K_h:
                        jogadores[1].go_right = False
                    elif event.key == pygame.K_k:
                        jogadores[1].go_right = True
                
                if len(jogadores) > 2: # arrow keys jogador 3
                    if event.key == pygame.K_UP:
                        jogadores[2].go_down = False
                    elif event.key == pygame.K_DOWN:
                        jogadores[2].go_down = True
                    if event.key == pygame.K_LEFT:
                        jogadores[2].go_right = False
                    elif event.key == pygame.K_RIGHT:
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

        if event.type == pygame.QUIT:
            run = False

    if start:
        timer = (agora-inicio) - tempo_pausa
        if playing:
            phase = int((round(timer) - round(timer)%10)/10) + 1

            utils.screen_print(screen, f"{timer:.2f}", BRANCO, width-100, 10)            
            utils.screen_print(screen, f"Fase {phase}", BRANCO, width/2-50, 10)

            pos = 0
            for p in jogadores:
                pos += 1
                utils.screen_print(screen, "VIDAS:", BRANCO, 10, 10)
                if not defeat_triggers[pos-1]:
                    utils.screen_print(screen, f"{p.name}", (255,255,255), p.x-p.size, p.y-p.size-20, 15)
                if p.health > 0:
                    utils.screen_print(screen, f"{p.name} "+f"{p.health} "+"♥ "*p.health, p.cor, 10, 40*pos+10)
                else:
                    defeat_triggers[pos-1] = True
                    utils.screen_print(screen, f"{p.name} derrotado em {p.defeat_time}", p.cor, 10, 40*pos+10)
                
            for p in jogadores:
                move_handler(p, timer)
            
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
            pos = 0
            for score in final_scores:
                pos += 1
                utils.screen_print(screen, f"{pos}º: "+f"{score[2]} - "+f"{score[0]}", score[1], (width/2)-100, (height/2.8)+40*pos, 30)
    else: 
        #paused state
        main_menu.draw(timer)

    pygame.display.update()
    clock.tick(fps)

pygame.quit()