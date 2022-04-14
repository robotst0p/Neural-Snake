import numpy as np
import pygame 
import random


class Environment:
    def __init__(self,pygame,width,height,cellsize,fr):
        #game elements
        self.pygame = pygame
        self.width = width
        self.height = height
        self.cellsize = cellsize
        self.fr = fr
        #pad for border
        self.board = np.pad(np.zeros([self.width-1,self.height-1]),
                            pad_width=(1,1),mode='constant',constant_values = 2)
        
        #game stats
        self.session_highscore = 0
        self.n_games = 0


    #COORDINATE PROGRAM LOOP AND UTILITY FUNCTIONS
    def Main(self):
        #initialize pygame and surface animation
        self.pygame.init() 
        self.surface = pygame.display.set_mode(((self.width+1)*self.cellsize,
                                                (self.height+1)*self.cellsize)) 
        #intiialize board and snake
        self.initialize_game()
    
        
        #main program loop
        while True:     
            keypress = False

            for event in self.pygame.event.get(): 
                self.Event = event
                #exit window
                if self.Event.type == self.pygame.QUIT:
                    self.pygame.quit()
                    quit()
                    return

                #if there is user input, update function takes key press
                elif self.Event.type == self.pygame.KEYDOWN:
                    pygame.time.delay(self.fr)

                    #illegal moves!!!
                    if self.snake_head.get('hed')[2] == 'up' and self.pygame.key.name(self.Event.key)    == 'down' or \
                       self.snake_head.get('hed')[2] == 'down' and self.pygame.key.name(self.Event.key)  == 'up'   or \
                       self.snake_head.get('hed')[2] == 'right' and self.pygame.key.name(self.Event.key) == 'left' or \
                       self.snake_head.get('hed')[2] == 'left' and self.pygame.key.name(self.Event.key)  == 'right':

                       self.update_environment(self.snake_head.get('hed')[2])
                       break
                    #legal moves
                    else:
                        self.update_environment((pygame.key.name(self.Event.key)))
                        self.draw_board()
                        keypress = True

            #if there is no user input, update function takes last dir
            if keypress == False:
                pygame.time.delay(self.fr)
                self.update_environment(self.snake_head.get('hed')[2])
                self.draw_board()

    #INITIALIZE GAME OBJECTS AND BOARD
    def initialize_game(self):
       
        #snake head dict contains head coords, and also current direction
        self.snake_head = {
                            'hed' : ([random.randint(10,self.width-10),
                                      random.randint(10,self.height-10),'up'])
        }
        #snake body, empty on init
        self.snake_body = {
        }
        #number of segments, 0 on init
        self.segments = 0
        #spawn food
        self.food = [random.randint(10,self.width-10),
                     random.randint(10,self.height-10)]
        self.board[self.food[0],self.food[1]] = 3

        #head on board
        self.board[self.snake_head.get('hed')[0],
                   self.snake_head.get('hed')[1]] = 1

        #body on board
        for segment in self.snake_body:
            self.board[self.snake_body.get(segment)[0],
                       self.snake_body.get(segment)[1]] = 2
        #score and game info
        self.pygame.display.set_caption(f"SCORE: {self.segments}  -  SESSION HIGHSCORE: {self.session_highscore}  -  GAMES PLAYED: {self.n_games}")
        self.draw_board()

    #UPDATE ENVIRONMENT
    def update_environment(self,key):

        #conditionals for key presses
        if key == 'up':
            old_hed_pos = self.snake_head.get('hed')
            self.new_hed_pos = [old_hed_pos[0],old_hed_pos[1]-1,'up']
        elif key == 'down':
            old_hed_pos = self.snake_head.get('hed')
            self.new_hed_pos = [old_hed_pos[0],old_hed_pos[1]+1,'down']
        elif key == 'right':
            old_hed_pos = self.snake_head.get('hed')
            self.new_hed_pos = [old_hed_pos[0]+1,old_hed_pos[1],'right']
        elif key == 'left':
            old_hed_pos = self.snake_head.get('hed')
            self.new_hed_pos = [old_hed_pos[0]-1,old_hed_pos[1],'left']
        else:
            #if the user hits a key they shouldnt...
            self.update_environment(self.snake_head.get('hed')[2])
            return

        #head hits wall or self
        if self.board[self.new_hed_pos[0],self.new_hed_pos[1]] == 2:
            self.n_games += 1
            
            if self.segments > self.session_highscore:
                self.session_highscore = self.segments
            
            print(f'Highscore: {self.session_highscore}')
            print(f'n_games: {self.n_games}')
            pygame.time.delay(1800)
            self.initialize_game()
            return
            
        #if get food
        if self.board[self.new_hed_pos[0],self.new_hed_pos[1]] == 3 :
           self.grow_snake()
           self.update_environment(key)
           return

        #all legal moves    
        else:
            #reset board array for animation
            self.board = np.pad(np.zeros([self.width-1,self.height-1]),
                                pad_width=(1,1),mode='constant',constant_values = 2)
            #draw food
            self.board[self.food[0],self.food[1]] = 3

            #update coords of body segments
            self.old_body_pos = self.snake_body.copy()
            for segment in self.snake_body:
                #if neck
                if segment == '1':
                    new_values = self.snake_head.get('hed')
                    self.snake_body.update({'1': new_values})
                    #draw snake on board
                    self.board[self.snake_body.get('1')[0],self.snake_body.get('1')[1]] = 2
                #if body
                else:
                    key = f'{(int(segment)-1)}'
                    new_values = self.old_body_pos.get(key)
                    self.snake_body.update({segment: new_values})
                    #draw segment on board
                    self.board[self.snake_body.get(segment)[0],self.snake_body.get(segment)[1]] = 2

            #update head coordinates
            self.snake_head.update({'hed': self.new_hed_pos})
            #draw snake head 
            self.board[self.snake_head.get('hed')[0],self.snake_head.get('hed')[1]] = 1
            self.draw_board()

    #DRAW BOARD
    def draw_board(self):
        for r, c in np.ndindex(self.width+1,self.height+1): #+1 for wall pads
            if self.board[r,c] == 1: #head
                col = (0,0,255)
            elif self.board[r,c] == 2: #body / wall
                col = (255,0,0)
            elif self.board[r,c] == 3: #food
                col = (0,255,0)
            else:
                col = (0)
            self.pygame.draw.rect(self.surface, col, (r*self.cellsize, c*self.cellsize, 
                                                        self.cellsize-.03, self.cellsize-.03)) #draw new cell
        pygame.display.update() #updates display from new .draw in update function

    #GROW SNAKE WHEN EAT FOOD
    def grow_snake(self):
        self.pygame.display.set_caption(f"SCORE: {self.segments+1}  -  SESSION HIGHSCORE: {self.session_highscore}  -  GAMES PLAYED: {self.n_games}")
    
        #snake head dict contains head coords, and also current direction
        self.segments +=1 

        #new food - only spawns in empty spaces
        while True:
            self.food = [random.randint(10,self.width-3),
                        random.randint(10,self.height-3)]
            if self.board[self.food[0],self.food[1]] != 0:
                continue
            else:
                break

        #delete food
        self.board[self.new_hed_pos[0],self.new_hed_pos[1]] = 1

        if self.segments == 1:
            self.snake_body[f'{self.segments}'] = [self.snake_head.get('hed')[0],
                                                   self.snake_head.get('hed')[1]+1,
                                                   self.snake_head.get('hed')[2]]        
        else:
            key = f'{self.segments-1}'
            self.snake_body[f'{self.segments}'] = self.snake_body.get(key)

def main():
    game = Environment(pygame,
                       width = 50,
                       height = 30,
                       cellsize = 20,
                       fr = 30)
    game.Main()
main()
