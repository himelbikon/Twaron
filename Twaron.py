from collections import defaultdict
from pygame import mixer
import pygame, os, random, math, time

pygame.font.init()
pygame.mixer.init()

def img_loader(file, size):
	return pygame.transform.scale(pygame.image.load(os.path.join('twaron_data', file)), size)

width, height = 1200, 600
black = 0, 0, 0
white = 255, 255, 255


# Frsit row
tree = img_loader('tree.png', (200, 350))
tree_2 = img_loader('tree_2.png', (200, 350))
build = img_loader('build.png', (200, 350))
build_2 = img_loader('build_2.png', (200, 350))
build_3 = img_loader('build_3.png', (200, 350))
build_4 = img_loader('build_4.png', (200, 350))
build_5 = img_loader('build_5.png', (200, 350))
build_6 = img_loader('build_6.png', (200, 350))
build_7 = img_loader('build_7.png', (200, 350))

obj_list_1 = [tree, tree_2, build, build_2, build_3, build_4, build_5, build_6, build_7]

# Last row
o1 = img_loader('o1.png', (300, 450))
o2 = img_loader('o2.png', (300, 450))
o3 = img_loader('o3.png', (300, 450))
o4 = img_loader('o4.png', (300, 450))
o5 = img_loader('o5.png', (300, 450))
o6 = img_loader('o6.png', (300, 450))
o7 = img_loader('o7.png', (300, 450))

# Background
bg = img_loader('background.jpg', (width*5, height+300))
gr = img_loader('ground.jpg', (width+150, 150))
gr_2 = img_loader('ground.jpg', (width+150, 150))

obj_list_2 = [o1, o2, o3, o4, o5, o6, o7]

# Ships & Bullets
hero_img = img_loader('hero.png', (100, 100))
hero_bullet_img = img_loader('hero_bullet.png', (10, 10))
hero_life_img = img_loader('hero.png', (50, 50))

villain_img = img_loader('villain.png', (350, 250))
villain_bullet_img = img_loader('villain_bullet.png', (25, 25))


win = pygame.display.set_mode((width, height))
pygame.display.set_caption('Twaron')

def bg_runner(x):
	if x < -bg.get_width() + 100 + width:
		x -= 0
	else:
		x -= 0.1
	return x

def gr_runner(x, vel):
	if x < -gr.get_width():
		x = width
	else:
		x -= vel
	return x

def obj_selection(list):
	return random.choice(list)

def obj_runner(var, obj, vel, list):
	if var < -350:
		var = random.randrange(1550, 2000)
		obj = obj_selection(list)
	else:
		var -= vel
	return var, obj


class Ship:
	def __init__(self, x, y, health=100):
		self.x = x
		self.y = y
		self.health = health
		#self.bullet_img = None
		#self.bullet_img = None
		#self.bullets = []
		self.cool_down_time = 0
		self.bul_dict = defaultdict(list)


	def draw(self):
		win.blit(self.ship_img, (self.x, self.y))
		for x in list(self.bul_dict):
			x.draw()

	def get_width(self):
		return self.ship_img.get_width()

	def get_height(self):
		return self.ship_img.get_height()

	def shoot(self, time, deg, vel, dam):
		if self.cool_down_time >= time:
			x = self.x + self.ship_img.get_width()
			y = self.y + self.ship_img.get_height() / 2 - self.bullet_img.get_height() / 2
			bullet = Bullet(x, y, self.bullet_img)
			self.bul_dict[bullet].append(deg)
			self.bul_dict[bullet].append(vel)
			self.bul_dict[bullet].append(dam)
			self.cool_down_time = 0
		elif self.cool_down_time < time:
			self.cool_down_time += 1

	def move_bullet(self, obj):
		for bullet in list(self.bul_dict):
			deg = self.bul_dict[bullet][0]
			r = self.bul_dict[bullet][1]
			dam = self.bul_dict[bullet][2]
			bullet.move(r, deg)
			if bullet.off_screen():
				if bullet in self.bul_dict:
					self.bul_dict.pop(bullet)
			if bullet.collision(obj):
				if bullet in self.bul_dict:
					self.bul_dict.pop(bullet)
				if obj.health - dam < 0:
					obj.health = 0
				else:
					obj.health -= dam

class Hero(Ship):
	def __init__(self, x, y):
		super().__init__(x, y)
		self.ship_img = hero_img
		self.bullet_img = hero_bullet_img
		self.mask = pygame.mask.from_surface(self.ship_img)
		self.health = 3

