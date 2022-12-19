import pygame, math, random
import time as time_module
from pygame_functions import clock as timer

wScreen = 1150
hScreen = 500

pygame.init()

clock = pygame.time.Clock()
clock2 = pygame.time.Clock()
win = pygame.display.set_mode((wScreen, hScreen))
pygame.display.set_caption("Cannon Game")

font = pygame.font.SysFont("Adobe Song Std L", 35)
font2 = pygame.font.SysFont("Adobe Song Std L", 25)
font3 = pygame.font.SysFont("Adobe Song Std L", 20)
font4 = pygame.font.SysFont("Rubber Biscuit", 50)
ground = pygame.image.load("img/ground.png")
cannon_base = pygame.image.load("img/cannon2.png")
cannon = pygame.image.load("img/cannon.png")
ball = pygame.image.load("img/ball.png").convert()
r = cannon.get_rect()

dot = []
data = []

index = 0

enemy_index = 0
enemy_index2 = 0
enemy = [pygame.image.load("img/enemy/0.png"),
         pygame.image.load("img/enemy/1.png"),
         pygame.image.load("img/enemy/2.png"),
         pygame.image.load("img/enemy/3.png")]
walk = [pygame.image.load("img/enemy/walk0.png"),
		pygame.image.load("img/enemy/walk1.png"),
		pygame.image.load("img/enemy/walk2.png"),
		pygame.image.load("img/enemy/walk3.png")]
enemy_pos = [0]
enemy_die = [pygame.image.load("img/enemy/die0.png"),
			pygame.image.load("img/enemy/die1.png"),
			pygame.image.load("img/enemy/die2.png"),
			pygame.image.load("img/enemy/die3.png"),
			pygame.image.load("img/enemy/die4.png"),
			pygame.image.load("img/enemy/die5.png")]
enemy_die_status = False
explosion_index = 0
explosion_pos = [0,0]
explosion = [pygame.image.load("img/explosion/0.png"),
         	 pygame.image.load("img/explosion/1.png"),
        	 pygame.image.load("img/explosion/2.png"),
       		 pygame.image.load("img/explosion/3.png"),
       		 pygame.image.load("img/explosion/4.png"),
         	 pygame.image.load("img/explosion/5.png"),
        	 pygame.image.load("img/explosion/6.png"),
       		 pygame.image.load("img/explosion/7.png"),
       		 pygame.image.load("img/explosion/8.png"),
         	 pygame.image.load("img/explosion/9.png"),
        	 pygame.image.load("img/explosion/10.png"),
       		 pygame.image.load("img/explosion/11.png")]

point_index = 0

backround = pygame.image.load("img/bg.jpg")

class ball(object):
	def __init__(self, x, y, radius, color):
		self.x = x
		self.y = y
		self.radius = radius
		self.color = color

	def drawBall(self, win):
		pygame.draw.circle(win, (0, 0 ,0), (self.x, self.y), self.radius)
		pygame.draw.circle(win, self.color, (self.x, self.y), self.radius-1)
	
	@staticmethod
	def ballPath(startX, startY, power, angle, time):
		velX = round(round(math.cos(angle) * power))
		velY = math.sin(angle) * power

		distX = round(velX * time)
		distY = (velY * time) + ((-4.9 * (time ** 2))/2)

		newX = round(startX + distX)
		newY = round(startY - distY)

		return (newX, newY, velX, distX)

def cannon_rotate(win, x, y, image, angle):
	cannon_rotated = pygame.transform.rotate(cannon, math.degrees(angle))
	rect = cannon_rotated.get_rect()
	win.blit(cannon_rotated, (x-rect.center[0], y-rect.center[1]))

