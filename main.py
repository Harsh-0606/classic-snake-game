from math import trunc
import pygame
import time
from pygame import surface
from pygame.locals import *
import random

from pygame.mixer import Sound

SIZE=40

class Apple:
    def __init__(self,surface):
        self.parentSurface=surface
        self.apple=pygame.image.load('resources/apple.jpg')
        self.x=120
        self.y=120
    
    def draw(self):
        self.parentSurface.blit(self.apple,(self.x,self.y))      
        pygame.display.update()
    
    def move(self):
        self.x=random.randint(1,19)*40
        self.y=random.randint(1,19)*40
        
class Snake:
    def __init__(self, surface,length):
        self.parentSurface= surface
        self.block=pygame.image.load("resources/block.jpg").convert()
        self.length=length
        self.block_x=[SIZE]*self.length
        self.block_y=[SIZE]*self.length
        self.direction= 'right'
    
    def increaseLength(self):
        self.length+=1
        self.block_x.append(-1)
        self.block_y.append(-1)

    def moveLeft(self):
        self.direction = 'left' 

    def moveRight(self):
        self.direction = 'right' 

    def moveUP(self):
        self.direction = 'up' 

    def moveDown(self):
        self.direction = 'down' 

    def walk(self):
        for i in range(self.length-1,0,-1):
            self.block_x[i]=self.block_x[i-1]
            self.block_y[i]=self.block_y[i-1]            

        if self.direction is 'down': 
            self.block_y[0]+=40
        if self.direction is 'up': 
            self.block_y[0]-=40
        if self.direction is 'left': 
            self.block_x[0]-=40
        if self.direction is 'right': 
            self.block_x[0]+=40
        self.draw()
    

    def draw(self):
        
        for i in range(self.length):
            self.parentSurface.blit(self.block,(self.block_x[i],self.block_y[i]))           #blit is used for drawing stuff
        pygame.display.update()  


class Game:
    def __init__(self):
        pygame.init()
        pygame.mixer.init()
        self.bgMusic()
        self.surface=pygame.display.set_mode((800,800))     #making screen
        self.bgimage()                     #setting colour of the background
        self.snake = Snake(self.surface,1)
        self.snake.draw()
        self.apple= Apple(self.surface)
        self.apple.draw()

    def isCollision(self,x1,y1,x2,y2):
        if(x1==x2 and y1==y2):
            return True
        return False

    def bgMusic(self):
        pygame.mixer.music.load('resources/bg_music_1.mp3')
        pygame.mixer.music.play()

    def bgimage(self):
        bg=pygame.image.load('resources/background.jpg')
        self.surface.blit(bg,(0,0))

    def score(self):
        font=pygame.font.SysFont('ariel',30)
        score=font.render(f'score:{self.snake.length}',True,(255,255,255)) 
        self.surface.blit(score,(700,10))

    def play(self):
        self.bgimage()
        self.snake.walk()
        self.apple.draw()
        self.score()
        pygame.display.update()

        # snake and apple
        if self.isCollision( self.snake.block_x[0],self.snake.block_y[0],self.apple.x,self.apple.y):
            sound=pygame.mixer.Sound('resources/1_snake_game_resources_ding.mp3')
            pygame.mixer.Sound.play(sound) 
            self.snake.increaseLength()
            self.apple.move()
        
        # snake and itself
        for i in range(2 ,self.snake.length):
            if self.isCollision( self.snake.block_x[0],self.snake.block_y[0], self.snake.block_x[i],self.snake.block_y[i]):
                sound=pygame.mixer.Sound('resources/1_snake_game_resources_crash.mp3')
                pygame.mixer.Sound.play(sound) 
                raise "Game Over"

        if (self.snake.block_x[0]==0 or self.snake.block_x[0]==800 or self.snake.block_y[0]==0 or self.snake.block_y[0]==800):
            sound=pygame.mixer.Sound('resources/1_snake_game_resources_crash.mp3')
            pygame.mixer.Sound.play(sound) 
            raise "Game Over"

    def show_game_over(self):
        self.bgimage()
        font=pygame.font.SysFont('ariel',30)
        gameOver=font.render('GAME OVER',True,(0,0,0)) 
        self.surface.blit(gameOver,(350,380))
        gameOver=font.render('ENTER TO PLAY AGAIN',True,(0,0,0)) 
        self.surface.blit(gameOver,(350,420))
        pygame.display.update()
        pygame.mixer.music.pause()

    def reset(self):
        self.snake= Snake(self.surface,1)
        self.apple= Apple(self.surface)

    def run(self):
        running=True

        while(running):
            for event in pygame.event.get():
                if event.type== KEYDOWN:
                    if event.key == K_RETURN:
                        pause=False
                        pygame.mixer.music.unpause()

                    if  event.key== K_ESCAPE:
                        running=False
                    if event.key== K_UP:
                        self.snake.moveUP()
                    if event.key== K_DOWN:
                        self.snake.moveDown()
                    if event.key== K_RIGHT:
                        self.snake.moveRight()
                    if event.key== K_LEFT:
                        self.snake.moveLeft()

                elif event.type==QUIT:
                    running=False
            
            try:
                if not pause:
                    self.play()
            except Exception as e:
                self.show_game_over()
                pause=True 
                self.reset()
            time.sleep(.2 )

if __name__=="__main__": 
    
    game= Game()
    game.run()

