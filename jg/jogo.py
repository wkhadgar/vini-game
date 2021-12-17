import os
import utils
import pygame
import random
import numpy as np
import time
pygame.init()


fps = 120
clock = pygame.time.Clock()
#screen = pygame.display.set_mode((0,0), pygame.FULLSCREEN)

PRETO = (0,0,0)
CINZA_ESCURO = (50, 50, 50)
BRANCO = (255,255,255)
VERMELHO = (255,0,0)
VERDE = (0,255,0)
AZUL = (0,0,255)
AMARELO = (255, 255, 0)
GOLDEN = (200,200,30)
ROXO = (255, 0, 255)
CYAN = (0, 255, 255)
WINDOW_SURFACE   = pygame.HWSURFACE|pygame.DOUBLEBUF

cores = [BRANCO, VERMELHO, VERDE, AZUL, ROXO, CYAN]
infoObject = pygame.display.Info()
screen =  pygame.display.set_mode((infoObject.current_w, infoObject.current_h), WINDOW_SURFACE)
width, height = screen.get_size()

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

    def __init__(self, pos, _id, tamanho=(100,50), cor=(100,100,100),text='', xo=65, yo=5):
        self.pos = pos
        self.tamanho = tamanho
        self.cor = np.array(cor)
        self.foco = 0
        self.texto = text
        self.x_offset = xo
        self.y_offset = yo
        self.id = _id
        self.body = pygame.draw.rect(screen, self.cor, (self.pos, self.tamanho))

    def draw(self, screen, selected=-1):
        pygame.draw.rect(screen, self.cor-60, (np.array(self.pos)+3, self.tamanho), 6)
        if selected == self.id:
            self.foco = 1
            self.body = pygame.draw.rect(screen, self.cor+40, (self.pos, self.tamanho))
        else:
            self.foco = 0
            self.body = pygame.draw.rect(screen, self.cor, (self.pos, self.tamanho))
        
        utils.screen_print(screen, self.texto, PRETO, self.pos[0]+self.x_offset, self.pos[1]+self.y_offset)

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
        self.border_color = self.cor
        self.power_up = 0
        self.powerUp_timer = 0
        self.body = pygame.draw.circle(screen, self.cor, (self.x, self.y), self.size, 0)

    def draw(self, x, y):
        self.body = pygame.draw.circle(screen, self.cor, (x, y), self.size, 0)
        pygame.draw.circle(screen, self.border_color, (x, y), self.size, 4)

class PowerUp(Player):
    def __init__(self, name, cor):
        super().__init__(name, cor)
        self.x = random.randint(30, width-30)
        self.y = random.randint(
            
            
            
            
            
            
            30, height-30)
        self.size = 10
        self.tp_frames = 3*fps
        self.count = self.tp_frames+1
        self.state = 0

    def draw(self, players):
        if self.size > 0:
            speed = 5
            if self.tp_frames < self.count:
                self.x_goto = random.randint(0, width)
                self.y_goto = random.randint(0, height)
                self.count = 0
            self.count += 1
            
            pygame.draw.line(screen, CINZA_ESCURO, (self.x_goto-4, self.y_goto), (self.x_goto+4, self.y_goto), 1)
            pygame.draw.line(screen, CINZA_ESCURO, (self.x_goto, self.y_goto-4), (self.x_goto, self.y_goto+4), 1)

            x_inc = (self.x_goto-self.x) * speed
            y_inc = (self.y_goto-self.y) * speed

            if abs(x_inc) > 200*speed or abs(y_inc) > 200*speed:
                self.cor = (110,110,90)
                self.state = 0
            else:
                self.cor = AMARELO
                self.state = 1

            self.x += x_inc/600
            self.y += y_inc/600
            self.body = pygame.draw.rect(screen, self.cor, ((self.x, self.y), (self.size, self.size)))

            for player in players:
                dist = np.sqrt(((self.x-player.x)**2 + (self.y-player.y)**2))
                if dist < player.size and self.state:
                    print("ai")
                    player.power_up += 1
                    player.powerUp_timer = time.time()
                    self.size = 0
                  

def move_handler(Border, player, timer, n_players):
    

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
    
    if player.hited and player.power_up != 1:
        player.health -= 1
        player.size *= 0.8
        if player.speed > 0.4:
            player.speed *= 0.7
        player.hited = 0

        if player.health == 0:
            player.speed = 0
            player.size = 0
            player.defeat_time = float(f"{timer: .2f}")
            player.health = -1

    if player.power_up:
        crn = time.time() - player.powerUp_timer
        player.border_color = GOLDEN
        utils.screen_print(screen, f"{10-crn:.2f}", BRANCO, player.x-30, player.y+player.size)
        if crn > 10:
            player.power_up -= 1
            player.border_color = player.cor
            player.health += 1
            
    player.draw(player.x, player.y)
    player.speed *= (1.0007+n_players/10000)

    return(player.x, player.y)

