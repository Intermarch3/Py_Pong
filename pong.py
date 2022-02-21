####################################
#                                  #
#   programme: pong game           #
#   auteur: Lucas L                #
#   date debut dev: 25/01/2022     #
#                                  #
####################################

##### importation librairie #####
from pygame.locals import *
import pygame,sys
from pygame.draw import *
from pygame.display import *
from random import randint

##### variables globales #####
size = width, height = 1500, 800 # taille de la fenêtre d'affichage
couleurFond = [0, 0, 0]    # noir
point_j1 = 0
point_j2 = 0
text_j1 = '0'.rjust(3)
text_j2 = '0'.rjust(3)
tap = 0
play = False
next = False

##### déclaration des attributs de la balle #####
dx = 4    # vecteur de déplacement
dy = 2
x = 750
y = 100
r = 10
couleurBalle = [255, 255, 255]

##### déclaration des attributs des raquettes #####
rx_j1, rx_j2 = 20, width - 40
ry_j1 = height / 2
ry_j2 = height / 2
dry_j1, dry_j2  = 4, 4 # vitesse raquette
rh_j1, rh_j2 = 100, 100
rw_j1, rw_j2 = 20, 20
rcolor = [255, 255, 255]


##### déclaration des fonctions #####
def menu(next_game=None):
    # fonction qui affiche le menu general avec bouton play et quit
    # parametre: next_game = dit si c'est la premiere partie; type = bool
    # retourne rien
    global play, mon_icon, couleurFond
    clickable_play_btn = pygame.Rect((250, 100), (700, 200))
    clickable_quit_btn = pygame.Rect((250, 100), (700, 500))
    rect_surf_play_btn = pygame.Surface(clickable_play_btn.size)
    rect_surf_quit_btn = pygame.Surface(clickable_quit_btn.size)
    # chargement et redimmension des image 
    play_btn = pygame.image.load("Images/play_btn_pong.png")
    quit_btn = pygame.image.load("Images/quit_btn_pong.png")
    play_btn = pygame.transform.scale(play_btn, (250, 100))
    quit_btn = pygame.transform.scale(quit_btn, (250, 100))
    mon_icon = pygame.transform.scale(mon_icon, (300, 300))
    # verif si btn cliquer
    while play != True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            elif event.type == MOUSEBUTTONUP: # quand je relache le bouton
                if event.button == 1: # 1 = clique gauche
                    if clickable_play_btn.collidepoint(event.pos):
                        pygame.mixer.Sound.play(btn)
                        play = True
                    elif clickable_quit_btn.collidepoint(event.pos):
                        pygame.display.quit()
                        sys.exit()
        # affichage bouton
        screen.fill(couleurFond)
        screen.blit(rect_surf_play_btn, clickable_play_btn)
        screen.blit(rect_surf_quit_btn, clickable_quit_btn)
        screen.blit(play_btn, (700, 200))
        screen.blit(quit_btn, (700, 500))
        screen.blit(mon_icon, (200, 250))
        pygame.display.flip()
    if next_game == True:
        pygame.mixer.music.play(-1)
        compte_rebourd()


def afficher():
    # fonction qui affiche la balle
    # aucun parametre
    # retourne rien
	global x, y, couleurBalle, r
	circle(screen, couleurBalle , [x, y], r, 0)


def avancer():
    # fonction qui fait avancer la balle
    # aucun parametre
    # retourne rien
	global x, y, dx, dy
	x = x + dx
	y = y + dy


def testCollision():
    # fonction qui verifie si la balle entre en colision avec un mure ou une raquette
    # aucun parametre
    # retourne rien
    global x, y, width, height, r, dx, dy, point_j1, point_j2, text_j1, text_j2, tap, dry_j1, dry_j2, ry_j1, ry_j2, rebond
    #bords verticaux
    if x + r > width: # rebond bord droit
        point_j1 = point_j1 + 1
        pygame.mixer.Sound.play(win_point)
        if point_j1 != 3:
            compte_rebourd()
        # reset var de position vitesse et autre
        tap = 0
        dry_j1, dry_j2  = 4, 4
        cote = randint(1, 2)
        if cote == 1:
            dx = -6
            dy = -3
        else:
            dx = 6
            dy = 3
        ry_j1 = height / 2
        ry_j2 = height / 2
        x = 750
        y = randint(50, 750)
    elif x - r < 0: # rebond bord gauche
        point_j2 = point_j2 + 1
        pygame.mixer.Sound.play(win_point)
        if point_j2 != 3:
            compte_rebourd()
        # reset var de position vitesse et autre
        tap = 0
        dry_j1, dry_j2  = 4, 4
        cote = randint(1, 2)
        if cote == 1:
            dx = -6
            dy = -3
        else:
            dx = 6
            dy = 3
        ry_j1 = height / 2
        ry_j2 = height / 2
        x = 750
        y = randint(50, 750)
    if y + r > height or y - r < 0: #bords horizontaux
        pygame.mixer.Sound.play(rebond)
        dy = -dy
    #rebond raquettes :
    if (ry_j1 < y) and (y < (ry_j1 + rh_j1)) and ((x - r) < (rx_j1 + rw_j1)): # raquette gauche
        pygame.mixer.Sound.play(rebond)
        dx = -dx
    if (ry_j2 < y) and (y < (ry_j2 + rh_j2)) and ((x + r) > (rx_j2)): # raquette droite
        pygame.mixer.Sound.play(rebond)
        dx = -dx
        tap += 1
        if (tap % 2) == 0: # tous les 2 rebond sur raquette droite
            dx = dx * 2 # vitesse balle x2
            dy = dy * 2
            dry_j1 += 1 # augmentation vitesse raquette
            dry_j2 += 1