class Villain(Ship):
	def __init__(self, x, y, health=100):
		super().__init__(x, y, health)
		self.ship_img = villain_img
		self.bullet_img = villain_bullet_img
		self.mask = pygame.mask.from_surface(self.ship_img)

	def move_bullet(self, obj):
		for bullet in list(self.bul_dict):
			deg = self.bul_dict[bullet][0]
			r = self.bul_dict[bullet][1]
			dam = self.bul_dict[bullet][2]
			bullet.move(r, deg)
			if bullet.off_screen():
				if bullet in self.bul_dict:
					self.bul_dict.pop(bullet)
			if bullet.collision(obj):
				if bullet in self.bul_dict:
					self.bul_dict.pop(bullet)
				if obj.health - dam < 0:
					obj.health = 0
				else:
					obj.health -= dam

				obj.x = - 150 - obj.get_width()
		
class Bullet:
	def __init__(self, x, y, img):
		self.x = x
		self.y = y
		self.img = img
		self.mask = pygame.mask.from_surface(self.img)

	def draw(self):
		win.blit(self.img, (self.x, self.y))

	def move(self, r, deg):
		#red = deg * 3.1416 / 180
		rad = math.radians(deg)
		self.x += r * (math.cos(rad))
		self.y += r * (math.sin(rad))

	def off_screen(self):
		return not (0 < self.x < width and 0 < self.y < height)

	def collision(self, obj):
		return collide(self, obj)

def collide(obj1, obj2):
	offset_x = int(obj2.x - obj1.x)
	offset_y = int(obj2.y - obj1.y)
	return obj1.mask.overlap(obj2.mask, (offset_x, offset_y))

def following_shoot(obj1, obj2):
	x = obj1.x + obj1.get_width()/2 - obj2.x - obj2.get_width()
	y = obj1.y + obj1.get_height()/2 - obj2.y - obj2.get_height()/2
	return x, y

def ran_cor(obj, x1, y1):
	x = random.randrange(600-100, width - obj.get_width())
	y = random.randrange(0, height - obj.get_height())
	if math.sqrt((x-x1)**2 + (y-y1)**2) > 200:
		return x, y
	else:
		return x1, y1

def follower(obj, target):
	x = target.x + target.get_width() / 2 - obj.x - obj.get_width() + 0.0001
	y = target.y + target.get_height() / 2 - obj.y - obj.get_height() / 2 + 0.0001
	if x >= 0 and y >= 0:
		extra = math.atan(abs(y) / abs(x))
	elif x < 0 and y >= 0:
		extra = math.pi - math.atan(abs(y) / abs(x))
	elif x < 0 and y < 0:
		extra = math.pi + math.atan(abs(y) / abs(x))
	elif x >= 0 and y < 0:
		extra = 2 * math.pi - math.atan(abs(y) / abs(x))
	ang = math.degrees(extra)
	return ang

ang_inc = 0

def shooter(con, choice, obj, target):
	global ang_inc
	vel = 8
	#choice = 500

	if con == True:
		if choice == 0:
			obj.shoot(1, random.randrange(90, 270), vel, 1)
		elif choice == 1:
			ang = follower(obj, target)
			obj.shoot(1*60, ang, vel*2, 1)
		elif choice == 2:
			obj.shoot(1, ang_inc, 3+vel, 1)
			ang_inc += 7
		elif choice == 3:
			for i in range(0, 361, 7):
				obj.shoot(0.5*60, i, vel, 1)
		elif choice == 4:
			for i in range(130, 225, 10):
				obj.shoot(0.8*60, i, vel, 1)
		elif choice == 5:
			obj.shoot(0.1*60, random.randrange(160, 200), 1.5*vel, 1)
			

	else:
		ang_inc = 0



