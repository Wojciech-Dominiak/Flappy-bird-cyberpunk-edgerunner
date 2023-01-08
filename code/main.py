import pygame, sys, time
from settings import *
from sprites import BG, Ground, Plane, Obstacle
from random import choice

class Game: 
    def __init__(self):

        #setup
        pygame.init()
        #to mozna wywalic na dole
        pygame.mixer.init()
        self.display_surface = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
        pygame.display.set_caption("Cyber Flap")
        self.clock = pygame.time.Clock()
        self.active = False
        

        #sprite groups
        self.all_sprites = pygame.sprite.Group()
        self.collision_sprites = pygame.sprite.Group()


        #scale factor - skalowanie obrazka
        bg_height = pygame.image.load('./imgs/bg.png').get_height()
        self.scale_factor = WINDOW_HEIGHT/ bg_height

        #sprite setup
        BG(self.all_sprites, self.scale_factor)
        Ground([self.all_sprites, self.collision_sprites], self.scale_factor)
        self.plane = Plane(self.all_sprites, self.scale_factor / 1.2)
        self.plane.kill()

        #timer
        self.obstacle_timer = pygame.USEREVENT + 1
        pygame.time.set_timer(self.obstacle_timer, 1400)

        #text
        self.font = pygame.font.Font('./imgs/font.ttf', 40)
        self.score = 0
        self.start_offset = 0

        #menu
        self.menu_surf = pygame.image.load('./imgs/menu.png').convert_alpha()
        self.menu_rect = self.menu_surf.get_rect(center = (WINDOW_WIDTH/2, WINDOW_HEIGHT/2 ))

        #music
        # self.music = pygame.mixer.Sound("./imgs/sounds/background.wav") f"./imgs/pipes/{choice([0, 1])}.png"
        # self.music = pygame.mixer.Sound(f"./imgs/sounds/background/{choice([0, 1, 2, 3])}.wav")
        # self.music.set_volume(0.20)
        # self.music.play(loops=-1)
        pygame.mixer.music.load(f"./imgs/sounds/background/{choice([0, 1, 2, 3, 4])}.wav")
        pygame.mixer.music.set_volume(0.20)
        pygame.mixer.music.play(loops=-1)
            
        # else:
        #     self.music.stop()

    def collisions(self):
        if pygame.sprite.spritecollide(self.plane, self.collision_sprites, False, pygame.sprite.collide_mask)\
        or self.plane.rect.top <= 0:
            for sprite in self.collision_sprites.sprites():
                if sprite.sprite_type == "obstacle":
                    sprite.kill()
            self.active = False
            self.plane.kill()

    def display_score(self):
        if self.active:
            self.score = (pygame.time.get_ticks() - self.start_offset) // 1000
            y = WINDOW_HEIGHT / 10
        else:
            y = WINDOW_HEIGHT / 2 + (self.menu_rect.height / 2)

        score_surf = self.font.render(f"Time on sandevistan:  {self.score} s", True, "Yellow")

        score_rect = score_surf.get_rect(midtop = (WINDOW_WIDTH/2 , y))

        self.display_surface.blit(score_surf, score_rect)

    def run(self):
        last_time = time.time()
        while True:
            #delta time
            dt = time.time() - last_time
            last_time = time.time()
            
            #event loop
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if self.active:
                        self.plane.jump()
                    else:
                        self.plane = Plane(self.all_sprites, self.scale_factor / 1.2)
                        self.active = True
                        pygame.mixer.music.load(f"./imgs/sounds/background/{choice([0, 1, 2, 3, 4])}.wav")
                        pygame.mixer.music.play(loops=-1)
                        self.start_offset = pygame.time.get_ticks()
                    
                if event.type == self.obstacle_timer and self.active:
                    Obstacle([self.all_sprites, self.collision_sprites], self.scale_factor * 1.35)

            #game logic
            #self.display_surface.fill("black")
            self.all_sprites.update(dt)
            self.all_sprites.draw(self.display_surface)
            self.display_score()
    

            if self.active:
                self.collisions()

            else:
                pygame.mixer.music.stop()
                self.display_surface.blit(self.menu_surf, self.menu_rect)

            pygame.display.update()
            self.clock.tick(FRAMERATE)



if __name__ == '__main__':
    game = Game()
    game.run()