def testEvenements():
    # fonction qui gere les evenement ( touche enfoncé et clic souris )
    # aucun parametre
    # retourne rien
    for event in pygame.event.get():
        if event.type == QUIT:      # si clique sur quitter
            pygame.display.quit()   # ferme la fenêtre
            sys.exit()              # arrête le programme
        if event.type == KEYDOWN:
            bouger_raquette()


def afficher_raquette():
    # fonction qui affiche la raquette et le score des joueurs
    # aucun parametre
    # retourne rien
    global point_j1, point_j2
    t1, t2 = str(point_j1).rjust(3), str(point_j2).rjust(3)
    font_point = pygame.font.SysFont('Bauhaus 93', 50)
    rect(screen, rcolor, [rx_j1, ry_j1, rw_j1, rh_j1])
    rect(screen, rcolor, [rx_j2, ry_j2, rw_j2, rh_j2])
    screen.blit(font_point.render(t1, True, (255, 255, 255)), (550, 50))
    screen.blit(font_point.render(t2, True, (255, 255, 255)), (900, 50))


def bouger_raquette():
    # fonction qui fait bouger les raquettes quand on appuie sur certaine touche
    # aucun parametre
    # retourne rien
    global ry_j1, dry_j1, ry_j2, dry_j2
    if pygame.key.get_pressed()[K_z]: # remplacer par w ou z en fonction du clavier
        if ry_j1 < 5:
            pass
        elif ry_j1 > 5:
            ry_j1 -= dry_j1
    if pygame.key.get_pressed()[K_s]:
        if (ry_j1 + rh_j1) > height - 5:
            pass
        elif ry_j1 < height - 5:
            ry_j1 += dry_j1 
    if pygame.key.get_pressed()[K_UP]:
        if ry_j2 < 5:
            pass
        elif ry_j2 > 5:
            ry_j2 -= dry_j2
    if pygame.key.get_pressed()[K_DOWN]:
        if (ry_j2 + rh_j2) > height - 5:
            pass
        elif ry_j2 < height - 5:
            ry_j2 += dry_j2


def compte_rebourd():
    # fonction qui realise et affiche un compte a rebourd
    # aucun parametre
    # retourne rien
    pygame.mixer.music.pause()
    clock = pygame.time.Clock()
    counter, text = 3, '3'.rjust(3)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if e.type == pygame.USEREVENT:
                counter -= 1
                text = str(counter).rjust(3) 
            if counter == 0: break
        else:
            screen.fill((0, 0, 0))
            screen.blit(font.render(text, True, (255, 255, 255)), (700, 200))
            pygame.display.flip()
            clock.tick(100)
            continue
        break
    pygame.mixer.music.unpause()


def winner(j):
    # fonction qui affiche le gagnant et le score final des joueurs
    # parametre: j = nom du joueur type = str
    # retourne rien
    global point_j1, point_j2, play
    t1, t2 = str(point_j1).rjust(3), str(point_j2).rjust(3)
    text = j + ' Gagne'.rjust(3)
    text_space = 'Tape sur [ESPACE] pour rejouer'
    font = pygame.font.SysFont('Bauhaus 93', 50)
    font_point = pygame.font.SysFont('Bauhaus 93', 100)
    new_game = False
    pygame.mixer.music.stop()
    while new_game != True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.display.quit()
                sys.exit()
            if pygame.key.get_pressed()[K_SPACE]:
                pygame.mixer.Sound.play(btn)
                # reset score
                point_j1 = 0
                point_j2 = 0
                play = False
                new_game = True
                break
        else:
            screen.fill((0, 0, 0))
            screen.blit(font.render(text, True, (255, 255, 255)), (550, 350))
            screen.blit(font.render(text_space, True, (255, 255, 255)), (450, 600))
            screen.blit(font_point.render(t1, True, (255, 255, 255)), (300, 200))
            screen.blit(font_point.render(t2, True, (255, 255, 255)), (1100, 200))
            pygame.display.flip()
            continue
    new_game = False
    menu(True)



if next == False: # si premiere partie:
    # initialisation des composants
    pygame.init()
    pygame.display.set_caption(" | Pong Game | ")
    mon_icon = pygame.image.load("Images/icone_pong.png")
    pygame.display.set_icon(mon_icon)
    pygame.mixer.init()
    pygame.mixer.music.load("Musique/Tetris_musique.mp3")
    rebond = pygame.mixer.Sound("Musique/ball-tap.wav")
    btn = pygame.mixer.Sound("Musique/btn.wav")
    win_point = pygame.mixer.Sound("Musique/win_point.wav")
    # vérifier les interactions clavier toutes les 10ms
    pygame.key.set_repeat(10, 10)
    screen = set_mode(size)
    # affichage menu
    menu()
    pygame.mixer.music.play(-1)
    font = pygame.font.SysFont('Bauhaus 93', 100)
    compte_rebourd()


while True:
    screen.fill(couleurFond)
    afficher()
    avancer()
    testCollision()
    afficher_raquette()
    flip() 
    pygame.time.delay(15)  #une image toute les 15 ms
    testEvenements()
    if point_j1 == 3:
        winner("Joueur gauche")
    elif point_j2 == 3:
        winner("Joueur droite")
