var1='background1.jpg'
var2='Snakehead2.png'
var3='gameover2.png'
var4='apple1.png'
var5='startscreen4.jpg'
var6='pausescr1.png'
var7='apple2.png'
var8='background1.wav'
var9='apple1.wav'
var10='gameover3.wav'
var11='abc.wav'
var12='button1.wav'
var13='control_scr-2.jpg'

import pygame,sys
import pygame.mixer
import time
import random
from locals import *
pygame.mixer.pre_init(44100, -16, 1, 512)  # to reduce the sound delay or lag
pygame.init()

screen_width=1000
screen_height=700
screen=pygame.display.set_mode((screen_width,screen_height),0,32)

backg=pygame.image.load(var1).convert()
snake_head=pygame.image.load(var2).convert_alpha()
game_over=pygame.image.load(var3).convert_alpha()
apple=pygame.image.load(var4).convert_alpha()
startscr=pygame.image.load(var5).convert()
pausescr=pygame.image.load(var6).convert_alpha()
goldenapple=pygame.image.load(var7).convert_alpha()
controlscr=pygame.image.load(var13).convert()

block_size=20
apple_size=30

backg_sound= pygame.mixer.Sound(var8)
apple_sound = pygame.mixer.Sound(var9)
gameover_sound= pygame.mixer.Sound(var10)
intro_sound = pygame.mixer.Sound(var11)
button_sound = pygame.mixer.Sound(var12)

pygame.display.set_caption("Snake Byte")
icon = pygame.image.load(var4).convert_alpha()
pygame.display.set_icon(icon)

white=[255,255,255]
black=[0,0,0]
red=[200,0,0]
light_red=[255,0,0]
green=[34,177,76]
light_green=[0,255,0]
snake_green=[0,155,0]
blue=[0,0,255]
yellow=[220,220,0]
light_yellow=[255,255,0]

smallfont=pygame.font.Font("Arial",32)
medfont=pygame.font.Font("Arial",50)
largefont=pygame.font.Font("Arial",80)

clock=pygame.time.Clock()
FPS=20

def pause():
	pause = True
	screen.blit(pausescr,(300,175))
	
	while pause:
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_c:
					pause = False
				if event.key == pygame.K_q:
					pygame.quit()
					quit()
		pygame.display.update()			
		clock.tick(10)			

def controls():
	controls = True
	while controls:	
		screen.blit(controlscr,(0,0))
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
		button("Start",800,50,120,75,green,light_green,"play")
		pygame.display.update()
		clock.tick(10)
		
def score(score):
	text = smallfont.render("Score : "+ str(score),True,black)
	screen.blit(text,(480,20))

def text_objects(text,color,size):
	if size == "small":	
		screen_surf = smallfont.render(text,True,color)
	if size == "medium":	
		screen_surf = medfont.render(text,True,color)
	if size == "large":	
		screen_surf = largefont.render(text,True,color)
	return screen_surf,screen_surf.get_rect()

def message(msg,color,y_disp=0,size="small"):
	screen_surface,text_rect = text_objects(msg,color,size)
	#screen_text=font.render(msg,True,color)
	#screen.blit(screen_text,(screen_width/3,screen_height/3))
	text_rect.center=(screen_width/2),(screen_height/2)+y_disp
	screen.blit(screen_surface,text_rect)

def button_text(msg,button_x,button_y,button_width,button_height,size="small"):	
	screen_surface,text_rect = text_objects(msg,black,size)
	text_rect.center = (button_x + button_width/2),(button_y + button_height/2) 
	screen.blit(screen_surface,text_rect)
		
def button(text,x,y,width,height,inactive_color,active_color,action = None):
	cursor = pygame.mouse.get_pos()
	if x+width > cursor[0] >x and y +height> cursor[1] > y:
		pygame.draw.rect(screen,active_color,(x,y,width,height))
		click = pygame.mouse.get_pressed()
		if click[0] == 1 and action != None:
			if action == "play":
				pygame.mixer.stop()
				button_sound.play()
				gameLoop()
			elif action == "quit":
				pygame.mixer.stop()
				button_sound.play()
				pygame.quit()
				quit()
			elif action == "controls":
				button_sound.play()
				controls()	
	else:
		pygame.draw.rect(screen,inactive_color,(x,y,width,height))

	button_text(text,x,y,width,height,"small")
			
def snakefunc(block_size,snake_list):

	if	direction == 'right':
		head = pygame.transform.rotate(snake_head,270)
	if direction == 'left':
		head = pygame.transform.rotate(snake_head,90)
	if direction == 'upwards':
		head=snake_head
	if direction == 'downwards':
		head = pygame.transform.rotate(snake_head,180)
		
	screen.blit(head,(snake_list[-1][0],snake_list[-1][1])) # copies the snakeHead to the last element in the snakeList every time
	for point in snake_list[:-1]:
		pygame.draw.rect(screen,snake_green,[point[0],point[1],block_size,block_size])	

