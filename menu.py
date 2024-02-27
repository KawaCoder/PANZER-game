import pygame
import sys
import os

class Menu:
    def __init__(self):
        pygame.init()

        # Initialize screen
        screen_info = pygame.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h
        self.screen = pygame.display.set_mode((self.width, self.height))
        pygame.display.set_caption("Menu d'accueil")

        # RTX logo
        self.rtx_logo = pygame.image.load("assets/RTX.png")
        self.rtx_logo = pygame.transform.scale(self.rtx_logo, (140, 110))
        
        self.rtx_position = (self.width // 1.4, self.height // 1.8)
        self.rtx_rect = self.rtx_logo.get_rect(center=self.rtx_position)

        # Load frames
        self.gif_frames = []
        frames_directory = "assets/frames_output"  # Directory containing individual frames
        for filename in sorted(os.listdir(frames_directory)):
            frame_path = os.path.join(frames_directory, filename)
            if frame_path.endswith('.png'):
                frame_image = pygame.image.load(frame_path).convert_alpha()  # Load frame
                frame_image = pygame.transform.scale(frame_image, (self.width, self.height))
                
                self.gif_frames.append(frame_image)

        # Initialize frame index
        self.frame_index = 0
        self.frame_count = len(self.gif_frames)

        # Colors
        self.WHITE = (255, 255, 255)
        self.BLACK = (0, 0, 0)
        self.RED = (255, 0, 0)
        self.GREEN = (0, 255, 0)

        # Font
        self.font = pygame.font.SysFont(None, 50)

        # Button rectangles
        self.demarrer_rect = None
        self.quitter_rect = None

    def afficher_menu(self):
        # Display current frame
        self.screen.blit(self.gif_frames[self.frame_index], (0, 0))
        self.frame_index = (self.frame_index + 1) % self.frame_count

        # Start button
        demarrer_texte = self.font.render("Démarrer", True, self.RED)
        self.demarrer_rect = demarrer_texte.get_rect(center=(self.width // 2, self.height // 2))
        self.screen.blit(demarrer_texte, self.demarrer_rect)

        # Start button SHADERS
        self.screen.blit(self.rtx_logo, self.rtx_rect)
        demarrer_rtx_texte = self.font.render("Démarrer avec Nvidia RTX", True, self.GREEN)
        self.demarrer_rtx_rect = demarrer_rtx_texte.get_rect(center=(self.width // 2, self.height // 1.7))
        self.screen.blit(demarrer_rtx_texte, self.demarrer_rtx_rect)

        # Quit button
        quitter_texte = self.font.render("Quitter", True, self.BLACK)
        self.quitter_rect = quitter_texte.get_rect(center=(self.width // 2, self.height // 1.3))
        self.screen.blit(quitter_texte, self.quitter_rect)

        pygame.display.flip()

    def menu(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    if self.demarrer_rect.collidepoint(event.pos):
                        return(False)
                    elif self.demarrer_rtx_rect.collidepoint(event.pos):
                        return(True)
                    elif self.quitter_rect.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

            clock.tick(20)
            self.afficher_menu()

