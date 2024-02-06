import time 
from zombax import zombax
class zombie_manager:

    def __init__(self, pygame_instance):
        self.zombie_list = []
        self.pygame_instance = pygame_instance
        from threading import Thread 
        t = Thread(target = self.timer, args =(10, )) 
        t.start()  
  
    def timer(self, n): 
        while n > 0: 
            n -= 1
            time.sleep(3)
            self.zombie_list.append(zombax(self.pygame_instance))
            
    def getZombies(self):
        return(self.zombie_list)