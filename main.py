import pygame
import sys
from zombie_manager import zombie_manager
from zombax import zombax
from pygame.locals import *
import math
import time as t
from menu import Menu
import random

afficher_hitbox = False

menu = Menu()
rtx = menu.menu()

if(rtx):
    # Chemins de fichiers des assets
    herbe_path = "assets/bg/herbe.jpeg"
    brouette_path = "assets/canon/brouette.png"
    rtx_on_path = "assets/rtx_on.png"
    canon_image_path = "assets/canon/canon_tuyaux.png"
    boulet_image_path = "assets/canon/boulet.png"
    TWINGO_path = "assets/canon/twingo.png"
    hitmarker_path = "assets/hitmarker.png"
    ciel_path = "assets/bg/ciel_shader.jpg"
    zombie_image_path = "assets/zombax/nazi_shader.png"
    canon_sound_path = "assets/canon.mp3"

    # Chargement de l'image RTX
    rtx_on = pygame.image.load(rtx_on_path)
    rtx_on = pygame.transform.scale(rtx_on, (200, 100))

else:
    # Chemins de fichiers des assets
    herbe_path = "assets/bg/herbe.jpeg"
    brouette_path = "assets/canon/brouette.png"
    canon_image_path = "assets/canon/canon_tuyaux.png"
    boulet_image_path = "assets/canon/boulet.png"
    TWINGO_path = "assets/canon/twingo.png"
    hitmarker_path = "assets/hitmarker.png"
    ciel_path = "assets/bg/ciel.png"
    zombie_image_path = "assets/zombax/nazi.png"
    canon_sound_path = "assets/canon.mp3"

# Initialisation de Pygame
pygame.init()

# Paramètres du jeu
minspeed = 2
maxspeed = 5
minspawnrate = 1
maxspawnrate = 4

# Obtenir les dimensions de l'écran
screen_info = pygame.display.Info()
width, height = screen_info.current_w, screen_info.current_h

# Paramètres de la fenêtre
floor_height = 100  # Hauteur du sol
floor_color = (34, 139, 34)  # Vert foncé (couleur de l'herbe)
sky_color = (0, 255, 255)  # Cyan (couleur du ciel)
canon_color = (132, 132, 132) # gris (couleur du canon)

if(rtx):
    # Position du rtx_on
    rtx_on_pos = (87, 200)
    rtx_rect = rtx_on.get_rect(center=(rtx_on_pos))


# Initialisation du mixeur
pygame.mixer.init()
pygame.mixer.music.load(canon_sound_path)

# Création de la fenêtre en plein écran
screen = pygame.display.set_mode((width, height), pygame.FULLSCREEN)  # Utilisez self.width et self.height
pygame.display.set_caption("Mon jeu Pygame - Zombie Shooter")

# Chargement de l'image du zombie
zombie_image = pygame.image.load(zombie_image_path)
zombie_image = pygame.transform.scale(zombie_image, (250, 250))

# Paramètre du canon 
canon_width, canon_height = 50, 100
canon_pos = [100,height-floor_height-50]
a = pygame.draw.rect(screen, (0,0,0), (150,150,150,150))

g=9.8
launch=False

# Score
score = 0

# Chargement de l'image du canon
canon_image = pygame.image.load(canon_image_path).convert_alpha()
rect_canon = canon_image.get_rect(center=(canon_pos))

# Chargement de l'image du hitmarker
hit_image = pygame.image.load(hitmarker_path)
hit_image = pygame.transform.scale(hit_image, (50, 50))

# Chargement de l'image de fond
bg = pygame.image.load(ciel_path)
bg = pygame.transform.scale(bg, (width, height))

