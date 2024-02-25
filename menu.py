import pygame
import sys

class Menu:
    def __init__(self):
        # Initialisation de Pygame
        pygame.init()

        # Paramètres de la fenêtre
        screen_info = pygame.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height), pygame.FULLSCREEN)  # Utilisez self.width et self.height
        pygame.display.set_caption("Menu d'accueil")

        # Couleurs
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)

        # Police de texte
        self.font = pygame.font.SysFont(None, 50)

        # Variables pour les rectangles des boutons
        self.demarrer_rect = None
        self.quitter_rect = None

    def afficher_menu(self):
        self.screen.fill(self.WHITE)
        
        # Titre du jeu
        titre_texte = self.font.render("PANZER", True, self.RED)
        titre_rect = titre_texte.get_rect(center=(self.width//2, self.height//3))
        self.screen.blit(titre_texte, titre_rect)
        
        # Bouton de démarrage
        demarrer_texte = self.font.render("Démarrer", True, self.BLACK)
        self.demarrer_rect = demarrer_texte.get_rect(center=(self.width//2, self.height//2))
        self.screen.blit(demarrer_texte, self.demarrer_rect)
        
        # Bouton de quitter
        quitter_texte = self.font.render("Quitter", True, self.BLACK)
        self.quitter_rect = quitter_texte.get_rect(center=(self.width//2, self.height//1.5))
        self.screen.blit(quitter_texte, self.quitter_rect)
        
        pygame.display.flip()

    def menu(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    # Vérifie si le clic est sur le bouton "Démarrer"
                    if self.demarrer_rect.collidepoint(event.pos):
                        # Lancer le jeu ou passer à l'écran de jeu
                        return True
                        pygame.quit()
                    # Vérifie si le clic est sur le bouton "Quitter"
                    elif self.quitter_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            self.afficher_menu()
