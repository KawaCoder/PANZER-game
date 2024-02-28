class zombax:
    def __init__(self, speed, pygame_instance):
        self.health = 100
        screen_info = pygame_instance.display.Info()
        width, height = screen_info.current_w, screen_info.current_h
        self.floor_height = 250  # Hauteur du sol
        self.zombie_width, zombie_height = 50, 50
        self.zombie_speed = speed
        self.zombie_pos = [width - self.zombie_width, height - self.floor_height - zombie_height]

    def getPos(self):
        return(self.zombie_pos)
    
    def getSpeed(self):
        return(self.zombie_speed)
    
    def getWidth(self):
        return(self.zombie_width)
    
    def getHealth(self):
        return(self.health)