def startScreen():
	intro = True
	while intro:
		screen.blit(startscr,(0,0))		
		
		for event in pygame.event.get():
			if event.type == QUIT:
				pygame.quit()
				quit()
		
		button("Play",40,95,120,75,green,light_green,"play")
		button("Controls",180,95,160,75,yellow,light_yellow,"controls")
		button("Quit",360,95,120,75,red,light_red,"quit")
		
		pygame.display.update()
		clock.tick(10)
def gameLoop():
	
	global direction 
	direction = "right"
	x=screen_width/2
	y=screen_height/2	
	x_change=10
	y_change=0
	apple_x=random.randrange(block_size,screen_width-block_size)#,block_size) # the 3rd parameter is the factor with witch rand no. is incremented
	apple_y=random.randrange(block_size,screen_height-block_size)#,block_size)	# hence the apple will always come in line of the snake 
	backg_sound.play()
	i = 0
	
	snake_list=[]
	snake_length=1  #this ensures that the number of points(blocks) in the snake is limited and not ever increasing(unlimited)
	
	gameExit = False
	gameOver = False
				
	while not gameExit :
		
		while gameOver == True:    # this loop will only be true once the snake touches the boundary i.e the the end and further action can be taken
			screen.blit(game_over,(300,150))
			button("play again",100,550,180,75,green,light_green,"play")
			button("Quit Game",720,550,180,75,red,light_red,"quit")
			backg_sound.stop()
			if i<1:
				gameover_sound.play()
				i+=1
			pygame.display.update()
			
			for event in pygame.event.get():
				if event.type==	QUIT:                            	# if we press the exit(red cross on top right) on the screen
					gameExit = True
					gameOver = False
					
				if event.type == pygame.KEYDOWN:
					if event.key==pygame.K_q:
						gameExit=True
						gameOver=False
					if event.key == pygame.K_c:
						pygame.mixer.stop()						
						gameLoop()
		
		for event in pygame.event.get():
			if event.type==	QUIT:
				gameExit = True
			
			if event.type==pygame.KEYDOWN:
				if event.key==pygame.K_LEFT:
					direction = 'left'
					x_change=-block_size
					y_change=0
				elif event.key==pygame.K_RIGHT:
					direction = 'right'
					x_change=block_size
					y_change=0
				elif event.key==pygame.K_UP:
					direction = 'upwards'
					y_change=-block_size
					x_change=0
				elif event.key==pygame.K_DOWN:
					direction = 'downwards'
					y_change=block_size
					x_change=0	
				elif event.key == pygame.K_p:
					pause()
		screen.blit(backg,(0,0))
							
		if x<0 or x>=screen_width or y<0 or y>=screen_height:
			gameOver = True
		
		x+=x_change
		y+=y_change
	
		snake_head = []	# snake head will be a kind of temp. list to hold the coordinates of the head of the snake
		snake_head.append(x)
		snake_head.append(y)
		snake_list.append(snake_head)
		
		# COLLISION DETECTION LOGIC :
		if x > apple_x and x < apple_x+apple_size or x+block_size > apple_x and x+block_size < apple_x+apple_size:
			if y > apple_y and y< apple_y+apple_size:
				apple_x=random.randrange(block_size,screen_width-block_size,block_size)	
				apple_y=random.randrange(block_size,screen_height-block_size,block_size)
				snake_length+=1
				apple_sound.play()
			elif y+block_size > apple_y and y+block_size< apple_y+apple_size:
				apple_x=random.randrange(block_size,screen_width-block_size,block_size)
				apple_y=random.randrange(block_size,screen_height-block_size,block_size)
				snake_length+=1
				apple_sound.play()
				
		#pygame.draw.rect(screen,red,[apple_x,apple_y,apple_size,apple_size])
		
		if (snake_length-1) % 7 !=0 :	
			screen.blit(apple,(apple_x,apple_y))	
		else:
			screen.blit(goldenapple,(apple_x,apple_y))
			
		if len(snake_list) > snake_length: #this ensures that the length of the snake is in control 
			del snake_list[0]                       # this deletes the earliest point which is no longer needed and shifts the new points leftwards
		
		for  eachSegment in snake_list[ : -1]:
			if eachSegment == snake_head:
				gameOver = True
		
		snakefunc(block_size,snake_list)  #we want the snake to overlap the apple hence first draw apple then the snake
		
		score(snake_length-1)
		
		pygame.display.update()
						
		clock.tick(FPS)				
	
	pygame.quit()
	quit()	
	
intro_sound.play()
startScreen()	
gameLoop()		



