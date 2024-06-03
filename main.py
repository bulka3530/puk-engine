import sys

import pygame
from pygame.locals import *

from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw() #to hide the main window


pygame.init()

# делаем переменные которые нужно

fps = 60
fpsClock = pygame.time.Clock()

width, height = 512, 512
screen = pygame.display.set_mode((width, height))

# читаем файл с картой

with open("data/map.txt", "r") as map_file:
	game_map = map_file.readlines()
game_map = [line.strip() for line in game_map]

# читаем файл с параметрами игры
#info = open("game.txt", "r")

pygame.display.set_caption("Game")

pygame.mouse.set_visible(False)

# загружаем смешные картинки

spriteW = pygame.image.load("data/win.png").convert_alpha()
spriteL = pygame.image.load("data/loose.png").convert_alpha()
spriteWall = pygame.image.load("data/wall.png").convert_alpha()
spritePlayer = pygame.image.load("data/player.png").convert_alpha()
spriteBg = pygame.image.load("data/bg.png").convert_alpha()
spriteButton1 = pygame.image.load("data/button.png").convert_alpha()
spriteButton2 = pygame.image.load("data/button2.png").convert_alpha()
spriteDoor = pygame.image.load("data/door.png").convert_alpha()
spriteEraser = pygame.image.load("data/eraser.png").convert_alpha()


myFont = pygame.font.Font("data/font.ttf", 12)

# игрок

pressed = False

player_rect = pygame.Rect(0, 0, 32, 32)
player_spawned = False
#move_y = 0

def move(thing, dx, dy):
	if dx != 0:
		thing.x += dx
	if dy != 0:
		thing.y += dy

def check_collision(thing, game_map, tile_size):
	for y, line in enumerate(game_map):
		for x, char in enumerate(line):
			if char == "#":
				tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
				if thing.colliderect(tile_rect):
					return True
			if char == "W":
				tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
				if thing.colliderect(tile_rect):
					messagebox.showinfo(":)", "You won!")
					sys.exit()
			if char == "L":
				tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
				if thing.colliderect(tile_rect):
					messagebox.showinfo(":(", "You loose!")
					sys.exit()
			if char == "B":
				tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
				if thing.colliderect(tile_rect):
					pressed = True
			if char == "D":
				tile_rect = pygame.Rect(x * tile_size, y * tile_size, tile_size, tile_size)
				if thing.colliderect(tile_rect):
					if pressed == False:
						return True

	return False

	



# игровой цикл

while True:
	screen.fill((0, 0, 0))

	for y in range(0,width,32):
		for x in range(0,height,32):
			screen.blit( spriteBg,(x,y))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

	keys = pygame.key.get_pressed()
	if keys[pygame.K_UP]:
		move(player_rect,0,-2)
		if check_collision(player_rect, game_map, 32):
			move(player_rect, 0, 2)
	if keys[pygame.K_DOWN]:
		move(player_rect,0,2)
		if check_collision(player_rect, game_map, 32):
			move(player_rect,0,-2)
	if keys[pygame.K_LEFT]:
		move(player_rect,-2,0)
		if check_collision(player_rect, game_map, 32):
			move(player_rect,2,0)
	if keys[pygame.K_RIGHT]:
		move(player_rect,2,0)
		if check_collision(player_rect, game_map, 32):
			move(player_rect,-2,0)

	for y, line in enumerate(game_map):
		for x, char in enumerate(line):
			if char == "#":
				#pygame.draw.rect(screen, "white", pygame.Rect(x * 32, y * 32, 32, 32))
				screen.blit(spriteWall, (x * 32, y * 32))
			if char == "W":
				#pygame.draw.rect(screen, "white", pygame.Rect(x * 32, y * 32, 32, 32))
				screen.blit(spriteW, (x * 32, y * 32))
			if char == "L":
				#pygame.draw.rect(screen, "white", pygame.Rect(x * 32, y * 32, 32, 32))
				screen.blit(spriteL, (x * 32, y * 32))
			if char == "P" and not player_spawned:
				player_rect.x = x * 32
				player_rect.y = y * 32
				player_spawned = True
			if char == "B":
				#pygame.draw.rect(screen, "white", pygame.Rect(x * 32, y * 32, 32, 32))
				if pressed:
					screen.blit(spriteButton2, (x * 32, y * 32))
				else:
					screen.blit(spriteButton1, (x * 32, y * 32))
			if char == "D":
				#pygame.draw.rect(screen, "white", pygame.Rect(x * 32, y * 32, 32, 32))
				screen.blit(spriteDoor, (x * 32, y * 32))

	#pygame.draw.rect(screen, "red", pygame.Rect(player_rect.x, player_rect.y, 32, 32))
	screen.blit(spritePlayer, (player_rect.x, player_rect.y))

	pygame.display.flip()
	fpsClock.tick(fps)
