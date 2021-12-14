import pygame
from pygame.locals import *
import sys
from copy import deepcopy
import random
import time
import sudoku


pygame.init()

WIDTH = 900
HEIGHT = 600
CELL_SIZE = 50

BLACK = (  0,  0,  0)
GREY = (127,127,127)
WHITE = (255,255,255)
LIGHT_BLUE = (150,150,255)
PALE_BLUE = (225,225,255)
BLUE = (0,0,255)
LILAC = (200,162,200)
NAVY = (50,50,150)
RED = (255,0,0)
PALE_RED = (255,225,225)
LIGHT_RED = (255,200,200)


display = pygame.display.set_mode((WIDTH,HEIGHT))
pygame.display.set_caption("Sudoku")

eraser = pygame.image.load('eraser.png')
eraser = pygame.transform.scale(eraser,(40,40))

pencilIcon = pygame.image.load('pencil.jpg')
pencilIcon = pygame.transform.scale(pencilIcon,(40,40))

undoIcon = pygame.image.load('undo.png')
undoIcon = pygame.transform.scale(undoIcon,(40,40))

redoIcon = pygame.transform.flip(undoIcon,True,False)

exitIcon = pygame.image.load('exit.png')
exitIcon = pygame.transform.scale(exitIcon,(40,40))

gameEnd = False

class Moves:
    def __init__(self):
        self.moves = []
        #a move consists of [(column,row),old value,new value]
        self.pointer = -1
    def add_move(self,move):
        if self.pointer < len(self.moves)-1:
            self.moves[self.pointer+1] = move
            while self.pointer+1 < len(self.moves)-1:#delete moves after new move
                self.moves.pop()
        else:
            self.moves.append(move)
        self.pointer += 1
    def top(self):
        if self.pointer<0:
            return None
        move = self.moves[self.pointer]
        return move
    def undo(self):
        if self.pointer > -1:
            move = self.top()
            row = move[0][1]
            col = move[0][0]
            num = move[1]
            sudoku.bcopy.add_val(row,col,num)
            self.pointer -= 1
    def redo(self):
        if self.pointer+1 < len(self.moves):
            self.pointer += 1
            move = self.top()
            row = move[0][1]
            col = move[0][0]
            num = move[2]
            sudoku.bcopy.add_val(row,col,num)
            

def setDifficulty(clicked,d):
    #the difficulties so far are: easy(7), medium(11), hard(15)
    #they are part of a gradient from 1 to 20
    difficulties = {'easy':7,
                    'medium':11,
                    'hard':15}
    
    words = list(difficulties)
    #draw a dropdown menu at position (400,275) with dimensions (100,30)
    current = d.draw(words,400,275,100,30,clicked)
    difficulty = difficulties[current]
    return difficulty
    
            
class dropDown:
    def __init__(self,current,text,box,box_hover):
        self.selected = False
        self.msg = current
        self.text = text
        self.box = box
        self.box_hover = box_hover
    def draw(self,words,x,y,w,h,clicked):
        #font should be: 20
        #base position: (300,300)
        #dimensions: (100,30)
        #colours: black,white,black,pale blue
        pygame.draw.rect(display,BLACK,(x-2,y-2,w+4,h+4))
        pressed = button(self.msg,20,x,y,w,h,self.text,self.box,None,self.box_hover,clicked)
        if pressed:
            self.selected = not(self.selected)
        if self.selected:
            for i in range(len(words)):
                diff_chosen = button(words[i],20,x,y+(i+1)*h,w,h,self.text,self.box,None,self.box_hover,clicked)
                if diff_chosen:
                    self.msg = words[i]
                    self.selected = False
        return self.msg
            

def menu():
    start = True
    clicked = False
    
    d = dropDown('easy',BLACK,WHITE,PALE_BLUE)
    while start:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                pygame.time.wait(175)
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
                

        font = pygame.font.SysFont('calibri',100)
        title = font.render("SUDOKU",True,(LIGHT_BLUE))
        title_rect = title.get_rect(center=(WIDTH/2, HEIGHT/3))
        display.fill(WHITE)
        display.blit(title,title_rect)
        
        #d.draw(['easy','medium'],400,300,100,30,clicked)
        sudoku.difficulty = setDifficulty(clicked,d)
        start_pressed = button('START',75,300,400,300,100,LILAC,PALE_BLUE,PALE_BLUE,LILAC,clicked) 
        if start_pressed:
            start = False
        pygame.display.update()
    #clock.tick(30)



