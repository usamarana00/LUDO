import sys
import os.path
import random
import pygame
from pygame.locals import *

pygame.init()        

class window: #Defining the fixed constants for the window (with exception of chance) [ftw stands for 'for the window]
    def __init__(self,chance='R'): # Initiallizing window
        self.HEIGHT = 1000 # Height
        self.WIDTH = 750 # Width
        self.chance = chance # Variable which defines what to do next every step in the window
        self.maindisplay = pygame.display.set_mode((self.HEIGHT, self.WIDTH)) # Setting up main display window with given h/w
        self.ICON = pygame.image.load('data\ludo.jpg') # Setting the icon image locally
        pygame.display.set_icon(self.ICON) # Displaying the set icon on the window
        self.centre = pygame.image.load('data\ludo.jpg') # Setting the centre image
        self.red = pygame.image.load('data/red.png') # Setting the red team's image
        self.yellow = pygame.image.load('data\yellow.png') # Setting the yellow team's image
        self.blue = pygame.image.load('data/blue.png') # Setting the blue team's image
        self.green = pygame.image.load('data\green.png') # Setting the green team's image
        self.FONT = pygame.font.Font('data\ComicNeueSansID.ttf',18) # Setting up a default font for the text in the window
        self.about = self.FONT.render("About:",True,(255,255,255)) # Rendering up default 'about' display on the menu using the given font
        self.info = self.FONT.render("Ludo by Abdullah Mehtab",True,(255,255,255)) # Rendering up default display on the menu using the given font
        self.aand = self.FONT.render("and Usama Ayyub",True,(255,255,255)) # Rendering up default display on the menu using the given font

    def GetIcon(self): # Getter for Icon
        return self.ICON 

    def SetChance(self,chance): # Setter for 'chance', the main variable in control of everything
        self.chance = chance
        
    def GetChance(self): # Getter for 'chance', the main variable in control of everything
        return self.chance

    def GetFont(self): # Getter for the font that will be used to display text on the window
        return self.FONT

win = window() #Making object for the window class

class grid_obj: # A class to give every location in the grid its own object, which color it will have, its coordinate and everything
    def __init__(self, bg_color, p_list, safe, coordinate): # Initializing the grid_obj
        self.bg_color = bg_color # Setting up a color for the specific object 
        self.p_list = p_list # Defining the pieces list if a piece is involved on that specific object
        self.safe = safe # Checking for safe spots in the grid
        self.coordinate = coordinate # A specified coordinate for the specified object


class piece: # A class that will define every piece and initiate it onto the board later on
    def __init__(self, id, color, anim_state, coordinates, radius): # Initializing piece
        self.id = id # Giving ID to the peace (which team it belongs to)
        self.color = color # Defining its color
        self.anim_state = anim_state # Its animation state, if the team is in focus the piece will be highlighted, otherwise not
        self.coordinates = coordinates # Coordinate for every piece's location
        self.radius = radius # Default radius for every piece (CONSTANT)
        self.original_coordinate = coordinates #The initial coordinate where every piece will be defined in the first place


class circularlist: # # This class defines a list that will be edited in the program throughout through interactions and commands from dice, then send information to draw it on the board
    def __init__(self): # Initializing circular_list
        self.c_list = [(1, 6), (2, 6), (3, 6), (4, 6), (5, 6), (6, 5), (6, 4), (6, 3), (6, 2), (6, 1), (6, 0), (7, 0),
                       (8, 0), (8, 1),(8, 2), (8, 3), (8, 4), (8, 5), (9, 6), (10, 6), (11, 6), (12, 6), (13, 6), (14, 6), (14, 7),
                       (14, 8), (13, 8),(12, 8), (11, 8), (10, 8), (9, 8), (8, 9), (8, 10), (8, 11), (8, 12), (8, 13), (8, 14), (7, 14),
                       (6, 14), (6, 13),(6, 12), (6, 11), (6, 10), (6, 9), (5, 8), (4, 8), (3, 8), (2, 8), (1, 8), (0, 8), (0, 7),
                       (0, 6)] #Defining the default circular list (every movement's index)

    def move(self, init_pos, value, chance): # Method to define movement on the board, using initial position of when the method was called, what value to move it and which teams turn it is (chance)
        i = 0 # Resetting to default value on every iteration, 'i' is the default location for every piece and its team
        j = -1 # Resetting to default value on every iteration, 'j' is the checking factor for this method
        flag = 0 # Resetting to default value on every iteration
        while True: # Initiating a loop to check if every piece is in a legitimate position or not before movement
            if self.c_list[i] == init_pos or j >= 0: # Will only run in case the given initial position exists on the board (always)
                if chance == 'R' and i == 50: # If its red's turn and its in a legitimate position
                    flag = 1 # Setting flag to 1
                if chance == 'G' and i == 11: # If its green's turn and its in a legitimate position
                    flag = 2 # Setting flag to 2
                if chance == 'B' and i == 37: # If its blue's turn and its in a legitimate position
                    flag = 3 # Setting flag to 3 
                if chance == 'Y' and i == 24: # If its yellow's turn and its in a legitimate position
                    flag = 4 # Setting flag to 4
                j += 1 # Adding for every step until the needed value is reached
                if j == value: # Checking for value 
                    break # Breaking the loop :V
            i = (i + 1) % len(self.c_list) # Editing 'i' every step in correspondence to the circular list where positions are defined
        if flag == 1: # If flag is equal to 1 (Red's turn)
            return (self.c_list[i][0] + 1, self.c_list[i][1] + 1) # Moving the piece the amount specified
        elif flag == 2: # If flag is equal to 2 (Green's turn)
            return (self.c_list[i][0] + 1, self.c_list[i][1] + 1) # Moving the piece the amount specified
        elif flag == 3: # If flag is equal to 3 (Blue's turn)
            return (self.c_list[i][0] + 1, self.c_list[i][1] - 1) # Moving the piece the amount specified
        elif flag == 4: # If flag is equal to 4 (Yellow's turn)
            return (self.c_list[i][0] - 1, self.c_list[i][1] - 1) # Moving the piece the amount specified
        else: 
            return (self.c_list[i][0], self.c_list[i][1]) # Returning the original list itself in case of no movement

    def chk(self, pos): # Defining a method to specify the mouse clicks are inside the given locations, 'pos' is the variable holding all positions
        if pos in self.c_list: # If given position where action occured, exists in the c_list, only then will it continue editing itself
            return True # Returning True
        else: # Else it will remain what it was, unchanged
            return False # Returning False

