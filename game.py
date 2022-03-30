import pygame
import sys
import random


class Game: 
    VER, HOR, SIDE = 15, 18, 30 
    WIDTH, HEIGHT = SIDE*VER, SIDE*HOR+SIDE*2
    score  = 0
    count = 1
    paused = over=False
    powercount=0
    eventlist=[]
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Snake Game")
        self.screen = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.HEADER = pygame.image.load("assets/header.png")
        self.GAMEOVER=pygame.image.load("assets/gameover.png")
        self.FONT   = pygame.font.Font('freesansbold.ttf', 17)
        self.FOOD   = [pygame.image.load(f"assets/food{i}.png") for i in range(5)]
        self.POWERUPS = [pygame.image.load(f"assets/food{i}.png") for i in range(3)]
        self.col = [random.randint(0,15)*self.SIDE + 3 for _ in range(len(self.FOOD))]
        self.row = [random.randint(0,18)*self.SIDE+self.SIDE*2 + 3 for _ in range(len(self.FOOD))]
        
    def wait_and_run(self, time):
        event = pygame.USEREVENT+self.count
        self.eventlist.append(event)
        self.count += 1
        pygame.time.set_timer(event ,time) 
        return event
    
    def scored(self,increase):
        if increase: self.score += 5
        else:   self.score -= 3
        
    def draw_screen(self):
        for line in range(self.VER):
            pygame.draw.line(self.screen,"white",(self.SIDE*line,self.SIDE*2),(self.SIDE*line,self.HEIGHT))
        for line in range(self.HOR):  
            pygame.draw.line(self.screen,"white",(0,self.SIDE*line+self.SIDE*2), (self.WIDTH,self.SIDE*line+self.SIDE*2))
        pygame.draw.rect(self.screen, "blue", pygame.Rect(0, self.SIDE*2, self.WIDTH, self.HEIGHT-self.SIDE*2),  5)
        self.screen.blit(self.HEADER,(0,0))
        text = self.FONT.render(f'Score:{self.score}', True, (0,255,0))
        self.screen.blit(text, (2,self.SIDE+5))
        if self.over: self.screen.blit(self.GAMEOVER,(25,125))
        
        if not self.paused:
            for f in range(len(self.FOOD)):  self.screen.blit(self.FOOD[f], (self.col[f],self.row[f]))

    def spawn_food(self,f):
        self.col[f] = random.randint(0,15)*self.SIDE + 3
        self.row[f] = random.randint(0,18)*self.SIDE+self.SIDE*2 + 3
        
    def powerups(self,time):
        if self.powercount % 2 == 0:
            powerup = random.choice(self.POWERUPS)
            
        self.powercount += 1
    
    def pause(self,gameover=False):
        self.over = gameover
        self.paused = True
        
    def restart(self,snake):
        self.paused = self.over = False
        snake.tails = 1
        snake.x,snake.y = self.SIDE*random.randint(4,9), self.SIDE*random.randint(3,7)
        snake.pos = [(snake.x,snake.y)]
        snake.direction = "down"
        self.score = 0
        snake.colour = random.choice(["blue", "red", "green", "grey"])
        
        
class Snake:
    tails=1
    pos =[]
    
    def __init__(self,screen,xcor,ycor,colour=random.choice(["blue", "red", "green", "grey"])):
        self.screen = screen
        self.x = Game.SIDE*random.randint(4,9)
        self.y = Game.SIDE*random.randint(3,7) 
        self.colour = colour
        self.direction = "down"
        self.pos.append((xcor,ycor))
        
    def draw(self):
        for block in range(1,self.tails+1):
            xcor,ycor = self.pos[-block][0], self.pos[-block][1]
            c=self.colour
            try: 
                if block==1:    c= "dark"+self.colour
                pygame.draw.rect(self.screen, c, pygame.Rect(xcor,ycor, Game.SIDE, Game.SIDE),border_radius=random.randint(2,4)  )
            except: 
                print(self.colour)

            
    def didturn(self,event):
        if   event.key == pygame.K_LEFT  and (self.direction!="right" or self.tails==1):   self.direction = "left" 
        elif event.key == pygame.K_RIGHT and (self.direction!="left"  or self.tails==1):   self.direction = "right"
        elif event.key == pygame.K_UP    and (self.direction!="down"  or self.tails==1):   self.direction = "up"
        elif event.key == pygame.K_DOWN  and (self.direction!="up"    or self.tails==1):   self.direction = "down" 
        
    def move(self,game): 
        self.did_eat_tail(game)
        for x in range(len(game.FOOD)):
            if self.x == game.col[x]-3 and self.y == game.row[x]-3:
                game.scored(True)
                self.tails += 1
                game.col[x],game.row[x]=Game.WIDTH*2,Game.HEIGHT*2
            
        if (-Game.SIDE < self.x < Game.WIDTH) and (Game.SIDE < self.y < Game.HEIGHT):
            if   self.direction == "left" :   self.x -= Game.SIDE
            elif self.direction == "right":   self.x += Game.SIDE
            elif self.direction == "up"   :   self.y -= Game.SIDE
            elif self.direction == "down" :   self.y += Game.SIDE 
        else: game.pause(True)
        
        try:    self.pos.append((self.x,self.y))
        except MemoryError: self.pos = self.pos[50:]
        
    def did_eat_tail(self,game):
        if (self.x, self.y) in self.pos[-self.tails:-1]:
            game.pause(True)

            
snakegame = Game()
makeamove = snakegame.wait_and_run(650)
snake = Snake(snakegame.screen,xcor=5,ycor=5)
foodspawn = [snakegame.wait_and_run(random.randint(10000,20000)) for t in range(len(snakegame.FOOD))]
placepowerup = snakegame.wait_and_run(25000)

# Main Loop
while 1:
    snakegame.screen.fill((0,0,0))
    
    for event in pygame.event.get():
        if   event.type == pygame.QUIT: sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos(); print(pos)
            if snakegame.paused and (45<pos[0]<110) and (435<pos[1]<500):   snakegame.restart(snake) 
        elif event.type == pygame.KEYDOWN:  snake.didturn(event)
        elif event.type == makeamove and not snakegame.paused:   snake.move(snakegame)
        elif event.type in foodspawn and not snakegame.paused:   snakegame.spawn_food(foodspawn.index(event.type))
        elif event.type == placepowerup and not snakegame.paused:snakegame.powerups(25000)
     
    snake.draw()
    snakegame.draw_screen() 
    
    pygame.display.update()
