import pygame
import sys

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

# Création de l'objet Clock
clock = pygame.time.Clock()

# paramètre du canon
alpha=45
v0=10

coord_canon=((100,100),(100,150),(125,150),(150,80))

# Boucle principale
while True:
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT and alpha<90:
                alpha+=5
            if event.key == pygame.K_LEFT and alpha<0:
                alpha-=5
            
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Déplacer le zombie vers la gauche
    zombie_pos[0] -= zombie_speed
    if zombie_pos[0] < 0:
        zombie_pos[0] = width - zombie_width

    # Dessiner le ciel
    screen.fill(sky_color)

    # Dessiner le sol
    pygame.draw.rect(screen, floor_color, (0, height - floor_height, width, floor_height))

    # Dessiner le canon
    pygame.draw.rect(screen, canon_color, (0, height-floor_height-50, 100,50))
    pygame.draw.polygon(screen, canon_color, coord_canon)

    # Afficher le zombie
    screen.blit(zombie_image, (zombie_pos[0], zombie_pos[1]))

    # Mettez à jour l'affichage
    pygame.display.flip()

    # Limitez la vitesse à 30 FPS
    clock.tick(30)