def rule_line():
	#rule line X
	pygame.draw.line(win, (0, 0, 0), (85,5), (985,5))
	count = 0
	for i in range(0, 91):
		if (i%10) != 0:
			i *= 10
			pygame.draw.line(win, (0, 0, 0), (85+i,5), (85+i,10))
			
		else:
			num = font.render("%d" %((i//10)*100), True, (255,255,255))
			num_rot = pygame.transform.rotate(num, 270)
			i *= 10
			pygame.draw.line(win, (0, 0, 0), (85+i,5), (85+i,15))
			win.blit(num_rot, (75+i, 20))

def redrawWindow(line,pos,press):
	global run, show_butt_status,box_status,point_index,show1_butt_box_status,show2_butt_box_status

	win.blit(backround, (0,0)) #backround

	if shoot == False:
		if not((1015 < pos[0] < 1015+130) and (90 < pos[1] < 140+50)):
			pygame.draw.line(win, (0, 0, 0), line[0], line[1])

	golfBall.drawBall(win) #draw a ball


	cannon_rotate(win, 85, 413, cannon, angle)
	win.blit(cannon_base, (42, 400)) #cannon base
	win.blit(ground, (0, 500-37)) #ground
	win.blit(ground, (1080, 500-33))

	rule_line()

	#text	
	angle_text = font.render("Angle : " + str(int(math.degrees(angle))), True, (255,255,255))
	power_text = font.render("Power : " + str(int(power)), True, (255,255,255))

	win.blit(angle_text, (1010, 10))
	win.blit(power_text, (1010, 50))	

	show_butt_col = (255,255,255)
	clear_butt_col = (255,255,255)
	menu_butt_col = (255,255,255)
	show1_butt_box_col = (128,128,128)
	show1_text_box_col = (255,255,255)
	show2_butt_box_col = (128,128,128)
	show2_text_box_col = (255,255,255)
	#show button
	if (1015 < pos[0] < 1015+60) and (90 < pos[1] < 90+40):
		show_butt_col = (128,128,128)
		if press[0] == 1 and len(dot) != 0:
			if show_butt_status == False:
				show_butt_status = True
			else:
				show_butt_status = False
				box_status = False
				show1_butt_box_status = False
				show2_butt_box_status = False
	#clear button
	elif  (1085 < pos[0] < 1085+60) and (90 < pos[1] < 90+40):
		clear_butt_col = (128,128,128)
		if press[0] == 1:
			box_status = False
			show1_butt_box_status = False
			show2_butt_box_status = False
			for i in dot:
				dot.remove(i)
	#menu button
	elif (1015 < pos[0] < 1015+130) and (140 < pos[1] < 140+50):
		menu_butt_col = (128,128,128)
		if press[0] == 1:
			run = False
			box_status = False
			show1_butt_box_status = False
			show2_butt_box_status = False
			while dot != []:
				for i in dot:
					dot.remove(i)
	
	count = 0
	if show_butt_status == True:
		for i in dot:
			if (i[0]-5) < pos[0] < (i[0]+5) and (i[1]-5) < pos[1] < (i[1]+5):
				if press[0] == 1:
					box_status = True
					point_index = count
			count += 1
	if box_status:
		pygame.draw.rect(win, (255,255,255), pygame.Rect(1015,195,130,170))
		#power_box_text
		power_box_text = font3.render("Power:" + str(data[point_index][0]), True, (128,128,128))
		win.blit(power_box_text, (1022.5, 200))
		#angle_box_text
		angle_box_text = font3.render("Angle:" + str(int(data[point_index][1])), True, (128,128,128))
		win.blit(angle_box_text, (1087.5, 200))
		#time_box_text
		time_box_text = font3.render("Time:" + str(data[point_index][2]), True, (128,128,128))
		win.blit(time_box_text, (1022.5, 220))
		#Vx_box_text
		Vx_box_text = font3.render("VelocityX:ucosθ", True, (128,128,128))
		win.blit(Vx_box_text, (1022.5, 240))
		#show1_butt_text_box		
		if (1050 < pos[0] < (1050+80)) and (255 < pos[1] < (255+40)):
			show1_butt_box_col = (255,255,255)
			show1_text_box_col = (128,128,128)
			if press[0] == 1:
				show1_butt_box_status = True
		if show1_butt_box_status == False:
			pygame.draw.rect(win, show1_butt_box_col, pygame.Rect(1050,255,80,40))
			show1_text_box = font3.render("Show", True, show1_text_box_col)
			win.blit(show1_text_box, (1075, 267.5))			
		else:			
			Vx_text1_box = font3.render("=%dcos(%d)" %(data[point_index][0], int(data[point_index][1])), True, (128,128,128))
			win.blit(Vx_text1_box, (1055, 260))
			Vx_text2_box = font3.render("=%d" %(data[point_index][3]), True, (128,128,128))
			win.blit(Vx_text2_box, (1055, 280))
		#distance_bix_text
		distance_box_text = font3.render("Distance:Vxt", True, (128,128,128))
		win.blit(distance_box_text, (1022.5, 297.5))
		#show2_butt_text_box
		if (1050 < pos[0] < (1050+80)) and (312.5 < pos[1] < (312.5+40)):
			show2_butt_box_col = (255,255,255)
			show2_text_box_col = (128,128,128)
			if press[0] == 1:
				show2_butt_box_status = True
		if show2_butt_box_status == False:
			pygame.draw.rect(win, show2_butt_box_col, pygame.Rect(1050,312.5,80,40))
			show2_text_box = font3.render("Show", True, show2_text_box_col)
			win.blit(show2_text_box, (1075, 325))			
		else:
			distance_text1_box = font3.render(("=%d*%.1f" %(data[point_index][3], data[point_index][2])), True, (128,128,128))
			win.blit(distance_text1_box, (1055, 317.5))
			distance_text2_box = font3.render("=%d" %(data[point_index][4]), True, (128,128,128))
			win.blit(distance_text2_box, (1055, 337.5))

	show_butt_text = font2.render("Show", True, show_butt_col)
	clear_butt_text = font2.render("Clear", True, clear_butt_col)
	menu_butt_text = font.render("Menu", True, menu_butt_col)
	#show button
	pygame.draw.rect(win, show_butt_col, pygame.Rect(1015,90,60,40), 3)
	win.blit(show_butt_text, (1022.5, 102.5))
	#clear button
	pygame.draw.rect(win, clear_butt_col, pygame.Rect(1085,90,60,40), 3)
	win.blit(clear_butt_text, (1092.5, 102.5))
	#menu button
	pygame.draw.rect(win, menu_butt_col, pygame.Rect(1015,140,130,50), 3)
	win.blit(menu_butt_text, (1050, 152.5))

	if show_butt_status:
		for i in dot:
			pygame.draw.circle(win, (255,255,255), i, 5)
			pygame.draw.line(win, (255,255,255), i, (i[0], 5))

def findAngle(pos):
	sX = golfBall.x
	sY = golfBall.y
	try:
		angle = math.atan((sY - pos[1]) / (sX - pos[0])) #((sY - pos[1]) / (sX - pos[0])) หา tan จาก opposite/adjacent ส่วน math.atan((sY - pos[1]) / (sX - pos[0])) invers trigometry function 
	except:
		angle = math.pi / 2 #0.5pi

	if pos[1] < sY and pos[0] > sX:
		angle = abs(angle) #quardrant 1
	elif pos[1] < sY and pos[0] < sX:
		angle = math.pi - angle #quardrant 2
	elif pos[1] > sY and pos[0] < sX:
		angle = math.pi + abs(angle) #quardrant 3
	elif pos[1] > sY and pos[0] > sX:
		angle = (math.pi * 2) - angle #quardrant 4

	return round(angle, 2) #return radian angle

golfBall = ball(85, 415, 13, (255,255,255))

x,y,power,angle,time = 0,0,0,0,0
run = True
shoot = False
q2, q4 = False, False
explosion_status = False
game_loop_status = False
show_butt_status = False
box_status = False
show1_butt_box_status = False
show2_butt_box_status = False
a = False

nextFrame1 = timer()
nextFrame2 = timer()
c1 = False

def menu_loop():
	global run, game_loop_status
	
	play_butt_col = (255,255,255)
	exit_butt_col = (255,255,255)
	while run:
		win.blit(backround, (0,0)) #backround
		win.blit(ground, (0, 500-37)) #ground
		win.blit(ground, (1080, 500-33)) #ground

		name = font4.render("Cannon Game", True, (255,255,255))
		win.blit(name, (440,100))
		
		pos = pygame.mouse.get_pos()
		press = pygame.mouse.get_pressed()

		if (510 < pos[0] < 510+100) and (250 < pos[1] < 250+50):
			play_butt_col = (128,128,128)
			if press[0] == 1:
				run = False
		elif  (510 < pos[0] < 510+100) and (320 < pos[1] < 320+50):
			exit_butt_col = (128,128,128)
			if press[0] == 1:
				pygame.quit()
		else:
			play_butt_col = (255,255,255)
			exit_butt_col = (255,255,255)
		#font
		play_butt_text = font.render("Play", True, play_butt_col)
		exit_butt_text = font.render("Exit", True, exit_butt_col)
		#play button
		pygame.draw.rect(win, play_butt_col, pygame.Rect(510,250,100,50), 3)
		win.blit(play_butt_text, (535, 262.5))
		#exit button
		pygame.draw.rect(win, exit_butt_col, pygame.Rect(510,320,100,50), 3)
		win.blit(exit_butt_text, (535, 332.5))

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
		pygame.display.update()
		clock.tick(60)

	game_loop_status = True
	run = True

def game_loop():

	global x, y, power, angle, time,a,nextFrame1,nextFrame2
	global run, shoot, nextFrame, q2, q4,game_loop_status
	global enemy_index, explosion_status, explosion_index,walkX,enemy_pos,enemy_die,enemy_die_status,enemy_index2
	while run:
		if shoot:
			if golfBall.y < (500 - 35) - golfBall.radius:
				time += 0.1
				time = round(time,2)
				po = ball.ballPath(x, y, power, angle, time)
				golfBall.x = po[0]
				golfBall.y = po[1]
				
			else:
				shoot = False
				if golfBall.x+13 >= enemy_pos[0] and golfBall.x+13 <= enemy_pos[0]+105:
					enemy_die_status = True
					a = True

				explosion_status = True
				explosion_pos[0], explosion_pos[1] = golfBall.x, golfBall.y
	

				dot.append((golfBall.x, golfBall.y))
				#po[2] is veilocityX, po[3] is distanceX
				data.append((power, math.degrees(angle), time, po[2], po[3]))

				time = 0
				golfBall.x = 85
				golfBall.y = 415

		pos = pygame.mouse.get_pos()
		press = pygame.mouse.get_pressed()
		line = [(golfBall.x, golfBall.y), pos]
		
		redrawWindow(line,pos,press)

		#enemy
		if timer() > nextFrame1:
			enemy_index = (enemy_index+1)%4
			if explosion_status == True:
				explosion_index += 1
			nextFrame1 += 80		
		if enemy_die_status == False:
			if walkX == enemy_pos[0]:
				win.blit(enemy[enemy_index], (enemy_pos[0], 370))
			else:
				win.blit(walk[enemy_index], (walkX, 365))
				walkX -= 1
				print(enemy_pos[0], walkX)
		elif enemy_die_status == True:
			win.blit(enemy_die[enemy_index], (enemy_pos[0], 370))

		print("enemy_index ", enemy_index)

		if enemy_index == 3 and walkX == enemy_pos[0]:
			enemy_index = 0
			enemy_die_status = False
		if enemy_index2 == 3 and walkX == enemy_pos[0]:
			print(111111111111111111)
			enemy_index2 = 0
			a = False
		
		if explosion_status == True and explosion_index <= 11:
			win.blit(explosion[explosion_index], (((dot[len(dot)-1][0])-65), (dot[len(dot)-1][1])-100) )
			if explosion_index == 11:
				explosion_status = False
				explosion_index = 0
				if a == True:
					walkX = 1160
					enemy_pos[0] = random.randint(85+100, (85+900))		
					a = False

		if shoot == False:
			angle = findAngle(pos)
			power = round(math.sqrt( ((pos[0] - golfBall.x)**2) + ((pos[1] - golfBall.y)**2) ) / 9)
			if math.degrees(angle) > 90 and math.degrees(angle) <= 180:
				q2 = True
				q4 = False
			elif math.degrees(angle) >= 270 and math.degrees(angle) <= 360:
				q2 = False
				q4 = True
			if math.degrees(angle) > 90 and q2 == True:
				angle = 1.5707963267948966
			elif  math.degrees(angle) > 90 and q4 == True:
				angle = 0

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
			if event.type == pygame.MOUSEBUTTONDOWN and not((1015 < pos[0] < 1015+130) and (90 < pos[1] < 140+50)):
				if shoot == False:
					shoot = True
					x = golfBall.x
					y = golfBall.y

		pygame.display.update()
		clock.tick(60)

	game_loop_status = False
	run = True

while True:

	if game_loop_status == True:
		walkX = 1160
		enemy_pos[0] = random.randint(85+100, (85+900))
		game_loop()
	else:
		menu_loop()