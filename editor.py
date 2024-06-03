import sys
import os

import pygame
from pygame.locals import *

from tkinter import *
from tkinter import messagebox

Tk().wm_withdraw() #to hide the main window


pygame.init()

# делаем переменные которые нужно

fps = 60
fpsClock = pygame.time.Clock()

width, height = 512 + 96, 512
screen = pygame.display.set_mode((width, height))

# читаем файл с картой

with open("data/map.txt", "r") as map_file:
	game_map = map_file.readlines()
game_map = [line.strip() for line in game_map]

# читаем файл с параметрами игры
#info = open("game.txt", "r")

pygame.display.set_caption("Map editor")

pygame.mouse.set_visible(True)



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

currentItem = 1


def mod_char(filename, line_number, column_number, new_character, encoding='utf-8'):

    if column_number <= 0:
        raise ValueError("Invalid column number: must be positive")

    with open(filename, 'r+', encoding=encoding) as f:
        # Read the entire content into memory
        content = f.readlines()

        if line_number <= 0 or line_number > len(content):
            raise ValueError(f"Invalid line number: {line_number}")

        # Get the line to modify
        line = content[line_number - 1]

        # Check if column number is within the line length (excluding newline)
        if column_number > len(line):
            raise ValueError(f"Invalid column number: line length is {len(line)}")

        # Modify the character at the specified column (zero-based indexing)
        content[line_number - 1] = line[:column_number - 1] + new_character + line[column_number:]

        # Move the file pointer to the beginning (not strictly necessary here, but can be for clarity)
        f.seek(0)

        # Write the modified content back to the file
        f.writelines(content)


# игровой цикл