Clicks = 0 # Global variable to define the amount of mouse interactions done in-game

class Instructions: # The class which will provide the user instructions in the game, during every movement check and specifing what to do
    def __init__(self): # Initializing Instructions
        self.piece = window(self) # Compositing window class in a variable
        self.FONT = self.piece.GetFont() # Getting the default font, which was pre-defined
        self.condit = 0 # Condition to display different texts 
        self.turn = self.FONT.render('Welcome to the Game!',True,(255,255,255)) # Initial display, when there are 0 clicks
        self.dicee = self.FONT.render('Click me!!!',True,(255,255,255)) # Specifiing where to click on every movement check
    
    def SetCondit(self,condit): # Setter for the condition variable
        self.condit = condit

    def GetCondit(self): # Getter for the condition variable
        return self.condit
    
    def turns(self): # Setting up variables depending on which team's turn it is, or is the dice supposed to clicked
        self.turn1 = self.FONT.render('Click on the',True,(255,255,255)) # Text display
        if self.condit == 'Red': # If its Red's turn
            self.turn = self.FONT.render('Red piece',True,(255,0,0)) # Red piece should be clicked (Text display)
        elif self.condit == 'Yellow': # If its Yellow's turn
            self.turn = self.FONT.render('Yellow piece',True,(255,255,0)) # Yellow piece should be clicked (Text display)
        elif self.condit == 'Blue': # If its Blue's turn
            self.turn = self.FONT.render('Blue piece',True,(0,0,255)) # Blue piece should be clicked (Text display)
        elif self.condit == 'Green': # If its Green's turn
            self.turn = self.FONT.render('Green piece',True,(0,255,0)) # Green piece should be clicked (Text display)
        elif self.condit == 'Dice': # If the dice should be clicked
            self.turn = self.FONT.render('Dice',True,(255,255,255)) # The dice should be clicked (Text display)
        self.turn3 = self.FONT.render('to continue',True,(255,255,255)) # Text display

    def textdisp(self): # Rendering the specified text onto the window
        global Clicks # Importing the amount of total clicks
        '''
        Rendering the pre-defined text onto the window on specific coordinates
        '''
        win.maindisplay.blit(win.about,(770,680))
        win.maindisplay.blit(win.info,(770,700)) 
        win.maindisplay.blit(win.aand,(770,720))
        win.maindisplay.blit(win.centre,(300,300))
        win.maindisplay.blit(win.red,(100,100))
        win.maindisplay.blit(win.blue,(100,550))
        win.maindisplay.blit(win.green,(575,125))
        win.maindisplay.blit(win.yellow,(550,550))
        if Clicks == 0: # Only for the initial click, asking to click the dice to start the game
            self.turn1 = self.turn3 = self.FONT.render('Click the Dice!',True,(255,255,255))
        else: # Else running the turns method to specify the turns
           Instructions.turns(self)
        win.maindisplay.blit(self.turn1,(800,100))
        win.maindisplay.blit(self.turn,(800,120))
        win.maindisplay.blit(self.turn3,(800,140))
        if self.condit == 'Dice': # If dice is supposed to be clicked
            win.maindisplay.blit(self.dicee,(830,280)) # Defining a specific text only for dice for it to be clicked


