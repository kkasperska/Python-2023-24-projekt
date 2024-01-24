import json
import random
import pygame

class Button:
    def __init__(self, x, y, color, size, flash):
        self.x = x
        self.y = y
        self.color = color
        self.size = size
        self.flash = flash

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, (self.x, self.y, self.size, self.size))

    def is_clicked(self, mouse_x, mouse_y):
        return (self.x <= mouse_x <= (self.x + self.size) and
                self.y <= mouse_y <= (self.y + self.size))
    
    #funkcja wzorowana na
    # https://stackoverflow.com/questions/54593653/how-to-fade-in-a-text-or-an-image-with-pygame?noredirect=1&lq=1
    def animation(self, game, animation_speed, fps, clock):
        flash_surface = pygame.Surface((self.size, self.size))
        button_surface = pygame.Surface((self.size, self.size))
        button_surface.fill(self.color)
        flash_surface.fill(self.flash)
        game.button_sound.play()
        for start, end, step in ((0, 255, 1), (255, 0, -1)):
            for alpha in range(start, end, animation_speed * step):
                game.screen.blit(button_surface, (self.x, self.y))
                flash_surface.set_alpha(alpha)
                game.screen.blit(flash_surface, (self.x, self.y))
                clock.tick(fps)
                pygame.display.update()
        game.screen.blit(button_surface, (self.x, self.y))
        
        

class Game:
    def __init__(self, data):
        self.data = data
        pygame.init()
        self.screen = pygame.display.set_mode((self.data["width"], self.data["height"]))
        pygame.display.set_caption(self.data["name"])
        self.clock = pygame.time.Clock()
        self.flash_colors = [self.data["colors"]["B1"],
                             self.data["colors"]["B2"],
                             self.data["colors"]["B3"],
                             self.data["colors"]["B4"],
                             self.data["colors"]["B5"],
                             self.data["colors"]["B6"],
                             self.data["colors"]["B7"],
                             self.data["colors"]["B8"],
                             self.data["colors"]["B9"]]
        self.color = self.data["colors"]["GREY"]
        self.button_sound = pygame.mixer.Sound("assets/click-button-140881.mp3")
        self.game_over_sound = pygame.mixer.Sound("assets/error-call-to-attention-129258.mp3")
        self.new_high_score_sound = pygame.mixer.Sound("assets/new-level-142995.mp3")

        self.buttons_computer = []
        self.buttons_player = []
        
        start_y = 100
        a = 1
        for i in range(1, 8, 3):
            start_x = 100
            for j in range(1, 4):    
               button = Button(start_x, start_y, self.color,
                               self.data["button_size_left"],
                               self.flash_colors[j+i-2])
               self.buttons_computer.append(button)
               start_x += self.data["button_size_left"]
            start_y += self.data["button_size_left"]
            
        x0 = start_x + 40
        start_y = 100
        a = 1
        for i in range(1, 8, 3):
            start_x = x0
            for j in range(1, 4):    
               button = Button(start_x, start_y, self.color,
                               self.data["button_size_right"],
                               self.flash_colors[j+i-2])
               self.buttons_player.append(button)
               start_x += self.data["button_size_right"] + 10
            start_y += self.data["button_size_right"] + 10
    
    def get_high_score(self):
        with open("assets/high_score.txt", "r") as file:
            score = file.read()
        return int(score)
    
    def set_high_score(self):
        with open("assets/high_score.txt", "w") as output:
            output.write(str(self.score))

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                if self.score > self.high_score:
                        self.set_high_score()
                pygame.quit()
                quit(0)

            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                for button in self.buttons_player:
                    if button.is_clicked(mouse_x, mouse_y):
                        self.clicked_button = button

    def draw(self):
        font = pygame.font.Font("assets/Federant-Regular.ttf", 32)
        self.screen.fill(self.data["colors"]["LIGHTGREY"])
        text_sc = font.render(f"Score: {str(self.score)}", False,
                              self.data["colors"]["lower_text_color"])
        self.screen.blit(text_sc, (357, 750))
        text_hisc = font.render(f"High score: {str(self.high_score)}", False,
                                self.data["colors"]["lower_text_color"])
        self.screen.blit(text_hisc, (990, 750))
        text_seq = font.render("Sequence", False,
                               self.data["colors"]["upper_text_color"])
        self.screen.blit(text_seq, (345, 50))
        text_pl = font.render("Player", False,
                              self.data["colors"]["upper_text_color"])
        self.screen.blit(text_pl, (1030, 50))
        for button in self.buttons_computer:
            button.draw(self.screen)
        for button in self.buttons_player:
            button.draw(self.screen)
        pygame.display.update()
         
    def new(self):
        self.waiting_input = False
        self.pattern = []
        self.step = 0
        self.score = 0
        self.high_score = self.get_high_score()
        
    def update(self):
        pygame.event.set_blocked(pygame.MOUSEBUTTONDOWN)
        if not self.waiting_input:
            pygame.time.wait(1000)
            self.pattern.append(random.choice(self.buttons_computer))
            for button in self.pattern:
                button.animation(self, self.data["button_animation_speed"],
                                 self.data["fps"], self.clock)
                pygame.time.wait(200)
            self.waiting_input = True
        
        else:
            pygame.event.set_allowed(pygame.MOUSEBUTTONDOWN)
            if (self.clicked_button and
                self.buttons_player.index(self.clicked_button)
                == self.buttons_computer.index(self.pattern[self.step])):
                self.clicked_button.animation(self,
                                              self.data["button_animation_speed"],
                                              self.data["fps"], self.clock)
                self.step += 1

                if self.step == len(self.pattern):
                    self.score += 1
                    if self.score == self.high_score + 1:
                        self.new_high_score_sound.play()
                    self.waiting_input = False
                    self.step = 0
            elif (self.clicked_button and
                  self.buttons_player.index(self.clicked_button)
                  != self.buttons_computer.index(self.pattern[self.step])):
                    self.clicked_button.animation(self,
                                                  self.data["button_animation_speed"],
                                                  self.data["fps"], self.clock)
                    self.playing = False
                    pygame.time.wait(200)
                    self.game_over_animation()
                    if self.score > self.high_score:
                        self.set_high_score()

    #funkcja wzorowana na
    # https://stackoverflow.com/questions/54593653/how-to-fade-in-a-text-or-an-image-with-pygame?noredirect=1&lq=1
    def game_over_animation(self):
        self.game_over_sound.play()
        original_surface = self.screen.copy()
        flash_surface = pygame.Surface((self.screen.get_size()))
        flash_surface = flash_surface.convert_alpha()
        flash_surface.fill(self.data["colors"]["FLASH"])
        for _ in range(2):
            for start, end, step in ((0, 255, 1), (255, 0, -1)):
                for alpha in range(start, end, self.data["game_over_animation_speed"] * step):
                    self.screen.blit(original_surface, (0, 0))
                    flash_surface.set_alpha(alpha)
                    self.screen.blit(flash_surface, (0, 0))
                    self.clock.tick(self.data["fps"])
                    pygame.display.update()
                    
                    
    def run(self):
        self.playing = True
        while self.playing:
            self.clock.tick(self.data["fps"])
            self.clicked_button = None
            self.events()
            self.draw()
            self.update()


def main():
    with open("assets/settings.json") as config_file:
            data = json.load(config_file)
    game = Game(data)
    while True:
        game.new()
        game.run()    

main()