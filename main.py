import pygame
import sys
from zombie_manager import zombie_manager
from zombax import zombax
from pygame.locals import *


# Initialisation de Pygame
pygame.init()

# Obtenez les dimensions de l'écran
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Paramètres de la fenêtre
floor_height = 100  # Hauteur du sol
floor_color = (34, 139, 34)  # Vert foncé (couleur de l'herbe)
sky_color = (0, 255, 255)  # Cyan (couleur du ciel)
canon_color = (132, 132, 132) # gris (couleur du canon)

# Paramètres du zombie
zombie_image_path = "assets/zombax/zombie.png"
zombie_width, zombie_height = 50, 50
zombie_speed = 5
zombie_pos = [width - zombie_width, height - floor_height - zombie_height]

# Création de la fenêtre en plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)
pygame.display.set_caption("Mon jeu Pygame - Zombie Shooter")

# Chargement de l'image du zombie
zombie_image = pygame.image.load(zombie_image_path)
zombie_image = pygame.transform.scale(zombie_image, (zombie_width, zombie_height))

# Paramètre du canon 
canon_image_path = "assets/canon/canon_tuyaux.png"
canon_width, canon_height = 50, 100
canon_pos = [75,height-floor_height-100]
a = pygame.draw.rect(screen, (0,0,0), (150,150,150,150))


# Chargement de l'image du canon
canon_image = pygame.image.load(canon_image_path).convert_alpha()
cannon_image = pygame.transform.rotate(canon_image, -80)
rect_canon = canon_image.get_rect(center=(canon_pos))

# Création de l'objet Clock
clock = pygame.time.Clock()

# paramètre du lancer
alpha=315
vitesse_initiale_lancer=10


# Gestion du Zombax
ZManager = zombie_manager(pygame)
print(ZManager.getZombies())



# Gestion du Zombax
ZManager = zombie_manager(pygame)
print(ZManager.getZombies())


def rot_center(image, angle):
    rect_origine = image.get_rect()
    rotate_image = pygame.transform.rotate(image, angle)
    rotate_rect = rect_origine.copy()
    rotate_rect.center = rotate_image.get_rect().center
    rotate_image = rotate_image.subsurface(rotate_rect).copy()
    return rotate_image
canon_mouv = rot_center(canon_image, alpha)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:

            if event.key == pygame.K_UP:
                print(ZManager.getZombies())
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    keystate = pygame.key.get_pressed()

    if keystate[K_LEFT]: # rotate conterclockwise
        alpha+=2
        if alpha > 360:
            alpha = 360
        canon_mouv = rot_center(canon_image, alpha)

    if keystate[K_RIGHT]: # rotate clockwise
        alpha-=2
        if alpha < 270:
            alpha = 270
        canon_mouv = rot_center(canon_image, alpha)

    # Déplacer le zombie vers la gauche
    zombie_pos[0] -= zombie_speed
    if zombie_pos[0] < 0:
        zombie_pos[0] = width - zombie_width

    # Dessiner le ciel
    screen.fill(sky_color)

    # Dessiner le sol
    pygame.draw.rect(screen, floor_color, (0, height - floor_height, width, floor_height))

    # Dessiner le canon
    pygame.draw.rect(screen, canon_color, (50, height-floor_height-50, 100,50))
    screen.blit(canon_mouv, rect_canon)
    

    # Afficher le zombie
    screen.blit(zombie_image, (zombie_pos[0], zombie_pos[1]))

    # Mettez à jour l'affichage
    pygame.display.flip()

    # Limitez la vitesse à 30 FPS
    clock.tick(30)
