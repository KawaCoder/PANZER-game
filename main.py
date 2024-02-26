import pygame
import sys
from zombie_manager import zombie_manager
from zombax import zombax
from pygame.locals import *
import math
import time as t
from menu import Menu
import random
menu = Menu()
menu.menu()

# Initialisation de Pygame
pygame.init()

# Obtenir les dimensions de l'écran
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Paramètres de la fenêtre
floor_height = 100  # Hauteur du sol
floor_color = (34, 139, 34)  # Vert foncé (couleur de l'herbe)
sky_color = (0, 255, 255)  # Cyan (couleur du ciel)
canon_color = (132, 132, 132) # gris (couleur du canon)

# Initialisation du mixeur
pygame.mixer.init()
pygame.mixer.music.load("assets/canon.mp3")


# Paramètres du zombie
zombie_image_path = "assets/nazi.png"
zombie_width, zombie_height = 200, 200
zombie_speed = 5
zombie_pos = [width - zombie_width, height - floor_height - zombie_height]

# Création de la fenêtre en plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)  # Utilisez self.width et self.height

#pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Mon jeu Pygame - Zombie Shooter")

# Chargement de l'image du zombie
zombie_image = pygame.image.load(zombie_image_path)
zombie_image = pygame.transform.scale(zombie_image, (zombie_width, zombie_height))

# Paramètre du canon 
brouette_path = "assets/canon/brouette.png"
canon_image_path = "assets/canon/canon_tuyaux.png"
canon_width, canon_height = 50, 100
canon_pos = [100,height-floor_height-50]
a = pygame.draw.rect(screen, (0,0,0), (150,150,150,150))
boulet_image_path = "assets/canon/boulet.png"
TWINGO_path = "assets/canon/twingo.png"
g=9.8
launch=False

# Score
score = 0

# Chargement de l'image du canon
canon_image = pygame.image.load(canon_image_path).convert_alpha()
rect_canon = canon_image.get_rect(center=(canon_pos))

# Création de l'objet Clock
clock = pygame.time.Clock()

# paramètre du lancer
alpha=315
vitesse_initiale_lancer=100

# Texte du score
font = pygame.font.SysFont(None, 75)
score_texte = font.render("Score: ", True, (0, 0, 0))
score_rect = score_texte.get_rect(center=(100, 100))

# Gestion du Zombax
ZManager = zombie_manager(pygame)
print(ZManager.getZombies())

# Gestion du Zombie triple mooonstre
# Paramètres de la fenêtre
floor_height = 100  # Hautembax
ZManager = zombie_manager(pygame)
print(ZManager.getZombies())

# fonction pour faire une rotation propre sans devenir un TUC
def rot_center(image, angle):
    rect_origine = image.get_rect()
    rotate_image = pygame.transform.rotate(image, angle)
    rotate_rect = rect_origine.copy()
    rotate_rect.center = rotate_image.get_rect().center
    rotate_image = rotate_image.subsurface(rotate_rect).copy()
    return rotate_image
canon_mouv = rot_center(canon_image, alpha)

bg = pygame.image.load("assets/ciel.jpg")
bg = pygame.transform.scale(bg, (width, height))

# fonction pour créer un boulet (pour eviter de reset un boulet déjà lancé)
def creation_boulet():
    boulet_image = pygame.image.load(boulet_image_path).convert_alpha()
    rect_boulet = boulet_image.get_rect(center=(canon_pos))
    return boulet_image, rect_boulet
afficher_boulets=0

"""def lancer(boulet, alpha, vitesse_initiale_lancer, g, t0, canon_pos):
    # vecteur position
    BOx=(vitesse_initiale_lancer*math.cos(alpha))*(t.time()-t0)+canon_pos[0]
    BOy=-1/2*g*(t.time()-t0)**2+(vitesse_initiale_lancer*math.sin(alpha))+canon_pos[1]
    coord_boulet=(BOx,BOy)
    return coord_boulet"""

