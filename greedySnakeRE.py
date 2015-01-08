#!/usr/bin/env python
from Tkinter import *
from random import *
class snake(Frame):
	def __init__(self):
		Frame.__init__(self)
		self.snake = [(0, 0)]
		self.snakeRec = []
		self.fruit = [-1, -1]
		self.fruitRec = -1
		self.gridNumber = 10
		self.size = 450
		self.di = 3
		self.originalSpeed = 500
		self.grid()
		
		self.canvas = Canvas(self)
		self.canvas.grid()
		self.canvas.config(width = self.size, height = self.size)
		self.draw_grid()
		s = self.size / self.gridNumber
		rec = self.canvas.create_rectangle(self.snake[0][0] * s, self.snake[0][1] * s, \
		(self.snake[0][0] + 1) * s, (self.snake[0][1] + 1) * s, fill = "yellow")
		self.snakeRec.insert(0, rec)
		self.bind_all("<KeyRelease>", self.key_release)
		self.draw_fruit()
		self.after(self.originalSpeed, self.draw_snake)
		
	def draw_grid(self):
		s = self.size / self.gridNumber
		for i in range(0, self.gridNumber + 1):
			self.canvas.create_line(i * s, 0, i * s, self.size)
			self.canvas.create_line(0, i * s, self.size, i * s)
		
	def draw_fruit(self):
		s = self.size / self.gridNumber
		x = randrange(0, self.gridNumber)
		y = randrange(0, self.gridNumber)
		while (x, y) in self.snake:
			x = randrange(0, self.gridNumber)
			y = randrange(0, self.gridNumber)
		rec = self.canvas.create_rectangle(x * s, y * s, (x + 1) * s, (y + 1) * s, \
		fill = "yellow")
		self.fruit[0] = x
		self.fruit[1] = y
		self.fruitRec = rec
		
	def draw_snake(self):
		s = self.size / self.gridNumber
		head = self.snake[0]
		new = [head[0], head[1]]
		if self.di == 1:
			new[1] = (head[1] - 1) % self.gridNumber
		elif self.di == 2:
			new[0] = (head[0] + 1) % self.gridNumber
		elif self.di == 3:
			new[1] = (head[1] + 1) % self.gridNumber
		else:
			new[0] = (head[0] - 1) % self.gridNumber
		next = (new[0], new[1])
		if next in self.snake:
			exit()
		elif next == (self.fruit[0], self.fruit[1]):
			self.snake.insert(0, next)
			self.snakeRec.insert(0, self.fruitRec)
			self.draw_fruit()
		else:
			tail = self.snake.pop()
			rec = self.snakeRec.pop()
			self.canvas.move(rec, (next[0] - tail[0]) * s, (next[1] - tail[1]) * s)
			self.snake.insert(0, next)
			self.snakeRec.insert(0, rec)	
		self.after(self.originalSpeed, self.draw_snake)
		
	def key_release(self, event):
		if event.keysym == "Up" and self.di != 3:
			self.di = 1
		elif event.keysym == "Right" and self.di !=4:
			self.di = 2
		elif event.keysym == "Down" and self.di != 1:
			self.di = 3
		elif event.keysym == "Left" and self.di != 2:
			self.di = 4
			
app = snake()
app.master.title("Greedy Snake")
app.mainloop()