Game_grid = [[-1 for _ in range(15)] for _ in range(15)] # Defining the main game grid with all objects in it on every location
ins = Instructions() # Making object for the instructions class

class Board: # Defining the board class, where a default initial board will be specified
    def __init__(self): # Initializing board
        self.init_x = 0 # Defining initial x value for every call
        self.init_y = 0 # Defining initial y value for every call
        self.Game_grid = [[-1 for _ in range(15)] for _ in range(15)] #Define a 15x15 matrix list of values '-1'
        self.color_dict =  {-1: (0, 0, 0), # The color dictionary which will store all color's in integers for easier manipulation, -1 as (0,0,0) or black
                             0: (255, 255, 255), # 0 as (255,255,255) or white
                             1: (255, 0, 0), 'R': (255, 0, 0), # 1 as (255,0,0) or red
                             2: (0, 255, 0,), 'G': (0, 255, 0,), # 2 as (0, 255, 0) or green
                             3: (0, 0, 255), 'B': (0, 0, 255), # 3 as (0, 0, 255) or blue
                             4: (255, 225, 100), 'Y': (255, 225, 100)} # 4 as (255,255,100) or yellow
        self.color_matrix =[[-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 2, 2, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 2, 2, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 2, 0, -1, -1, -1, -1, -1, -1],
                            [ 0,  1,  0,  0,  0,  0, 1, 0, 2,  0,  0,  0,  4,  0,  0],
                            [ 0,  1,  1,  1,  1,  1, 0, 0, 0,  4,  4,  4,  4,  4,  0],   # Making a visual for the back-end with the specified colors
                            [ 0,  0,  1,  0,  0,  0, 3, 0, 4,  0,  0,  0,  0,  4,  0],
                            [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 3, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 3, 3, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 3, 3, 0, -1, -1, -1, -1, -1, -1],
                            [-1, -1, -1, -1, -1, -1, 0, 0, 0, -1, -1, -1, -1, -1, -1]]
        self.coordinate_matrix = [[[self.init_x + i * 50, self.init_y + j * 50] for i in range(0, 15)] for j in range(0, 15)] # Assigning a coordinate to every location in the grid (times 50)
        '''
        Defining a new list matrix with all positions '0' 
        Then using '1' to specify the safe spots/places
        '''
        self.safe_matrix = [[0 for _ in range(15)] for _ in range(15)] 
        self.safe_matrix[6][1] = 1 
        self.safe_matrix[8][2] = 1
        self.safe_matrix[13][6] = 1
        self.safe_matrix[12][8] = 1
        self.safe_matrix[8][13] = 1
        self.safe_matrix[6][12] = 1
        self.safe_matrix[1][8] = 1
        self.safe_matrix[2][6] = 1
        '''
        Defining the faces of the dice. 
        left being the top, 
        middle being the middle,
        right being the bottom. 
        1 defines a 'dot', while '0' means blank
        '''
        self.faces ={1: [[0, 0, 0], [0, 1, 0], [0, 0, 0]],
                     2: [[0, 1, 0], [0, 0, 0], [0, 1, 0]],
                     3: [[0, 1, 0], [0, 1, 0], [0, 1, 0]],
                     4: [[1, 0, 1], [0, 0, 0], [1, 0, 1]],
                     5: [[1, 0, 1], [0, 1, 0], [1, 0, 1]],
                     6: [[1, 0, 1], [1, 0, 1], [1, 0, 1]],}
        
        global Game_grid # Assigning all the defined objects to the game-grid as objects, storing an object at every location to do their job.
        for i in range(15): # Iterating every 15 steps
            for j in range(15): # Iterating every 15 steps
                self.ob = grid_obj(self.color_dict[self.color_matrix[i][j]], [], self.safe_matrix[i][j], self.coordinate_matrix[i][j]) # Defining an object for the game-grid
                Game_grid[i][j] = self.ob # Assigning it to the Game-grid list as the main object

    # piece_initialization 50 defines initial position, multiplying by where its supposed to be and go
        self.R1 = piece('R1', self.color_dict[1], 0, (50 * 1, 50 * 1), 20) # Red piece one, defining its Id, color, location and radius
        Game_grid[1][1].p_list.append(self.R1) # Assigning the piece in the Game-grid
        self.R2 = piece('R2', self.color_dict[1], 0, (50 * 4, 50 * 1), 20) # Red piece two, defining its Id, color, location and radius
        Game_grid[4][1].p_list.append(self.R2) # Assigning the piece in the Game-grid
        self.R3 = piece('R3', self.color_dict[1], 0, (50 * 1, 50 * 4), 20) # Red piece three, defining its Id, color, location and radius
        Game_grid[1][4].p_list.append(self.R3) # Assigning the piece in the Game-grid
        self.R4 = piece('R4', self.color_dict[1], 0, (50 * 4, 50 * 4), 20) # Red piece four, defining its Id, color, location and radius
        Game_grid[4][4].p_list.append(self.R4) # Assigning the piece in the Game-grid
        self.G1 = piece('G1', self.color_dict[2], 0, (50 * 10, 50 * 1), 20) # Green piece one, defining its Id, color, location and radius
        Game_grid[10][1].p_list.append(self.G1) # Assigning the piece in the Game-grid
        self.G2 = piece('G2', self.color_dict[2], 0, (50 * 13, 50 * 1), 20) # Green piece two, defining its Id, color, location and radius
        Game_grid[13][1].p_list.append(self.G2) # Assigning the piece in the Game-grid
        self.G3 = piece('G3', self.color_dict[2], 0, (50 * 10, 50 * 4), 20) # Green piece three, defining its Id, color, location and radius
        Game_grid[10][4].p_list.append(self.G3) # Assigning the piece in the Game-grid
        self.G4 = piece('G4', self.color_dict[2], 0, (50 * 13, 50 * 4), 20) # Green piece four, defining its Id, color, location and radius
        Game_grid[13][4].p_list.append(self.G4) # Assigning the piece in the Game-grid
        self.B1 = piece('B1', self.color_dict[3], 0, (50 * 1, 50 * 10), 20) # Blue piece one, defining its Id, color, location and radius
        Game_grid[1][10].p_list.append(self.B1) # Assigning the piece in the Game-grid
        self.B2 = piece('B2', self.color_dict[3], 0, (50 * 4, 50 * 10), 20) # Blue piece two, defining its Id, color, location and radius
        Game_grid[4][10].p_list.append(self.B2) # Assigning the piece in the Game-grid
        self.B3 = piece('B3', self.color_dict[3], 0, (50 * 1, 50 * 13), 20) # Blue piece three, defining its Id, color, location and radius
        Game_grid[1][13].p_list.append(self.B3) # Assigning the piece in the Game-grid
        self.B4 = piece('B4', self.color_dict[3], 0, (50 * 4, 50 * 13), 20) # Blue piece four, defining its Id, color, location and radius
        Game_grid[4][13].p_list.append(self.B4) # Assigning the piece in the Game-grid
        self.Y1 = piece('Y1', self.color_dict[4], 0, (50 * 10, 50 * 10), 20) # Yellow piece one, defining its Id, color, location and radius
        Game_grid[10][10].p_list.append(self.Y1) # Assigning the piece in the Game-grid
        self.Y2 = piece('Y2', self.color_dict[4], 0, (50 * 13, 50 * 10), 20) # Yellow piece two, defining its Id, color, location and radius
        Game_grid[13][10].p_list.append(self.Y2) # Assigning the piece in the Game-grid
        self.Y3 = piece('Y3', self.color_dict[4], 0, (50 * 10, 50 * 13), 20) # Yellow piece three, defining its Id, color, location and radius
        Game_grid[10][13].p_list.append(self.Y3) # Assigning the piece in the Game-grid
        self.Y4 = piece('Y4', self.color_dict[4], 0, (50 * 13, 50 * 13), 20) # Yellow piece four, defining its Id, color, location and radius
        Game_grid[13][13].p_list.append(self.Y4) # Assigning the piece in the Game-grid
        self.clist_obj = circularlist() # Making an object for the circular list to use it for movements on every piece
    
    def GetGameGrid(self): # Getter for the game-grid
        return self.Game_grid