def main():
	run = True
	fps = 60
	clock = pygame.time.Clock()
	run_obj_x = 1300
	run_obj_x_2 = 1250
	obj = obj_selection(obj_list_1)
	obj_2 = obj_selection(obj_list_2)

	bg_x = 0

	gr_x = 0
	gr_2_x = gr.get_width()-100

	hero = Hero(20, 200)
	hero_vel = 5
	hero_firing_delay = 0.08
	hero_life = 3
	hero_bul_dam = 0.05

	bullet_vel = 8

	villain = Villain(width - 50 - villain_img.get_width(), 100)
	vil_hel_bar_hei = 10
	vil_hel_bar_wid = 305
	vil_bul_dam = 1
	vil_pos_changer = False
	vil_vel = 0.5
	vil_shoot = False
	vil_shoot_counter = 3
	vil_bul_vel = 8

	style_cho = 0
	cho_start = 0
	cho_stop = 6


	ran_cor_x = 300
	ran_cor_y = 300

	gv = False
	gv_des = 'You can rest in peace now','It was worth trying...'

	main_font = pygame.font.SysFont('comicsans', 20)
	gv_font = pygame.font.SysFont('Times New Roman', 100)
	nor_font = pygame.font.SysFont('Courier', 30)

	won_font = pygame.font.SysFont('Times New Roman', 40)
	won_label = won_font.render(f'Himel Bikon is down, You have won!', 1, (255,0,0))

	go_home_label = nor_font.render(f'Come to HQ, Major is waiting for you...', 1, (255,0,0))


	def redraw_window():
		win.fill(white)

		win.blit(bg, (bg_x, -250))

		win.blit(gr, (gr_x, height-150))
		win.blit(gr_2, (gr_2_x, height-150))

		win.blit(obj_2, (run_obj_x_2, 50))
		win.blit(obj, (run_obj_x, 250))

		if hero.health > 0:
			for i in range(hero.health):
				win.blit(hero_life_img, (30 + hero_life_img.get_width() * i, 10))

		if villain.health <= 0:
			win.blit(won_label, (width/2 - won_label.get_width()/2, 200))
			win.blit(go_home_label, (width/2 - go_home_label.get_width()/2, 250))

		villain.draw()
		hero.draw()

		vil_life_label = main_font.render(f'Himel Bikon', 1, (10,10,255))
		win.blit(vil_life_label, (800, 10))

		gv_label = gv_font.render(f'Gave Over', 1, (255,0,0))
		gv_des_label_0 = nor_font.render(f'{gv_des[0]}', 1, (255,10,10))
		gv_des_label_1 = nor_font.render(f'{gv_des[1]}', 1, (255,10,10))


		if gv == True:
			win.blit(gv_label, (50, 100))
			win.blit(gv_des_label_0, (250, 90 + gv_label.get_height()))
			win.blit(gv_des_label_1, (280, 220))


		

		pygame.draw.rect(win, (255,0,0), (vil_life_label.get_width() + 806, 11, vil_hel_bar_wid*villain.health/100, vil_hel_bar_hei))
		pygame.draw.rect(win, (150,150,150), (vil_life_label.get_width() + 805, 10, vil_hel_bar_wid + 2, vil_hel_bar_hei + 2), 2)

		pygame.display.update()

	while run:
		clock.tick(fps)
		redraw_window()

		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				quit()

		if hero.health < 1:
			hero.x = -900
			hero.y = -900
			vil_shoot = False
			gv = True

			
		run_obj_x, obj = obj_runner(run_obj_x, obj, 10, obj_list_1)
		run_obj_x_2, obj_2 = obj_runner(run_obj_x_2, obj_2, 1, obj_list_2)

		bg_x = bg_runner(bg_x)

		gr_x = gr_runner(gr_x, 1)
		gr_2_x = gr_runner(gr_2_x, 1)

		keys = pygame.key.get_pressed()
		if keys[pygame.K_RIGHT] and hero.x + hero.get_width() < width:
			hero.x += hero_vel
		if keys[pygame.K_LEFT] and hero.x > 0:
			hero.x -= hero_vel
		if keys[pygame.K_UP] and hero.y > 0:
			hero.y -= hero_vel
		if keys[pygame.K_DOWN] and hero.y + hero.get_height() < height:
			hero.y += hero_vel
		if keys[pygame.K_SPACE]:
			hero.shoot(hero_firing_delay * fps, 0, bullet_vel, 110*hero_bul_dam) # time, degree, velocity, damage


		if hero.x < -4:
			hero.x += hero_vel-2
			villain.bul_dict.clear()

		if villain.health > 0:
			if vil_pos_changer == True:
				if abs(ran_cor_x - villain.x) <= vil_vel or abs(ran_cor_y - villain.y) <= vil_vel:
					vil_pos_changer = False
					if vil_shoot_counter >= 6:
						vil_shoot = not vil_shoot
						vil_shoot_counter = 0
						style_cho = random.randrange(cho_start, cho_stop)
					else:
						vil_shoot_counter += 1
				else:
					if ran_cor_x < villain.x:
						villain.x -= vil_vel
					elif ran_cor_x > villain.y:
						villain.x += vil_vel
					if ran_cor_y < villain.y:
						villain.y -= vil_vel
					elif ran_cor_y > villain.y:
						villain.y += vil_vel
			else:
				ran_cor_x, ran_cor_y = ran_cor(villain, ran_cor_x, ran_cor_y)
				vil_pos_changer = True
		elif villain.health <= 0:
			if villain.y < height - villain.get_height() + 100:
				villain.y += 3
				vil_shoot = False
			elif villain.y >= height - villain.get_height() + 100 and villain.x > -900:
				villain.x -= 2




		shooter(vil_shoot, style_cho, villain, hero)
		
		villain.move_bullet(hero)
		hero.move_bullet(villain) 


