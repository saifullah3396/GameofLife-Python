#!/usr/bin/python3

import curses
import time
import numpy as np
from os import listdir

class GameOfLife:
	def __init__(self, config):
		self.height = config['grid_size']['height']
		self.width = config['grid_size']['width']
		self.refresh_rate = config['refresh_rate']
		if not config['is_test']:
			patterns = [p.split('.')[0] for p in listdir(config['pattern_dir'])]
			print("Please choose a pattern to start:")
			for i, j in enumerate(patterns): 
				print(str(i+1) + ". " + j)
			s = input('--> ')
			if not s:
				print("No starting pattern chosen. Exiting game.")
				exit()
			for i, j in enumerate(patterns):
				if(s == str(i+1)):
					self.pattern = self.readPattern(config['pattern_dir'] + j + ".txt")
		else:
			self.pattern = self.readPattern(config['pattern_dir'] + config['test_pattern'] + ".txt")
		print(self.pattern)
		stdscr = curses.initscr()
		stdscr.nodelay(1)
		curses.wrapper(self.start)
	
	def alive_neighbours(self, y, x):
		count = 0
		for n in [self.pattern[j][i] for j in [y-1,y,y+1] for i in [x-1,x,x+1] if j in range(0,len(self.pattern)) and i in range(0,len(self.pattern[y])) and (x,y) != (i,j)]:
			if n == 1:
				count = count + 1
		return count

	def update_screen(self, screen):
		for (y,x), val in np.ndenumerate(self.pattern):
			if val == 1:
				screen.addstr(y, x, "x")
			else:
				screen.addstr(y, x, ".")

	def update_game(self):
		temp = np.zeros((self.height, self.width))
		np.copyto(temp, self.pattern)
		for (y,x), val in np.ndenumerate(self.pattern):
			neighbours = self.alive_neighbours(y, x)
			if val == 0:
				if neighbours == 3:
					temp[y][x] = 1
			else:
				if (neighbours < 2) or (neighbours > 3):
					temp[y][x] = 0
		self.pattern = temp

	def readPattern(self, file):
		f = open(file, "r")
		pattern = np.zeros((self.height, self.width))
		y = 0
		x = 0
		for row in f.readlines():
			x = 0
			for col in range(0, len(row)):
				if row[col] == "x":
					pattern[y, x] = 1
				x = x + 1
			y = y + 1 
		f.close()
		return pattern

	def start(self, screen):
		while(1):
			self.update_screen(screen)
			self.update_game()
			screen.refresh()
			time.sleep(self.refresh_rate)
			ch = screen.getch()
			if ch != -1:
				break