board, dice_clicked, dice_value, move_list, n_times , e_list = Board(), False, 6, [], 0, [] # Setting up some variables for the main loop to iterate
'''
Board containing the board object
dice_clicked checking when a dice is being clicked or not (True if yes, False if no)
Initial dice value will be 6, cosmetic display before the start
Defining an empty list which will specify movements throughout the program
'''

class Layout(Board): # Defining the layout class, which imports the main board and then draws it on the window.
    def __init__(self,cha=''): # Initializing the layout
        self.compi = window(cha) # Compositing the window class in a variable
        self.boardd = Board() # Compositing the board class in a varible
        window.__init__(self) # Inheriting all initializing parts from the window class

    def gridlocation(self,pos): # Method for specifying every location on the grid using pos
        x = pos[0] # x-coordinates 
        y = pos[1] # y-coordinates
        return (x // 50, y // 50) # Retuning new positions

    def relativePieceStructure(p_list, x, y): # Checking which ID, check and team is in focus to highlight it
        l = len(p_list) # Length of the imported position list
        relRadius = int((2 / (l + 1)) * 20) # Overlay radius for a piece
        relpoint = [] # Default value for relative point
        j = 0 # Default value for this method (to check)
        if l % 2 == 0:
            l1 = [i + 1 for i in range((l // 2))]
            l2 = [i - 1 for i in range((l // 2))]
            relpoint = l2[::-1] + l1
        else:
            l1 = [i + 1 for i in range((l // 2))]
            l2 = [i - 1 for i in range((l // 2))]
            relpoint = l2[::-1] + [0] + l1
        for p in p_list:
            p.radius = relRadius
            p.coordinates = ((x) + (relpoint[j] * (relRadius // 2)), (y))
            j += 1


    def drawGrid(self): # Method to draw everything after inheriting from previous classes and running an infinite loop to check for user intractions
        newSurface = pygame.display.set_mode((self.HEIGHT,self.WIDTH)) # Setting up a new empty window panel for the surface
        for i in range(15): # Iterating 15 times
            for j in range(15): # Iterating 15 times
                pygame.draw.rect(newSurface, Game_grid[i][j].bg_color, tuple(Game_grid[i][j].coordinate + [50, 50])) # Drawing the game grid using their colors and specified coordinates
                pygame.draw.rect(newSurface, (0, 0, 0), tuple(Game_grid[i][j].coordinate + [50, 50]), 1) # Defining the extra space around the board/dice
                
        '''
        Fixed constant drawing statements that will define the board again on every run
        '''
        pygame.draw.rect(newSurface, self.boardd.color_dict[1], (self.boardd.init_x, self.boardd.init_y, 300, 300))
        pygame.draw.rect(newSurface, self.boardd.color_dict[0], (self.boardd.init_x + 50, self.boardd.init_y + 50, 200, 200))
        pygame.draw.rect(newSurface, self.boardd.color_dict[2], (self.boardd.init_x + 450, self.boardd.init_y, 300, 300))
        pygame.draw.rect(newSurface, self.boardd.color_dict[0], (self.boardd.init_x + 500, self.boardd.init_y + 50, 200, 200))
        pygame.draw.rect(newSurface, self.boardd.color_dict[3], (self.boardd.init_x, self.boardd.init_y + 450, 300, 300))
        pygame.draw.rect(newSurface, self.boardd.color_dict[0], (self.boardd.init_x + 50, self.boardd.init_y + 500, 200, 200))
        pygame.draw.rect(newSurface, self.boardd.color_dict[4], (self.boardd.init_x + 450, self.boardd.init_y + 450, 300, 300))
        pygame.draw.rect(newSurface, self.boardd.color_dict[0], (self.boardd.init_x + 500, self.boardd.init_y + 500, 200, 200))

        for i in range(15): # Iterating 15 times
            for j in range(15): # Iterating 15 times
                Layout.relativePieceStructure(Game_grid[i][j].p_list, i * 50, j * 50) # Checking which team's turn it is and highlighting it using the grid
                for k in Game_grid[i][j].p_list: # Running loop for every element (object) in the game grid and its position
                    c = k.coordinates # Inheriting the coordinates
                    pygame.draw.circle(newSurface, k.color, (c[0] + 25, c[1] + 25), k.radius) # Drawing pieces and their respective colors and radius
                    pygame.draw.circle(newSurface, self.boardd.color_dict[-1], (c[0] + 25, c[1] + 25), k.radius, 1) # Drawing the highlighter for each team when its their turn
                    if k.id[0] == win.GetChance():
                        pygame.draw.circle(newSurface, self.boardd.color_dict[0], (c[0] + 25, c[1] + 25), k.radius - 2, 2) # Removing the highlighter for the previous step so next can continue
        self.face = self.boardd.faces[dice_value] # Inheriting the dice faces to draw them
        for i in range(3): # Iterating three times
            for j in range(3): # Iterating thee times
                pygame.draw.rect(newSurface, self.boardd.color_dict[0], ((0 + 800) + (50 * j), (0 + 300) + (50 * i), 50, 50)) # Drawing the dice
                if self.face[i][j] == 1:
                    pygame.draw.circle(newSurface, self.boardd.color_dict[1], ((0 + 800) + (50 * j) + 25, (0 + 300) + (50 * i) + 25), 10) # Drawing the dice specificly if its value is '1'
        pygame.draw.rect(newSurface, self.boardd.color_dict[win.GetChance()], ((0 + 800), (0 + 300), 150, 150), 4) # Drawing the highlighter around the Dice
        return newSurface # Returining the new drawn surface to the original display window

    def checkCollision(self,p_list): # Checking for collision between two pieces, from any team
        new_list=[] # Defining a new list in case of pieces stacking
        for p in p_list: # Checking for every position in the pos_list
            if p.id[0] == win.GetChance(): # If the ID of the coordinate is the same of the one which turn it is, then
                new_list.append(p) # The pieces will stack on one another in a new list
            else: # Otherwise
                p.coordinates=p.original_coordinate # Matching the coordinates of two different teams on the same spot
                i=p.coordinates[0]//50 # Removing the x-coordinate
                j=p.coordinates[1]//50 # Removing the y-coordinate
                Game_grid[i][j].p_list.append(p) # And then ultimately removing the piece that was killed and updating the game-grid
        return new_list # Returning the stacked or unchanged object for the movement

    def chk_id(self,p_list): # Checking ID for movement defining from the game-grid to program running display on every step on the background
        for i in p_list: # Iterating elements from the position list
            if i.id[0] == win.GetChance(): # If the ID of the position matches the chance of whose turn it is
                return True # return true
        return False # else return false

runner = Layout() # Defining an object for the Layout class

def main(): #Initiating the main function
    pygame.display.set_caption('Ludo') # Setting windows title
    pygame.display.update() # Booting up the windows for the first time with all fixed constants
main() # Calling the main function

'''
File managing
Stores logs for each movement inside log text files
Limit for log files is 5, to be safe from excess memory usage
'''
def checker():
    if os.path.isfile('logs/logs5.txt'):
        logselector = random.randint(1,5)
        with open(f'logs/logs{logselector}.txt','w') as adder:
            adder.writelines('')
        return f'logs/logs{logselector}.txt'
    if os.path.isfile('logs/logs4.txt'):
        with open('logs/logs5.txt','w') as adder:
            adder.writelines('')
        return 'logs/logs5.txt'
    elif os.path.isfile('logs/logs3.txt'):
        with open('logs/logs4.txt','w') as adder:
            adder.writelines('')
        return 'logs/logs4.txt'
    elif os.path.isfile('logs/logs2.txt'):
        with open('logs/logs3.txt','w') as adder:
            adder.writelines('')
        return 'logs/logs3.txt'
    elif os.path.isfile('logs/logs1.txt'):
        with open('logs/logs2.txt','w') as adder:
            adder.writelines('')
        return 'logs/logs2.txt'
    else:
        with open('logs/logs1.txt','w') as adder:
            adder.writelines('')
        return 'logs/logs1.txt'  
file_name = checker()
print('L'+file_name[6:10],'created')
def file_mng(x):
    print(x)
    e_list.append(x)
    to_add = []
    for i in e_list:
        to_add.append(str(i)+'\n')
    with open(file_name,'a') as adder:
        adder.writelines(to_add[-1])
file_mng('Game started\n')

while (True):
        for event in pygame.event.get():

            if event.type == MOUSEBUTTONDOWN:
                loc = runner.gridlocation(event.pos)
                Clicks += 1
                if loc[0] >= 16 and loc[0] <= 18 and loc[1] >= 6 and loc[1] <= 8 and dice_clicked == False:
                    # dice_value = 6
                    dice_value = random.randint(1, 6) # having a random Dice value between 1 to 6
                    if win.GetChance() == 'R': # Red Piece's turn
                        teem = 'Red'
                        tem = 'Green' 
                    elif win.GetChance() == 'G': # Green Piece's turn
                        teem = 'Green'
                        tem = 'Yellow'
                    elif win.GetChance() == 'Y': # Yellow Piece's turn 
                        teem = 'Yellow'
                        tem = 'Blue'
                    elif win.GetChance() == 'B': # Blue Piece's turn
                        teem = 'Blue'
                        tem = 'Red'
                    file_mng("Dice rolled by "+teem+"\nDice number: "+str(dice_value)) # printing dice rolled by which team and the dice value
                    dice_clicked = True #clicked

                if dice_value != 6 and dice_clicked == True:  # if the dice value is not 6
                    flag = 0  
                    for i in board.clist_obj.c_list: 
                        for p in Game_grid[i[0]][i[1]].p_list:
                            if p.id[0] == win.GetChance():
                                ins.SetCondit(teem)
                                flag = 1
                    if flag == 0: #if the dice value is not 6 then it will be next team's turn
                        if win.GetChance() == 'R': #if the current team is red
                            win.SetChance('G') #the next team will be green
                        elif win.GetChance() == 'G': #if the current team is green
                            win.SetChance('Y') #the next team will be yellow
                        elif win.GetChance() == 'Y': #if the current team is Yellow
                            win.SetChance('B') #the next team will be blue
                        elif win.GetChance() == 'B': #if the current team is blue
                            win.SetChance('R') #the next team will be read
                        ins.SetCondit('Dice') #if the dice should be clicked
                        dice_clicked = False #dice is not clicked

                elif dice_value == 6 and dice_clicked == True: #if the dice value is 6
                    n_times += 1
                    file_mng(f'Click on the {teem} piece to continue ({n_times})') #displaying the team name to continue
                    ins.SetCondit(teem) 
                
                if win.GetChance() == 'R' and dice_value == 6 and (loc in [(1, 1), (4, 1), (4, 4), (1, 4)]) and dice_clicked == True: #if the dice value is 6 and its red team's turn and user cicked on the red pieces 
                    file_mng(f'{teem} piece successfully moved out.') #printing red team
                    Game_grid[1][6].p_list.append(Game_grid[loc[0]][loc[1]].p_list[0]) # Assigning the piece in the Game-grid
                    Game_grid[1][6].p_list[-1].coordinates = (50 * 1, 50 * 6) #storing the piece coordinates
                    Game_grid[loc[0]][loc[1]].p_list = [] # Assigning the piece in the Game-grid an emptylist
                    file_mng('Piece ID: '+str(Game_grid[1][6].p_list[-1].id)) #printing the piece ID
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click
                    n_times = 0
                elif win.GetChance() == 'G' and dice_value == 6 and (
                        loc in [(10, 1), (13, 1), (13, 4), (10, 4)]) and dice_clicked == True:  #if the dice value is 6 and its green team's turn and user cicked on the Green pieces 
                    file_mng(f'{teem} piece successfully moved out.')#printing Green team's name
                    Game_grid[8][1].p_list.append(Game_grid[loc[0]][loc[1]].p_list[0]) # Assigning the piece in the Game-grid
                    Game_grid[8][1].p_list[-1].coordinates = (50 * 8, 50 * 1) # Assigning the piece in the Game-grid
                    Game_grid[loc[0]][loc[1]].p_list = []   # Assigning the piece in the Game-grid  an emptylist
                    file_mng('Piece ID: '+str(Game_grid[8][1].p_list[0].id)) #printing the piece ID
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click
                    n_times = 0
                elif win.GetChance() == 'Y' and dice_value == 6 and (
                        loc in [(10, 10), (13, 10), (13, 13), (10, 13)]) and dice_clicked == True:  #if the dice value is 6 and its yellow team's turn and user cicked on the yellow pieces 
                    file_mng(f'{teem} piece successfully moved out.')#printing Yellow team's name
                    Game_grid[13][8].p_list.append(Game_grid[loc[0]][loc[1]].p_list[0])# Assigning the piece in the Game-grid
                    Game_grid[13][8].p_list[-1].coordinates = (50 * 13, 50 * 8) # Assigning the piece in the Game-grid
                    Game_grid[loc[0]][loc[1]].p_list = [] # Assigning the piece in the Game-grid an emptylist
                    file_mng('Piece ID: '+str(Game_grid[13][8].p_list[0].id)) #printing the piece ID
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click
                    n_times = 0
                elif win.GetChance() == 'B' and dice_value == 6 and (
                        loc in [(1, 10), (4, 10), (4, 13), (1, 13)]) and dice_clicked == True: #if the dice value is 6 and its Blue team's turn and user cicked on the blue pieces 
                    file_mng(f'{teem} piece successfully moved out.') #printing Blue team's name
                    Game_grid[6][13].p_list.append(Game_grid[loc[0]][loc[1]].p_list[0])# Assigning the piece in the Game-grid
                    Game_grid[6][13].p_list[-1].coordinates = (50 * 6, 50 * 13) # Assigning the piece in the Game-grid
                    Game_grid[loc[0]][loc[1]].p_list = [] # Assigning the piece in the Game-grid an emptylist
                    file_mng('Piece ID: '+str(Game_grid[6][13].p_list[0].id)) #printing the piece ID
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click
                    n_times = 0
                elif win.GetChance() == 'R' and (loc in [(1, 7), (2, 7), (3, 7), (4, 7), (5, 7)]) and len(
                        Game_grid[loc[0]][loc[1]].p_list) > 0 and dice_clicked == True: #if the piece is unlocked and and the dice is rolled 
                    if loc[0] + dice_value <= (5 + 1): # checking for the movement
                        Game_grid[loc[0] + dice_value][loc[1]].p_list.append(Game_grid[loc[0]][loc[1]].p_list[-1])#checking the current piece location in the game_grid
                        Game_grid[loc[0] + dice_value][loc[1]].p_list[-1].coordinates = (
                        50 * (loc[0] + dice_value), 50 * (loc[1]))#moving the piece according to the dice value
                        Game_grid[loc[0]][loc[1]].p_list = Game_grid[loc[0]][loc[1]].p_list[:-1] #assigning previous loc in p_list
                    ins.SetCondit('Dice')
                    dice_clicked = False #no click

                elif win.GetChance() == 'G' and (loc in [(7, 1), (7, 2), (7, 3), (7, 4), (7, 5)]) and len(
                        Game_grid[loc[0]][loc[1]].p_list) > 0 and dice_clicked == True: #if the piece is unlocked and and the dice is rolled 
                    if loc[1] + dice_value <= (5 + 1):   # checking for the movement
                        Game_grid[loc[0]][loc[1] + dice_value].p_list.append(Game_grid[loc[0]][loc[1]].p_list[-1])#checking the current piece location in the game_grid
                        Game_grid[loc[0]][loc[1] + dice_value].p_list[-1].coordinates = (
                            50 * (loc[0]), 50 * (loc[1] + dice_value))#moving the piece according to the dice value
                        Game_grid[loc[0]][loc[1]].p_list = Game_grid[loc[0]][loc[1]].p_list[:-1] #assigning previous loc in p_list
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click

                elif win.GetChance() == 'Y' and (loc in [(9, 7), (10, 7), (11, 7), (12, 7), (13, 7)]) and len(
                        Game_grid[loc[0]][loc[1]].p_list) > 0 and dice_clicked == True: #if the piece is unlocked and and the dice is rolled and clicked
                    if loc[0] - dice_value >= (9 - 1):  # checking for the movement
                        Game_grid[loc[0] - dice_value][loc[1]].p_list.append(Game_grid[loc[0]][loc[1]].p_list[-1]) #checking the current piece location in the game_grid
                        Game_grid[loc[0] - dice_value][loc[1]].p_list[-1].coordinates = (
                            50 * (loc[0] - dice_value), 50 * (loc[1])) #moving the piece according to the dice value
                        Game_grid[loc[0]][loc[1]].p_list = Game_grid[loc[0]][loc[1]].p_list[:-1] #assigning previous loc in p_list
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click

                elif win.GetChance() == 'B' and (loc in [(7, 9), (7, 10), (7, 11), (7, 12), (7, 13)]) and len(
                        Game_grid[loc[0]][loc[1]].p_list) > 0 and dice_clicked == True:  #if the piece is unlocked and and the dice is rolled 
                    if loc[1] + dice_value >= (9 - 1):  # checking for the movement
                        Game_grid[loc[0]][loc[1] + dice_value].p_list.append(Game_grid[loc[0]][loc[1]].p_list[-1])#checking the current piece location in the game_grid
                        Game_grid[loc[0]][loc[1] + dice_value].p_list[-1].coordinates = (
                            50 * (loc[0]), 50 * (loc[1] + dice_value)) #moving the piece according to the dice value
                        Game_grid[loc[0]][loc[1]].p_list = Game_grid[loc[0]][loc[1]].p_list[:-1] #assigning previous loc in p_list
                    ins.SetCondit('Dice') #setting the condition variable to Dice
                    dice_clicked = False #no click

                elif (board.clist_obj.chk(loc)) and runner.chk_id(Game_grid[loc[0]][loc[1]].p_list) and dice_clicked == True: #if the piece, piece location matches and clicked
                    file_mng(f'{teem} piece successfully moved.\nNext '+tem+"'s turn")
                    newpos = board.clist_obj.move(loc, dice_value, win.GetChance()) #variable for new position 
                    new_list = [] 
                    flg = 0
                    for i in Game_grid[loc[0]][loc[1]].p_list: #for loop to check in the game grid
                        if i.id[0] == win.GetChance() and flg == 0: #checking if no collision is made
                            Game_grid[newpos[0]][newpos[1]].p_list.append(i) # storing the position in game_grid
                            Game_grid[newpos[0]][newpos[1]].p_list[-1].coordinates = (50 * newpos[0], 50 * newpos[1]) # assigning the new position
                            #eating pieces
                            Game_grid[newpos[0]][newpos[1]].p_list=runner.checkCollision(Game_grid[newpos[0]][newpos[1]].p_list) #for colliding with other pieces
                            flg = 1
                        else:
                            new_list.append(i) #if no collision  is made
                    Game_grid[loc[0]][loc[1]].p_list = new_list # assigning gamegrid an empty list
                    dice_clicked = False #no click

                    if dice_value != 6: # if the dice value is not 6
                        if win.GetChance() == 'R': # turn of red team   
                            tem = 'Green' 
                            win.SetChance('G') #setting the next turn for green team
                        elif win.GetChance() == 'G': # turn of green team 
                            tem = 'Yellow'
                            win.SetChance('Y')# setting the next turn for yellow team 
                        elif win.GetChance() == 'Y': # turn of yellow team 
                            tem = 'Blue'
                            win.SetChance('B') # setting the next turn for Blue team
                        elif win.GetChance() == 'B': # turn of Blue team 
                            tem = 'Red'
                            win.SetChance('R') # setting the next turn for red team
                        ins.SetCondit('Dice')  #setting the condition variable to Dice
            win.maindisplay.blit(runner.drawGrid(), (0, 0)) #initiating the game grid
            ins.textdisp() #function to display instructions
            pygame.display.update() #updating each move and text on dislplay
            

            if event.type == QUIT: #to quit game
                file_mng('\nGame exited.')
                pygame.quit()
                sys.exit()
        
        pygame.display.update() #updating each move and text on dislplay