while True:
	screen.fill((127, 127, 127))

	for y in range(0,width,32):
		for x in range(0,height,32):
			screen.blit( spriteBg,(x,y))

	for event in pygame.event.get():
		if event.type == QUIT:
			pygame.quit()
			sys.exit()

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
			if char == "P":
				screen.blit(spritePlayer, (x * 32, y * 32))
			if char == "K":
				screen.blit(spritePlayer, (x * 32, y * 32))

	mouseX, mouseY = pygame.mouse.get_pos()
	if not mouseX > 512:
		ix = mouseX // 32
		iy = mouseY // 32
		pukX, pukY = ix * 32, iy * 32
		pygame.draw.rect(screen, Color(255,255,255,5), pygame.Rect(pukX, pukY, 32, 32))
		pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR))
	else:
		pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))

	

	screen.blit(spriteW, (544, 32))
	screen.blit(spriteL, (544, 96))
	screen.blit(spriteWall, (544, 160))
	screen.blit(spritePlayer, (544, 224))
	screen.blit(spriteEraser, (544, 288))

	if pygame.mouse.get_pressed()[0]:
		if 544 <= mouseX <= 544+140 and 32 <= mouseY <= 32+32:
			print("win")
			currentItem = 1
		if 544 <= mouseX <= 544+140 and 96 <= mouseY <= 96+32:
			print("loose")
			currentItem = 2
		if 544 <= mouseX <= 544+140 and 160 <= mouseY <= 160+32:
			print("wall")
			currentItem = 3
		if 544 <= mouseX <= 544+140 and 224 <= mouseY <= 224+32:
			print("player")
			currentItem = 4
		if 544 <= mouseX <= 544+140 and 288 <= mouseY <= 288+32:
			print("none")
			currentItem = 5

	keys = pygame.key.get_pressed()
	if keys[pygame.K_1]:
		print("win")
		currentItem = 1
	if keys[pygame.K_2]:
		print("loose")
		currentItem = 2
	if keys[pygame.K_3]:
		print("wall")
		currentItem = 3
	if keys[pygame.K_4]:
		print("player")
		currentItem = 4
	if keys[pygame.K_5]:
		print("none")
		currentItem = 5

	screen.blit(myFont.render("Puk engine v2", 1, (255,255,255)), (10, 10))
	screen.blit(myFont.render("Numbers-change", 1, (255,255,255)), (512, 384))
	screen.blit(myFont.render("item", 1, (255,255,255)), (512, 410))
	screen.blit(myFont.render("RMB - eraser", 1, (255,255,255)), (512, 436))


	if pygame.mouse.get_cursor() == pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_CROSSHAIR):
		if currentItem == 1 and not pygame.mouse.get_pressed()[2]:
			screen.blit(spriteW, (pygame.mouse.get_pos()))
			if pygame.mouse.get_pressed()[0]:
				mouseX, mouseY = pygame.mouse.get_pos()
				pukX = mouseX // 32
				pukY = mouseY // 32
				print(pukX)
				print(pukY)
				mod_char("data/map.txt", pukY+1, pukX+1, 'W', encoding='utf-8')
				with open("data/map.txt", "r") as map_file:
					game_map = map_file.readlines()
				game_map = [line.strip() for line in game_map]

		if currentItem == 2 and not pygame.mouse.get_pressed()[2]:
			screen.blit(spriteL, (pygame.mouse.get_pos()))
			if pygame.mouse.get_pressed()[0]:
				mouseX, mouseY = pygame.mouse.get_pos()
				pukX = mouseX // 32
				pukY = mouseY // 32
				print(pukX)
				print(pukY)
				mod_char("data/map.txt", pukY+1, pukX+1, 'L', encoding='utf-8')
				with open("data/map.txt", "r") as map_file:
					game_map = map_file.readlines()
				game_map = [line.strip() for line in game_map]
		if currentItem == 3 and not pygame.mouse.get_pressed()[2]:
			screen.blit(spriteWall, (pygame.mouse.get_pos()))
			if pygame.mouse.get_pressed()[0]:
				mouseX, mouseY = pygame.mouse.get_pos()
				pukX = mouseX // 32
				pukY = mouseY // 32
				print(pukX)
				print(pukY)
				mod_char("data/map.txt", pukY+1, pukX+1, '#', encoding='utf-8')
				with open("data/map.txt", "r") as map_file:
					game_map = map_file.readlines()
				game_map = [line.strip() for line in game_map]
		if currentItem == 4 and not pygame.mouse.get_pressed()[2]:
			screen.blit(spritePlayer, (pygame.mouse.get_pos()))
			if pygame.mouse.get_pressed()[0]:
				mouseX, mouseY = pygame.mouse.get_pos()
				pukX = mouseX // 32
				pukY = mouseY // 32
				print(pukX)
				print(pukY)
				mod_char("data/map.txt", pukY+1, pukX+1, 'P', encoding='utf-8')
				with open("data/map.txt", "r") as map_file:
					game_map = map_file.readlines()
				game_map = [line.strip() for line in game_map]
		if currentItem == 5:
			screen.blit(spriteEraser, (pygame.mouse.get_pos()))
			if pygame.mouse.get_pressed()[0]:
				mouseX, mouseY = pygame.mouse.get_pos()
				pukX = mouseX // 32
				pukY = mouseY // 32
				print(pukX)
				print(pukY)
				mod_char("data/map.txt", pukY+1, pukX+1, '.', encoding='utf-8')
				with open("data/map.txt", "r") as map_file:
					game_map = map_file.readlines()
				game_map = [line.strip() for line in game_map]
		if pygame.mouse.get_pressed()[2]:
			screen.blit(spriteEraser, (pygame.mouse.get_pos()))
			mouseX, mouseY = pygame.mouse.get_pos()
			pukX = mouseX // 32
			pukY = mouseY // 32
			print(pukX)
			print(pukY)
			mod_char("data/map.txt", pukY+1, pukX+1, '.', encoding='utf-8')
			with open("data/map.txt", "r") as map_file:
				game_map = map_file.readlines()
			game_map = [line.strip() for line in game_map]

	pygame.display.flip()
	fpsClock.tick(fps)