test = [0, 0]
def lancer(alpha, v0, g, x, w0, h0):
    # Convertir l'angle alpha en radians
    alpha = math.radians(alpha)
    alpha = - alpha
    y=(1/2)*g*((x-w0)/(v0*math.sin(alpha)))**2-(v0*math.cos(alpha))*((x-w0)/(v0*math.sin(alpha)))+h0
    coord_boulet=(x,y)
    return coord_boulet
indice_lancer=75

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:                
                print(ZManager.getZombies())
            if event.key == pygame.K_SPACE:
                if(not launch):

                    pygame.mixer.music.play()
                    pygame.event.wait()
                    if random.randint(0,15) == 1:
                        nouveau_boulet = pygame.image.load(TWINGO_path).convert_alpha()
                        nouveau_rect_boulet = nouveau_boulet.get_rect(center=(canon_pos))
                        screen.blit(nouveau_boulet, nouveau_rect_boulet)
                        launch=True
                    else:
                        nouveau_boulet = pygame.image.load(boulet_image_path).convert_alpha()
                        nouveau_rect_boulet = nouveau_boulet.get_rect(center=(canon_pos))
                        screen.blit(nouveau_boulet, nouveau_rect_boulet)
                        launch=True
                
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()


    if launch==True:
        for zombie in ZManager.getZombies():
            zombie_x, zombie_y = zombie.getPos()  # Position du zombie
            zombie_rect = pygame.Rect(zombie_x, zombie_y, 50, 50)  # Rectangle de collision du zombie
            boulet_rect = pygame.Rect(test[0], test[1], 30, 30)
            if boulet_rect.colliderect(zombie_rect):  # Vérifier la collision entre les deux rectangles
                ZManager.getZombies().remove(zombie)  # Supprimer le zombie touché
                print("Naah triple mooonstre")
                score += 1

    keystate = pygame.key.get_pressed()
    if(not launch):
        if keystate[K_LEFT]: # rotate conterclockwise
            
            alpha += 2
            if alpha > 360:
                alpha = 360
            canon_mouv = rot_center(canon_image, alpha)

        if keystate[K_RIGHT]: # rotate clockwise
            alpha-=2
            if alpha < 270:
                alpha = 270
            canon_mouv = rot_center(canon_image, alpha)

    # Dessiner le ciel
    screen.blit(bg, (0, 0))
    #screen.fill(sky_color)

    # Dessiner le sol
    pygame.draw.rect(screen, floor_color, (0, height - floor_height, width, floor_height))


    # Dessiner le score
    score_texte = font.render(f"Score: {score}", True, (0, 0, 0))

    screen.blit(score_texte, score_rect)


    # Dessiner le canon
    canon = pygame.image.load(brouette_path).convert_alpha()
    screen.blit(canon_mouv, rect_canon)
    screen.blit(canon, [25,height-floor_height-50])

    # Afficher les zombies
    ZManager.moveZombies()
    for zombax in ZManager.getZombies():
        screen.blit(zombie_image, (zombax.getPos()[0], zombax.getPos()[1]))

    # afficher les boulets
    if launch:
        indice_lancer+=15
        if indice_lancer<width:
            if not lancer(alpha, vitesse_initiale_lancer, g, indice_lancer, canon_pos[0], canon_pos[1])[1]>height-floor_height:
                test = lancer(alpha, vitesse_initiale_lancer, g, indice_lancer, canon_pos[0], canon_pos[1])
                screen.blit(nouveau_boulet, test)
            elif lancer(alpha, vitesse_initiale_lancer, g, indice_lancer, canon_pos[0], canon_pos[1])[1]>height-floor_height:
                launch=False
                nouveau_boulet=None
                nouveau_rect_boulet=None
                indice_lancer=75
        

    # Mettez à jour l'affichage
    pygame.display.flip()

    # Limitez la vitesse à 30 FPS
    clock.tick(30)
