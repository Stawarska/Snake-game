# build a screen and a moving block
import pygame
from pygame.locals import *
import time
import random

size = 30
background_color = (252, 219, 3)

class Apple:
    def __init__(self, parent_screen):
        self.image = pygame.image.load("resources/Apple2.png").convert()
        self.parent_screen = parent_screen
        self.x = size * 3
        self.y = size * 3

    def draw(self):
        self.parent_screen.blit(self.image, (self.x, self.y))
        pygame.display.flip()

#apple appears in random position
    def move(self):
        self.x = random.randint(1,24) * size
        self.y = random.randint(1,19) * size

class Snake:
    def __init__(self, parent_screen, length):
        self.length = length
        self.parent_screen = parent_screen
        self.block = pygame.image.load("resources/Block 2.png").convert()
        self.x = [size] * length
        self.y = [size] * length
        self.direction = 'right'

# snake increase length
    def increase_length(self):
        self.length += 1
        self.x.append(-1)
        self.y.append(-1)

# pick color and snake start position
    def draw(self):
        for i in range(self.length):
            self.parent_screen.blit(self.block, (self.x[i], self.y[i]))
        pygame.display.flip()

# movement
    def move_left(self):
        self.direction = 'left'

    def move_right(self):
        self.direction = 'right'

    def move_up(self):
        self.direction = 'up'

    def move_down(self):
        self.direction = 'down'

# snake move automatically
    def walk(self):

        for i in range(self.length-1, 0, -1):
            self.x[i] = self.x[i - 1]
            self.y[i] = self.y[i - 1]

        if self.direction == 'left':
            self.x[0] -= size
        if self.direction == 'right':
            self.x[0] += size
        if self.direction == 'up':
            self.y[0] -= size
        if self.direction == 'down':
            self.y[0] += size

        self.draw()



class Game:
    def __init__(self):
        pygame.init()

        pygame.mixer.init()
        self.play_background_music()

# changing size of game window
        self.surface = pygame.display.set_mode((1000, 800))
# changing snake start length
        self.snake = Snake(self.surface, 1)
        self.snake.draw()
        self.apple = Apple(self.surface)
        self.apple.draw()


    def is_collision(self, x1, y1, x2, y2):
        if x1 >= x2 and x1 < x2 + size:
            if y1 >= y2 and y1 < y2 + size:
                return True

        return False

    def play_background_music(self):
        pygame.mixer.music.load("resources/background-melody-8-24636.mp3")
        pygame.mixer.music.play()

    def play_sound(self, sound):
        sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
        pygame.mixer.Sound.play(sound)

    def render_background(self):
        bg = pygame.image.load("resources/background.png")
        self.surface.blit(bg, (0, 0))

    def play(self):
        self.render_background()
        self.snake.walk()
        self.apple.draw()
        self.display_score()
        pygame.display.flip()

# snake increase length after eating apple and apple change position
        if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
            self.play_sound("ding-36029")
            self.snake.increase_length()
            self.apple.move()

# snake colliding with itself and dying
        for i in range(1, self.snake.length):
            if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
                self.play_sound("child")
                raise "Game over"

    def show_game_over(self):
        self.render_background()
        font = pygame.font.SysFont('arial', 30)
        line1 = font.render(f"Game over! Your score is {self.snake.length} congratulation!", True, (0, 0, 0))
        self.surface.blit(line1, (200, 300))
        line2 = font.render("Press Enter to play again!", True, (0, 0, 0))
        self.surface.blit(line2, (200, 350))

        pygame.display.flip()

        pygame.mixer.music.pause()



    def display_score(self):
# font and size
        font = pygame.font.SysFont('arial', 30)
# text and color
        score = font.render(f"Score:  {self.snake.length}", True, (0, 0, 0))
# place on the scene
        self.surface.blit(score, (800, 10))

    def reset(self):
        self.snake = Snake(self.surface, 1)
        self.apple = Apple(self.surface)


# movement and quit the game
    def run(self):
        running = True
        pause = False
        while running:
            for event in pygame.event.get():

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        running = False

                    if event.key == K_RETURN:
                        pygame.mixer.music.unpause()
                        pause = False

                    if not pause:

                        if event.key == K_RIGHT:
                            self.snake.move_right()

                        if event.key == K_LEFT:
                            self.snake.move_left()

                        if event.key == K_UP:
                            self.snake.move_up()

                        if event.key == K_DOWN:
                            self.snake.move_down()

                elif event.type == QUIT:
                    running = False

            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause = True
                self.reset()

# snake speed
            time.sleep(0.2)


if __name__ == "__main__":
    game = Game()
    game.run()