def intro():
	run = True
	clock = pygame.time.Clock()
	run_obj_x = 1300
	run_obj_x_2 = 1250
	obj = obj_selection(obj_list_1)
	obj_2 = obj_selection(obj_list_2)

	bg_x = 0

	gr_x = 0
	gr_2_x = gr.get_width()-100

	main_font = pygame.font.SysFont('Courier', 30)
	intro_font = pygame.font.SysFont('Times New Roman', 100)
	nor_font = pygame.font.SysFont('Times New Roman', 60)

	game_name_label = intro_font.render(f'Twaron', 1, (255,0,0))
	gn_x = width/2 - game_name_label.get_width()/2
	gn_y = 100

	d_x = width / 2
	d_y = gn_y + game_name_label.get_height()

	des_list = ['Made by Himel Bikon by using Python and Pygame', 'www.github.com/himelbikon', 'www.facebook.com/himelbikon', 'www.instagram.com/bikonhimel']

	sim_but_col = 112, 6, 9
	play_but_col = sim_but_col
	exit_but_col = sim_but_col
	on_but_col = 255, 0, 7
	play_but_label = nor_font.render(f'Play', 1, (play_but_col))
	pbl_x = 300 - play_but_label.get_width() / 2
	pbl_y = 400

	exit_but_label = nor_font.render(f'Exit', 1, (exit_but_col))
	ebl_x = width - pbl_x - exit_but_label.get_width() / 2
	ebl_y = 400

	
	mixer.music.load(os.path.join('twaron_data', 'background.wav'))
	mixer.music.play(-1)

	while run:
		clock.tick(60)



		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				pygame.quit()
				quit()

		run_obj_x, obj = obj_runner(run_obj_x, obj, 10, obj_list_1)
		run_obj_x_2, obj_2 = obj_runner(run_obj_x_2, obj_2, 1, obj_list_2)
		bg_x = bg_runner(bg_x)
		gr_x = gr_runner(gr_x, 1)
		gr_2_x = gr_runner(gr_2_x, 1)


		# Draw section
		win.blit(bg, (bg_x, -250))
		win.blit(gr, (gr_x, height-150))
		win.blit(gr_2, (gr_2_x, height-150))
		win.blit(obj_2, (run_obj_x_2, 50))

		win.blit(game_name_label, (gn_x, gn_y))

		for i in range(len(des_list)):
			des_label = main_font.render(f'{des_list[i]}', 1, (11, 156, 23))
			win.blit(des_label, (d_x - des_label.get_width()/2 , d_y + i * des_label.get_height()))

		win.blit(play_but_label, (pbl_x, pbl_y))
		win.blit(exit_but_label, (ebl_x, ebl_y))

		mouse = pygame.mouse.get_pos()
		click = pygame.mouse.get_pressed()

		if pbl_x <= mouse[0] <= pbl_x + play_but_label.get_width() and pbl_y <= mouse[1] <= pbl_y + play_but_label.get_height():
			play_but_col = on_but_col
			if click[0] == 1:
				mixer.music.stop()
				main()
		else:
			play_but_col = sim_but_col

		if ebl_x <= mouse[0] <= ebl_x + exit_but_label.get_width() and ebl_y <= mouse[1] <= ebl_y + exit_but_label.get_height():
			exit_but_col = on_but_col
			if click[0] == 1:
				quit()

		else:
			exit_but_col = sim_but_col

		play_but_label = nor_font.render(f'Play', 1, (play_but_col))
		exit_but_label = nor_font.render(f'Exit', 1, (exit_but_col))
		pygame.display.update()
 

intro()

quit()