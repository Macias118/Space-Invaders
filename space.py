import pygame
import random
from pygame import gfxdraw
pygame.init()
acceleration = 8

black = (0,0,0)
white = (255,255,255)
gray = (100,100,100)

green = (0,255,0)
red = (255,0,0)
blue = (0,0,255)
clock = pygame.time.Clock()  

window_width = 1366			#window_weight
window_height = 768
window = pygame.display.set_mode((window_width, window_height), pygame.DOUBLEBUF | pygame.FULLSCREEN )

class Bullet():

	def __init__(self, x, y, r):
		self.x = x
		self.y = y
		self.radius = r
		
	def draw(self):
		#pygame.draw.circle(window, red, (self.x, self.y), self.radius)
		pygame.draw.line(window, red, (self.x, self.y), (self.x, self.y-30), self.radius)
	
	
class Enemy():
	
	def __init__(self, x, y, w, h):
		self.x = x
		self.y = y
		self.width = w
		self.height = h
		self.pixel = 8
		
	def draw(self):	
		self.points = (
			(self.x-self.pixel, self.y+self.pixel),				# I
			(self.x, self.y+self.pixel),							# J
			(self.x, self.y),											# A
			(self.x+self.pixel, self.y),							# B
			(self.x+self.pixel, self.y+self.pixel),				# C
			(self.x+3*self.pixel, self.y+self.pixel),			# D
			(self.x+3*self.pixel, self.y),						# E	
			(self.x+4*self.pixel, self.y),						# F
			(self.x+4*self.pixel, self.y+self.pixel),			# X
			(self.x+5*self.pixel, self.y+self.pixel),			# G
			(self.x+2*self.pixel, self.y+5*self.pixel),		# H
			
			)
		
		
		pygame.draw.polygon(window, white, self.points)	
	
	def changeX(self, value):
		self.x += value
	
def message(content, size, x, y):

	text = pygame.font.Font('freesansbold.ttf', size)
	textSurface = text.render(content, True, white)
	textRect = textSurface.get_rect()
	textRect.center = (x,y)
	window.blit(textSurface, textRect)
	
def intro():

	intro = True
	pygame.display.set_caption('Space Invaders')
	
	while intro:
		for event in pygame.event.get():
			
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				if event.key == pygame.K_s:
					intro = False
					
		window.fill(black)
		message('Press S to START', 70, window_width/2, window_height/2)
		pygame.display.update()

		
def ship(shipImg, x, y):
	window.blit(shipImg, (x, y))
	
def moveEnemies(enemyArray, dir, down, s_y):
	
	dv = dir * 15
	for e in enemyArray:
		e.x += dv
		e.y += down
		if e.y + e.height >= s_y:
			lose()
			
def lose():
	
	lose = True
	while lose:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_r:
					lose = False
					main()
				
		window.fill(black)
		message('You Lose. Press R to restart', 60, window_width/2, window_height/2)
		pygame.display.update()
		
def main():
	
	space_width = 50
	space_x = window_width / 2
	space_y = window_height - 80
	dx = 0
	shot = False
	TimeToNextShoot = 80
	
	NumberOfStars = 3500
	NumberOfBullets = 0
	NumberOfEnemies = 60
	
	Counter = 1000
	EnemyCounter = 10
	EnemyDir = 1
	LeftOrRight = 6
	OutroCounter = 0
	outro = 1
	down = 0
	
	pointz = 0
	
	space = pygame.image.load('space.png')
	
	# bullets
	bulletsArray = []
	
	# stars
	stars = []
	for s in range(NumberOfStars):
		i = random.randrange(0, window_width)
		j = random.randrange(0, window_height)
		stars.append(i)
		stars.append(j)
		
	#enemies
	enemies = []
	x = 200
	y = 200
	enemy_width = 50
	enemy_height = 36
	for e in range(NumberOfEnemies):
		en = Enemy(x, y, enemy_width, enemy_height)
		enemies.append(en)
		x += enemy_width * 2
		if x > window_width - 200:
			x = 200
			y += enemy_height*2
	

	while True:
		for event in pygame.event.get():
		
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_ESCAPE:
					pygame.quit()
					quit()
				if event.key == pygame.K_LEFT:
					dx = -4
				if event.key == pygame.K_RIGHT:
					dx = 4
				if event.key == pygame.K_q:
					licznik = len(enemies)
					for e in range(licznik):
						enemies.pop()
						NumberOfEnemies -= 1
						pointz = 9999999999
				if event.key == pygame.K_a:
					main()
						
			if event.type == pygame.KEYUP:
				if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
					dx = 0
					
		if pygame.key.get_pressed()[ pygame.K_SPACE ]:	
			if Counter >= TimeToNextShoot:
				bul = Bullet(space_x+25, space_y, 6)
				bulletsArray.append(bul)
				NumberOfBullets += 1
				Counter = 0
			
			
		# BACKGROUND	
		window.fill(black)
		for i in range(0, NumberOfStars ,2):
			gfxdraw.pixel(window, stars[i], stars[i+1], white)
		message("Points: "+str(pointz), 20, 50, 20)
		
		# SPACE
		space_x += dx
		if space_x + dx < space_width:
			space_x = space_width
		if space_x + dx > window_width - 2*space_width:
			space_x = window_width - 2*space_width
		ship(space, space_x, space_y)
		
		
		# BULLETS
		if Counter < TimeToNextShoot:
			Counter += 1
		
		for bullet in bulletsArray:
			bullet.y -= 3
			if bullet.y < 0:
				bulletsArray.remove(bullet)
				NumberOfBullets -= 1
			else:
				bullet.draw()
				for en in enemies:
					if bullet.x + bullet.radius >= en.x and bullet.x - bullet.radius <= en.x + en.width:
						if bullet.y < en.y + en.height and bullet.y + bullet.radius > en.y:
							try:
								bulletsArray.remove(bullet)
								enemies.remove(en)
								NumberOfEnemies -= 1
								NumberOfBullets -= 1
								pointz += 100
							except:	
								pass
							
					
		
		# ENEMIES
		EnemyCounter -= 1
		Down = 0
			
		if EnemyCounter < 0:
			if LeftOrRight < 0:
				Down = 10
				EnemyDir *= -1
				LeftOrRight = 6
			else:
				LeftOrRight -= 1
				EnemyCounter = 80
			moveEnemies(enemies, EnemyDir, Down, space_y)
			
			
		for en in enemies:
		 	en.draw()
		
		if len(enemies) <= 0:
			if OutroCounter > 20 or OutroCounter < 0:
				outro *= -1
			
			if outro == 1:
				message("You Win", 300, window_width/2, window_height/2)
				OutroCounter += 1
			else:
				OutroCounter -= 1
				
				
		pygame.display.update()
		clock.tick( 60 )	
		
		
		
		
intro()	
main()