# Chargement de l'herbe
herbe = pygame.image.load(herbe_path)
herbe = pygame.transform.scale(herbe, (width, 200))
herbe_rect = herbe.get_rect(center=(width // 2, height))

# Chargement de l'image de la brouette
canon = pygame.image.load(brouette_path).convert_alpha()

# Création de l'objet Clock
clock = pygame.time.Clock()

# paramètre du lancer
alpha=315
vitesse_initiale_lancer=100

# Texte du score
font = pygame.font.SysFont(None, 75)
score_texte = font.render("Score: ", True, (0, 0, 0))
score_rect = score_texte.get_rect(center=(100, 100))

# Gestion du Zombie triple mooonstre
# Paramètres de la fenêtre
floor_height = 100  # Hautembax
ZManager = zombie_manager(pygame, minspeed, maxspeed, minspawnrate, maxspawnrate)

# fonction pour faire une rotation propre sans devenir un TUC
def rot_center(image, angle):
    """
    Fait pivoter une image autour de son centre.

    Args:
        image (pygame.Surface): L'image à faire pivoter.
        angle (float): L'angle de rotation en degrés.

    Returns:
        pygame.Surface: L'image pivotée.
    """
    rect_origine = image.get_rect()
    rotate_image = pygame.transform.rotate(image, angle)
    rotate_rect = rect_origine.copy()
    rotate_rect.center = rotate_image.get_rect().center
    rotate_image = rotate_image.subsurface(rotate_rect).copy()
    return rotate_image
canon_mouv = rot_center(canon_image, alpha)


# fonction pour créer un boulet (pour eviter de reset un boulet déjà lancé)
def creation_boulet():
    """
    Crée un boulet pour le canon.

    Returns:
        Tuple[pygame.Surface, pygame.Rect]: L'image du boulet et son rectangle de collision.
    """
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

position_boulet = [0, 0]
def lancer(alpha, v0, g, x, w0, h0):
    """
    Calcule la position d'un projectile lancé.

    Args:
        alpha (float): L'angle de tir en degrés.
        v0 (float): La vitesse initiale du projectile.
        g (float): L'accélération due à la gravité.
        x (int): La position horizontale actuelle du projectile.
        w0 (int): La position horizontale initiale du canon.
        h0 (int): La position verticale initiale du canon.

    Returns:
        Tuple[int, int]: Les coordonnées (x, y) du projectile.
    """
    # Convertir l'angle alpha en radians
    alpha = math.radians(alpha)
    alpha = - alpha
    y=(1/2)*g*((x-w0)/(v0*math.sin(alpha)))**2-(v0*math.cos(alpha))*((x-w0)/(v0*math.sin(alpha)))+h0
    coord_boulet=(x,y)
    return coord_boulet
indice_lancer=75

compteur_hitmark = 0
position_hitmark = (34, 0)

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if(not launch):
                    pygame.mixer.music.play()
                    pygame.event.wait()
                    if random.randint(0,5) == 1:
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
            zombie_x, zombie_y = zombie.getPos()
            zombie_rect = pygame.Rect(zombie_x+(250-130)//2, zombie_y, 130, 200)
            boulet_rect = pygame.Rect(position_boulet[0], position_boulet[1], 30, 30)
            if boulet_rect.colliderect(zombie_rect):  # Vérifier la collision entre les deux rectangles
                position_hitmark = (zombie_x+50, zombie_y+35)
                compteur_hitmark = 10
                score += 1
                ZManager.getZombies().remove(zombie)  # Supprimer le zombie touché
                print("boulet:", position_boulet, " zombax:",zombie_x, zombie_y )

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

    # Dessiner le sol
    if(rtx):
        screen.blit(herbe, herbe_rect)
    else:
        pygame.draw.rect(screen, floor_color, (0, height - floor_height, width, floor_height))

    # Afficher le RTX_on
    if(rtx):
        screen.blit(rtx_on, rtx_rect)


    # Dessiner le score
    score_texte = font.render(f"Score: {score}", True, (0, 0, 0))
    screen.blit(score_texte, score_rect)

    # Afficher le canon
    screen.blit(canon_mouv, rect_canon)
    screen.blit(canon, [25,height-floor_height-50])

    # Afficher le hitmark
    if(compteur_hitmark>0):
        compteur_hitmark -= 1
        screen.blit(hit_image, position_hitmark)

    # Afficher les zombies
    ZManager.moveZombies()
    for zombax in ZManager.getZombies():
        if(afficher_hitbox):
            zombie_x, zombie_y = zombax.getPos()
            pygame.draw.rect(screen, floor_color, (zombie_x+(250-130)//2, zombie_y, 130, 200))
        screen.blit(zombie_image, (zombax.getPos()[0], zombax.getPos()[1]))

    # afficher les boulets
    if launch:
        indice_lancer+=15
        if indice_lancer<width:
            if not lancer(alpha, vitesse_initiale_lancer, g, indice_lancer, canon_pos[0], canon_pos[1])[1]>height-floor_height:
                position_boulet = lancer(alpha, vitesse_initiale_lancer, g, indice_lancer, canon_pos[0], canon_pos[1])
                screen.blit(nouveau_boulet, position_boulet)
            elif lancer(alpha, vitesse_initiale_lancer, g, indice_lancer, canon_pos[0], canon_pos[1])[1]>height-floor_height:
                launch=False
                nouveau_boulet=None
                nouveau_rect_boulet=None
                indice_lancer=75
                position_boulet = [0, 0]
        

    # Mettez à jour l'affichage
    pygame.display.flip()

    # Limitez la vitesse à 30 FPS
    clock.tick(30)