def button(msg,fontSize,x,y,w,h,col1,col2,col3 = None,col4 = None,clicked = False):
    #col1 is the colour of the text when the mouse is not on the box
    #col2 is the colour of the box when the mouse is not on it
    #col3 is the colour of the text when the mouse is on the box
    #col4 is the colour of the box when the mouse is on it
    
    if col3 == None:
        col3 = col1
    if col4 == None:
        col4 = col2

    mouse = pygame.mouse.get_pos()
    font = pygame.font.SysFont('calibri',fontSize)
    pressed = 0
    if x+w > mouse[0] > x and y+h > mouse[1] > y:
        pygame.draw.rect(display, col4,(x,y,w,h))
        colour = col3

        if clicked:
            pressed = 1
    else:
        pygame.draw.rect(display,col2,(x,y,w,h))
        colour = col1
    text = font.render(msg,True,(colour))
    text_rect = text.get_rect(center=(x+(w/2),y+(h/2)))
    display.blit(text,text_rect)
    return pressed


##
def cellButton(num,xpos,ypos,x,y,selectedCell,textColour,boxColour,hover,clicked):
    row = (xpos-50)//CELL_SIZE
    col = (ypos-50)//CELL_SIZE
    pressed = button(num,28,xpos,ypos,CELL_SIZE,CELL_SIZE,textColour,boxColour,None,hover,clicked)
    if pressed:
        if sudoku.newcopy.rows[col][row] == ' ':
            selectedCell = (row, col)
    return selectedCell,pressed

def selectBox(x,y):
    return (x,y)
    