def edge_adjust(bord, prop=1):
    if prop >= 1:
        bord.x_o = 0
        bord.y_o = 0
        bord.w = width
        bord.h = height
         
    else:        
        xo = width*prop
        yo = height*prop
        w = 2*width*prop
        h = 2*height*prop

        bord.x_o = xo
        bord.y_o = yo
        bord.w -= w
        bord.h -= h



def main():

    player_keys = [("player 1", [pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d]),
        ("player 2", [pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT])]
    bkp_player_keys = player_keys
    player_keys = player_keys[:2]
    difs = ["FÁCIL", "NORMAL", "DIFÍCIL"]
    dificuldade = 1
    n_players = len(player_keys)
    i_n_players = 1
                

    jogadores = []
    if n_players > 1:
        for i in range(1, n_players+1):
            jogadores.append(Player((f"Jogador {i}").strip().capitalize(), random.choice(cores)))
    else:
        jogadores.append(Player("", random.choice(cores)))
    bkp_jog = jogadores


    edge = Border(0,0, width, height)
    pre_edge = Border(0,0, width, height, cor=(10,0,70))

    pwup = PowerUp("teste", AMARELO)
    power_ups = []


    iniciar_but = Button((width/2-100,height-300), 0, tamanho=(200,50), text="INICIAR", xo=45)
    difc_but = Button((width/2-180,height-200), 1, tamanho=(360,50), text=f"DIFICULDADE: {difs[dificuldade]}", xo=7)
    sair_but = Button((width/2-100,height-100), 2, tamanho=(200,50), text="SAIR", xo=65)
    num_player_but = Button((width/2-125,height-400), 3, tamanho=(250,50), text=f"JOGADORES: {n_players}", xo=7)
    restart_but = Button((width/2-100, height-200), 4, tamanho=(200,50), text="RESTART", xo=40)

    start_botoes = [num_player_but, iniciar_but, difc_but , sair_but]
    pause_botoes = [iniciar_but, difc_but , sair_but]
    finish_botoes = [restart_but, sair_but]


    run = True
    playing = True
    start =  False
    first_action = True
    defeat_triggers = [False]*n_players
    inicio = time.time()
    tempo_pausa = 0
    timer = 0
    debuffs = {2: "voce vai ficar maior!", 3: "voce vai acelerar! (e muito)", 4: "o espaço vai ficar menor?"} #go to line 298
    level_triggers = [True]*100
    clicado = -1
    last = 1
    selecionado = 1

    bgs = []
    for filename in next(os.walk("assets/ingame_bgs"), (None, None, []))[2]:
        bg = pygame.image.load(f"assets/ingame_bgs/{filename}")
        bg = pygame.transform.scale(bg, (width, height))
        bgs.append(bg)


    menu_bg = pygame.image.load("assets/menu-bg.jfif")
    menu_bg = pygame.transform.scale(menu_bg, (width, height))

    parser = 0
    fps_counter = 0


    while run:

        screen.blit(bgs[parser], (0,0))
        #background img loop
        if fps_counter % (fps/30) == 0:
            parser += 1
            if parser >= len(bgs):
                parser = 0
        fps_counter += 1

        agora = time.time()

        for event in pygame.event.get():
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_SPACE:
                    start = not start
                    if first_action:
                        inicio = time.time()
                        iniciobkp = inicio
                        first_action = False
                    elif not start:
                        iniciobkp = agora
                    if not first_action and start:
                        tempo_pausa += agora - iniciobkp
                if start:
                    for i, player in enumerate(player_keys):
                        if event.key == player[1][0]: # WASD jogador 1
                            jogadores[i].go_down = False
                        elif event.key == player[1][1]:
                            jogadores[i].go_down = True
                        if event.key == player[1][2]:
                            jogadores[i].go_right = False
                        elif event.key == player[1][3]:
                            jogadores[i].go_right = True
                else:
                    if first_action:
                        target_botoes = start_botoes
                    elif playing:
                        target_botoes = pause_botoes
                    else:
                        target_botoes = finish_botoes
                        print("acabouuuuuuuuuu")
                        print(target_botoes)
                    
                    selec_n = [but.id for but in target_botoes]
                    if event.key == pygame.K_UP:
                        selecionado = (selecionado-1)%len(target_botoes)
                        selecionado_main = selec_n[selecionado]
                    if event.key == pygame.K_DOWN:
                        selecionado = (selecionado+1)%len(target_botoes)
                        selecionado_main = selec_n[selecionado]

                    if event.key == pygame.K_RETURN:
                        for i, but in enumerate(target_botoes):
                            if but.foco:
                                clicado = but.id


            if event.type == pygame.QUIT:
                run = False

        if start:

            timer = (agora-inicio) - tempo_pausa
            if playing:
                pre_edge.draw()
                edge.draw()
                phase = int((round(timer) - round(timer)%10)/10) + 1
                
                for pwu in power_ups:
                    if len(power_ups):
                        pwu.draw(jogadores)

                if level_triggers[phase]:
                    if phase == 2:
                        for player in jogadores:
                            player.size *= (1.5 + dificuldade)

                    if phase == 3:
                        red_prop = (0.07 + dificuldade/20)
                        edge_adjust(pre_edge, red_prop)
                        for player in jogadores:
                            player.speed *= (3 + dificuldade)
                        
                    if phase == 4:
                        for player in jogadores:
                            player.speed /= (3 + dificuldade)
                        edge_adjust(edge, red_prop)
                        edge_adjust(pre_edge, 1)
                        power_ups.append(pwup)

                    if phase == 5:
                        edge_adjust(edge, 1)
                        for player in jogadores:
                            player.size /= (1.5 + dificuldade)

                    
                    if phase == 100:
                        for player in jogadores:
                            player.health = 0

                        

                    level_triggers[phase] = False
                

                utils.screen_print(screen, f"{timer:.2f}", BRANCO, width-100, 10)            
                utils.screen_print(screen, f"Fase {phase}", BRANCO, width/2-50, 10)

                ordem_lista = 0
                for p in jogadores:
                    ordem_lista += 1
                    utils.screen_print(screen, "VIDAS:", BRANCO, 10, 10)
                    if not defeat_triggers[ordem_lista-1]:
                        utils.screen_print(screen, f"{p.name}", (255,255,255), p.x-p.size, p.y-p.size-20, 15)
                    if p.health > 0:
                        utils.screen_print(screen, f"{p.name} "+f"{p.health} "+"♥ "*p.health, p.border_color, 10, 40*ordem_lista+10)
                    else:
                        defeat_triggers[ordem_lista-1] = True
                        utils.screen_print(screen, f"{p.name} derrotado em {p.defeat_time}", p.cor, 10, 40*ordem_lista+10)
                if phase+1 in debuffs.keys():
                    utils.screen_print(screen, debuffs[phase+1], BRANCO, width/2-100, 40)
                    
                for p in jogadores:
                    move_handler(edge, p, timer, n_players)
                    if last != phase:
                        last = phase
                
                if all(defeat_triggers):
                    playing = False
                    print("morreu todos")
            else:
                start = False
                print("isso dpeois ")

        else:
            if not playing:
                #endgame state
                final_scores = []
                utils.screen_print(screen, "FIM DE JOGO", BRANCO, (width/2)-190, (height/4)-30, 60)
                utils.screen_print(screen, "PLACAR FINAL", BRANCO, (width/2)-105, (height/3), 30)

                for but in finish_botoes:
                    but.draw(screen, selected=selecionado_main)
                
                if clicado == 4:
                    inicio = time.time()
                    tempo_pausa = 0
                    timer = 0
                    defeat_triggers = [False]*n_players
                    for p in jogadores:
                        p.health = 10
                        p.defeat_time=0
                        p.size = min(height, width) / 15
                        playing = True
                        p.x = random.randint(200, width-200)
                        p.y = random.randint(200, height-200)
                        p.speed = 0.5

                if clicado == 2: 
                    run = False

                for p in jogadores:
                    final_scores.append([p.defeat_time, p.cor, p.name])
                final_scores.sort(reverse=True)
                ordem_lista = 0
                for score in final_scores:
                    ordem_lista += 1
                    utils.screen_print(screen, f"{ordem_lista}º: {score[2]} - {score[0]}", score[1], (width/2)-140, (height/2.8)+40*ordem_lista, 30)

        
            else:
                screen.blit(menu_bg, (0,0))
                if first_action:
                    for but in start_botoes:
                        but.draw(screen, selected=selecionado)
                else:
                    for but in pause_botoes:
                        but.draw(screen, selected=selecionado)

                if clicado == 0:
                    if first_action:
                        inicio = time.time()
                        iniciobkp = inicio
                        first_action = False
                    start = True
                    clicado = -1
                if clicado == 1:
                    dificuldade = (dificuldade+1)%len(difs)
                    pause_botoes[1].texto = f"DIFICULDADE: {difs[dificuldade]}"
                    clicado = -1
                if clicado == 2:
                    run = False
                if clicado == 3:
                    jog_ = [1,2]
                    i_n_players = (i_n_players+1)%2
                    n_players = jog_[i_n_players]
                    player_keys = bkp_player_keys[:n_players]
                    defeat_triggers = [False]*n_players
                    start_botoes[0].texto = f"JOGADORES: {n_players}"
                    jogadores = bkp_jog[:(n_players)]
                    clicado = -1

        pygame.display.update()
        clock.tick(fps)

    pygame.quit()


if __name__ == '__main__':

    pygame.font.init()
    main()
