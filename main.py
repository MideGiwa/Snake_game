import pygame
from pygame.locals import *
import time
import random

SIZE = 40
BACKGROUND_COLOR = (110, 110, 5)

class Apple:
	def __init__(self, parent_screen):
		self.image = pygame.image.load("resources/apple2.jpg").convert()
		self.parent_screen = parent_screen
		self.x = SIZE * 3
		self.y = SIZE * 3

	# draws apple...
	def draw(self):
		self.parent_screen.blit(self.image,(self.x, self.y))
		pygame.display.flip()

	# moves apple after collision
	def move(self):
		self.x = random.randint(0, 24) * SIZE
		self.y = random.randint(0, 16) * SIZE

	# draw big apple,(bonus)...
	def draw_big_apple(self):
		self.big_apple = pygame.image.load("resouces/apple.jpg").convert()
		self.big_apple = pygame.transform.smoothscale(self.big_apple, (80, 80))
		self.surface.blit(self.big_apple, (random.randint(0, 11) * 80, random.randint(0, 9) * 80))

class Snake:
	# creating block snake...
	def __init__(self, parent_screen, length):
		self.length = length
		self.parent_screen = parent_screen
		self.block = pygame.image.load("resources/block.jpg").convert()
		self.x = [SIZE] * length
		self.y = [SIZE] * length
		self.direction = 'down'
		self.speed = 0.6
		self.level = 1

	# increases snake length after collision...
	def increase_length(self):
		self.length+=1
		self.x.append(-1)
		self.y.append(-1)
	# increases level and speed...
		if self.length % 5 == 0 and self.speed != 0:
			self.level += 1
			self.speed -= 0.2

	def move_left(self):
		self.direction = 'left'

	def move_right(self):
		self.direction = 'right'

	def move_up(self):
		self.direction = 'up'

	def move_down(self):
		self.direction = 'down'

	# draws snake on screen...
	def draw(self):
		for i in range(self.length):
			self.parent_screen.blit(self.block,(self.x[i], self.y[i]))
		pygame.display.flip()

	# puts snake in a continuous motion...
	def walk(self):

		for i in range(self.length - 1, 0, -1):
			self.x[i] = self.x[i - 1]
			self.y[i] = self.y[i - 1]

		if self.direction == 'left':
			self.x[0] -= SIZE

		if self.direction == 'right':
			self.x[0] += SIZE

		if self.direction == 'up':
			self.y[0] -= SIZE

		if self.direction == 'down':
			self.y[0] += SIZE

		self.draw()
		
	
class Game:
	def __init__(self):
		# initializing pygame and pygame's music module...
		pygame.init()
		pygame.mixer.init()


		self.play_background_music()
		self.surface = pygame.display.set_mode((1000, 720))
		self.snake = Snake(self.surface, 1)
		self.snake.draw()
		self.apple = Apple(self.surface)
		self.apple.draw()

	def is_collision(self, x1, y1, x2, y2):
		if x1 >= x2 and x1 < x2 + SIZE:
			if y1 >= y2 and y1 < y2 + SIZE:
				return True

		return False
	def display_big_apple(self):
		if self.snake.level == 2:
				self.apple.draw_big_apple()
				#if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y)

	def barrier(self, x, y):
		if x < 0 or x > 960:
			return True
		if y < 0 or y > 680:
			return True

	def play_sound(self, sound):
		sound = pygame.mixer.Sound(f"resources/{sound}.mp3")
		pygame.mixer.Sound.play(sound)
		

	def play_background_music(self):
		pygame.mixer.music.load("resources/bg_music_1.mp3")
		pygame.mixer.music.play()


	def render_background(self):
		bg = pygame.image.load("resources/background.jpg")
		self.surface.blit(bg, (0, 0))


	def play(self):
		self.render_background()
		self.snake.walk()
		self.apple.draw()
		self.display_score()
		self.display_level()
		#self.display_big_apple()
		pygame.display.flip()

		if self.is_collision(self.snake.x[0], self.snake.y[0], self.apple.x, self.apple.y):
			self.play_sound("ding")
			self.snake.increase_length()
			self.apple.move()

		if self.barrier(self.snake.x[0], self.snake.y[0]):
			self.play_sound("crash")
			raise "Game Over"
		for i in range(3, self.snake.length):
			 if self.is_collision(self.snake.x[0], self.snake.y[0], self.snake.x[i], self.snake.y[i]):
			 	self.play_sound("crash")
			 	raise "Game Over"

	def show_pause_screen(self):
		image = pygame.Surface([640, 480], pygame.SRCALPHA, 32)
		image = image.convert_alpha()
		font = pygame.font.SysFont('', 40)
		text1 = font.render("Paused.", True, (0, 0, 0))
		self.surface.blit(text1, (420, 300))
		text2 = font.render(f"Score: {self.snake.length}", True, (0, 0, 0))
		self.surface.blit(text2, (420, 350))
		text3 = font.render(f"Hit the SPACE BAR to resume the game.", True, (0, 0, 0))
		self.surface.blit(text3, (200, 400))
		pygame.display.flip()

	def show_game_over(self):
		image = pygame.Surface([640, 480], pygame.SRCALPHA, 32)
		image = image.convert_alpha()
		font = pygame.font.SysFont('', 40)
		line1 = font.render(f"Game is over! Your score is {self.snake.length}.", True, (0, 0, 0))
		self.surface.blit(line1, (250, 300))
		line2 = font.render("Hit the ENTER KEY or SPACE BAR to replay.", True, (0, 0, 0))
		self.surface.blit(line2, (250, 350))
		pygame.display.flip()

		pygame.mixer.music.pause()

	def reset(self):
		self.snake = Snake(self.surface, 1)
		self.apple = Apple(self.surface)

	def display_score(self):
		font = pygame.font.SysFont('arial', 30)
		score = font.render(f"Score: {self.snake.length}", True, (255, 255, 255))
		self.surface.blit(score, (800,10))

	def display_level(self):
		font = pygame.font.SysFont('arial', 30)
		score = font.render(f"Level: {self.snake.level}", True, (255, 255, 255))
		self.surface.blit(score, (40,10))

	def run(self):
		running = True
		pause = False

		while running:
			for event in pygame.event.get():
				if event.type == KEYDOWN:
					if event.key == K_ESCAPE:	
						running = False

					if event.key == K_RETURN:
						pygame.mixer.music.rewind()
						pygame.mixer.music.unpause()

						pause = False

					if event.key == K_SPACE:
						if pause:
							pygame.mixer.music.unpause()
							pause = False

						else:
							pygame.mixer.music.pause()
							self.show_pause_screen()
							pause = True

					if not pause:
						if event.key == K_UP:
							self.snake.move_up()

						if event.key == K_DOWN:
							self.snake.move_down()

						if event.key == K_LEFT :
							self.snake.move_left()

						if event.key == K_RIGHT:
							self.snake.move_right()

				elif event.type == QUIT:
						running = False
			try:
				if not pause:
					self.play()
			except Exception as e:
				self.show_game_over()
				pause = True
				self.reset()

			time.sleep(self.snake.speed)


if __name__ == "__main__":
	game = Game()
	game.run()