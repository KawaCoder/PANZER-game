import time 
from zombax import zombax
class zombie_manager:

    def __init__(self, pygame_instance):
        self.zombie_speed = 2
        self.zombie_list = []
        screen_info = pygame_instance.display.Info()
        self.width, self.height = screen_info.current_w, screen_info.current_h
        self.pygame_instance = pygame_instance
        from threading import Thread 
        t = Thread(target = self.timer, args =(10, )) 
        t.start()  
  
    def timer(self, n): 
        while n > 0: 
            n -= 1
            time.sleep(3)
            self.zombie_list.append(zombax(self.zombie_speed, self.pygame_instance))
            
    def getZombies(self):
        return(self.zombie_list)
    
    def moveZombies(self):
        for zombax in self.getZombies():
            zombax.getPos()[0] -= zombax.getSpeed()
            if zombax.getPos()[0] < 0:
                zombax.getPos()[0] = self.width - zombax.getWidth()