def drawBox(x,y,xgap,ygap,num,selectedCell,clicked,selectedNum):
    font = pygame.font.SysFont('calibri',15)
    noteNums = sudoku.notes.rows[y][x]
    textColour = BLACK
    boxColour = WHITE
    hover = PALE_BLUE
    if num != sudoku.poss.rows[y][x] and num != ' ':
            textColour = RED
            boxColour = PALE_RED
            hover = LIGHT_RED
    else:
        if sudoku.newcopy.rows[y][x] != sudoku.bcopy.rows[y][x]:
            textColour = BLUE
        if selectedCell == None:
            if selectedNum == num and selectedNum != ' ':
                boxColour = PALE_BLUE
        elif selectedCell != None and selectedNum == None:
            if selectedCell[0] == x and selectedCell[1] == y:
                boxColour = LIGHT_BLUE
                hover = LIGHT_BLUE
            else:
                if selectedCell[0] == x or selectedCell[1] == y:
                    boxColour = PALE_BLUE
                if selectedCell[0] // 3 == x // 3 and selectedCell[1]//3 == y//3:
                    boxColour = PALE_BLUE
    xpos = 50+CELL_SIZE*x
    ypos = 50+CELL_SIZE*y
    pygame.draw.rect(display,BLACK,(xpos-xgap,ypos-ygap,CELL_SIZE+3*xgap,CELL_SIZE+3*ygap))
    pygame.draw.rect(display,WHITE,(xpos,ypos,CELL_SIZE,CELL_SIZE))
    selectedCell,pressed = cellButton(num,xpos,ypos,x,y,selectedCell,textColour,boxColour,hover,clicked)
    if num == ' ':
        for mr in range(3):
            for mc in range(3):
                cell = 3*mc+mr
                text = font.render(noteNums[cell],True,GREY)
                text_rect = text.get_rect(center=(xpos+(CELL_SIZE*(mr+1))//4,ypos+(CELL_SIZE*(mc+1))//4))
                display.blit(text,text_rect)
    return selectedCell,pressed
    
def numButton(val,x,y,selectedNum,clicked):
    colour = LIGHT_BLUE
    pressed = 0
    if val == selectedNum:
        colour = NAVY
    pressed = button(val,30,x,y,70,70,WHITE,colour,WHITE,NAVY,clicked)
    if pressed == 1:
        if val == selectedNum:
            selectedNum = None
        else:
            selectedNum = val
            
    return selectedNum,pressed

def eraserButton(x,y,selectedNum,clicked):
    colour = WHITE
    if selectedNum == ' ':
        colour = BLUE
    pressed = 0
    pressed = general_button(x,y,colour,BLUE,clicked)
    if pressed == 1:
        selectedNum = ' '
    display.blit(eraser,(x,y))
    return selectedNum,pressed

def pencilButton(x,y,pencil,clicked):
    colour = WHITE
    pressed = 0
    if pencil:
        colour = BLUE
    pressed = general_button(x,y,colour,BLUE,clicked)
    if pressed == 1:
        print(not(pencil))
        pencil = not(pencil)
    display.blit(pencilIcon,(x,y))
    return pencil,pressed

def undoButton(x,y,moves,clicked):
    pressed = 0
    pressed = general_button(x,y,WHITE,BLUE,clicked)
    if pressed:
        moves.undo()
    display.blit(undoIcon,(x,y))
    return pressed

def redoButton(x,y,moves,clicked):
    pressed = 0
    pressed = general_button(x,y,WHITE,BLUE,clicked)
    if pressed:
        pressed = 1
        moves.redo()
    display.blit(redoIcon,(x,y))
    return pressed

def exitButton(x,y,clicked):
    pressed = 0
    pressed = general_button(x,y,WHITE,RED,clicked)
    if pressed:
        pressed = 1
    display.blit(exitIcon,(x,y))
    return pressed

def general_button(x,y,selected,hover,clicked):
    pressed = button(' ',30,x-1,y-1,42,42,WHITE,selected,None,hover,clicked)
    return pressed

def loading():
    font = pygame.font.SysFont('calibri',30)
    display.fill(WHITE)
    ctr = 0
    sudoku.poss,sudoku.blanked,sudoku.bcopy = sudoku.create_grid()
    while not sudoku.blanked.check():
        display.fill(WHITE)
        ellipsis = '{dots}'
        c = (ctr//25)%4
        d = ellipsis.format(dots='.'*c).ljust(3)
        #print(c)
        text = font.render('Loading'+d,True,PALE_BLUE)
        text_rect = text.get_rect(center=(WIDTH/2,HEIGHT*(5/6)))
        ctr += 1
        sudoku.blanked = sudoku.solvable(sudoku.poss)
        sudoku.bcopy = deepcopy(sudoku.blanked)
        display.blit(text, text_rect)
        pygame.display.update()
        
    sudoku.newcopy = deepcopy(sudoku.bcopy)
    

def main():
    main = True
    clicked = False
    #mode 0: nothing
    #mode 1: cell then value
    #mode 2: value then cell
    mode = 0
    selectedCell = None
    selectedNum = None
    pencil = False
    moves = Moves()
    numsPressed = [0 for i in range(9)]
    cellsPressed = [0 for i in range(81)]
    while main:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                clicked = True
                pygame.time.wait(300)
            if event.type == pygame.MOUSEBUTTONUP:
                clicked = False
        display.fill(WHITE)
        exitPressed = exitButton(800,50,clicked)
        selectedNum,eraserPressed = eraserButton(575,175,selectedNum,clicked)
        pencil,pencilPressed = pencilButton(635,175,pencil,clicked)
        undoPressed = undoButton(695,175,moves,clicked)
        redoPressed = redoButton(755,175,moves,clicked)
        
        

        for r in range(3):
            for c in range(3):
                selectedNum,numsPressed[(r%3)+3*c] = numButton(str((r%3+1)+3*c),575+85*r,250+85*c,selectedNum, clicked)
        numPressed = max(numsPressed)
        for x in range(9):
            xgap = 1
            if x % 3 == 0:
                xgap = 2
            for y in range(9):
                ygap = 1
                if y % 3 == 0:
                    ygap = 2
                num = sudoku.bcopy.rows[y][x]
                selectedCell,cellsPressed[(x%9)+9*y] = drawBox(x,y,xgap,ygap,num,selectedCell,clicked,selectedNum)
        cellPressed = max(cellsPressed)
        pressed = max(redoPressed,eraserPressed,pencilPressed,numPressed,cellPressed,undoPressed)
            
        if mode == 0:
            if selectedCell != None and selectedNum == None:
                mode = 1
            if selectedNum != None and selectedCell == None:
                mode = 2
        elif pressed == 0 and clicked:
            mode = 0
            selectedNum = None
            selectedCell = None
        elif selectedCell != None and selectedNum != None and clicked == 0:
            row = selectedCell[1]
            col = selectedCell[0]
            val = selectedNum
            if selectedNum != ' ':
                index = int(selectedNum) - 1
            if (sudoku.bcopy.rows[row][col] == selectedNum and not pencil) or (sudoku.notes.rows[row][col][index] == selectedNum and pencil):
                val = ' '
            if pencil and sudoku.bcopy.rows[row][col] == ' ':
                sudoku.notes.add_val(row,col,val,index)
            if not pencil:
                v = sudoku.bcopy.rows[row][col]
                sudoku.bcopy.add_val(row,col,val)
                sudoku.notes.rows[row][col] = [' ' for i in range(9)]
                moves.add_move([selectedCell,v,val])
            if mode == 1:
                selectedNum = None
                selectedCell = None
                mode = 0
            if mode == 2:
                selectedCell = None
        if sudoku.bcopy.rows == sudoku.poss.rows or exitPressed:
            main = False
        
        pygame.display.update()
        
while not gameEnd:
    for event in pygame.event.get():
        if event.type == QUIT:
            gameEnd = True
            pygame.quit()
            sys.exit()

    menu()
    loading()
    main()
    pygame.display.flip()

menu()


