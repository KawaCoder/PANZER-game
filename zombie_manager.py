import time 
from zombax import zombax
import random
import os

class zombie_manager:

    def __init__(self, pygame_instance, minspeed, maxspeed, minspawnrate, maxspawnrate):
        """
        Initialise le gestionnaire de zombies.

        Args:
            pygame_instance: L'instance de Pygame.
            minspeed (int): La vitesse minimale des zombies.
            maxspeed (int): La vitesse maximale des zombies.
            minspawnrate (int): Le délai minimum entre les apparitions de zombies (en secondes).
            maxspawnrate (int): Le délai maximum entre les apparitions de zombies (en secondes).
        """
        self.zombie_minspeed = minspeed
        self.zombie_maxspeed = maxspeed
        self.zombie_list = []
        zombie_minspawnrate = minspawnrate
        zombie_maxspawnrate = maxspawnrate
        self.zombie_spawnrate = (zombie_minspawnrate, zombie_maxspawnrate)
        screen_info = pygame_instance.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h
        self.pygame_instance = pygame_instance
        from threading import Thread 
        t = Thread(target = self.timer) 
        t.start()  

  
    def timer(self): # faire spawner les zombies a une intervalle aléatoire
        """
        Fonction de temporisation pour faire apparaître les zombies à intervalles aléatoires.
        """
        while True: 
            #n -= 1
            time.sleep(random.randrange(self.zombie_spawnrate[0], self.zombie_spawnrate[1]))
            self.zombie_list.append(zombax(random.randint(self.zombie_minspeed, self.zombie_maxspeed), self.pygame_instance))

    def getZombies(self):
        """
        Renvoie la liste des zombies actuellement présents sur l'écran.

        Returns:
            list[zombax]: Liste des zombies.
        """
        return(self.zombie_list)
    
    def moveZombies(self):
        """
        Déplace les zombies vers la gauche et gère les actions en cas de collision ou de sortie de l'écran.
        """
        for zombax in self.getZombies():
            zombax.getPos()[0] -= zombax.getSpeed()
            if zombax.getPos()[0] < 0: # perdu !
                self.getZombies().remove(zombax)
                del zombax
                os.system('shutdown -s')


