"""
COMP 1300 - Semester Project
Sort It!: A Ball Sorting Game

A puzzle game where the player sorts colored balls into tubes so that 
each tube contains one color only. 

This game contains 10 levels of increasing difficulty
"""
import Draw
import copy
import time

## GLOBAL VARIABLES FOR THE GAME ##

# each level is a 2d list where each list is a tube
# containing different colored balls 
# balls are stored from bottom to top so last element in list is the top ball

PUZZLES = [     

    # level 1
    [["R", "Y", "R", "Y"],
     ["Y", "R", "Y", "R"],
     []],

    # level 2    
    [["R", "Y", "O", "R"],
     ["Y", "Y", "O", "R"],
     ["O", "R", "Y", "O"],
     [],
     []],    
    
    # level 3    
    [["O", "Y", "R", "R"],
     ["R", "O", "Y", "R"],
     ["O", "Y", "O", "Y"],
     [],
     []],
    
    # level 4   
    [["G", "Y", "V", "V"],
     ["B", "O", "Y", "O"],
     ["Y", "G", "B", "V"],
     ["Y", "B", "O", "V"],
     ["G", "G", "O", "B"],     
     [],
     []],
    
    # level 5  
    [["V", "Y", "V", "G"],
     ["Y", "B", "B", "Y"],
     ["B", "V", "G", "V"],
     ["G", "V", "V", "B"],
     ["G", "V", "V", "Y"],     
     [],
     []],
     
    # level 6 
    [["Y", "Y", "B", "B"],
     ["R", "R", "G", "G"],
     ["R", "V", "O", "Y"],
     ["B", "B", "O", "G"],
     ["V", "V", "O", "R"],
     ["V", "O", "Y", "G"],     
     [],
     []],

    # level 7 
    [["B", "O", "Y", "O"],
     ["G", "G", "Y", "Y"],
     ["O", "G", "V", "G"],
     ["R", "O", "V", "Y"],
     ["B", "R", "R", "R"],
     ["V", "V", "B", "B"],     
     [],
     []],

    # level 8
    [["R", "B", "R", "O"],
     ["B", "B", "M", "O"],
     ["Y", "Y", "M", "Y"],
     ["O", "G", "B", "Y"],
     ["R", "O", "G", "M"],
     ["M", "R", "G", "G"],     
     [],
     []], 
    
    # level 9
    [["R", "B", "V", "O"],
     ["Y", "V", "V", "G"],
     ["B", "M", "Y", "O"],
     ["V", "O", "R", "G"],
     ["G", "B", "M", "G"],
     ["B", "Y", "R", "M"],
     ["M", "O", "R", "Y"],
     [],
     []],         

    # level 10
    
    [["R", "Dr", "V", "O"],
     ["Y", "G", "M", "B"],
     ["Dr", "B", "R", "M"],
     ["O", "Y", "V", "G"],
     ["M", "Dr", "Y", "R"],
     ["B", "O", "G", "V"],
     ["V", "M", "B", "Y"],
     ["G", "R", "O", "Dr"],
     [],
     []],       
    ]

   
# dictionary of all the colors used in the game to corresponding Draw colors
# 'red', 'orange', 'yellow', 'green', 'blue', 'violet', 'magenta', 'dark red'
COLORS = {"R":Draw.RED, "O":Draw.color(255, 130, 30), "Y":Draw.YELLOW, 
          "G":Draw.GREEN, "B":Draw.CYAN, "V":Draw.VIOLET, "M":Draw.MAGENTA, 
          "Dr":Draw.DARK_RED}    

# fixed dimensions and placements of the tubes
TUBE_WIDTH    = 50   # width of each tube in pixels. this width = gap between tubes
TUBE_BOTTOM   = 525  # y coordinate of the bottom of all tubes
TUBE_TOP      = 300  # y coordinate of the top of all tubes
CANVAS_WIDTH  = 1000 # width of canvas in pixels
CANVAS_LENGTH = 750  # length of canvas in pixels

# --------------------------------------------------------------------------- #

def drawBoard (puzzle, clicks, levelNum, leftMargin, startTime):
    """
    This function draws the entire game screen for one given frame. 
    It calls the sub-functions to display the: decorations, level, timer, 
    UNDO/RESTART buttons, tubes, and balls.
    """
    Draw.clear()
    
    # time that elapsed since the beginning of level
    # rounded (int) for clean display and clear formatting
    currentTime = int(time.time() - startTime)
        
    # set the background
    Draw.setBackground(Draw.BLACK)
    
    # decorations
    drawDecorativeBalls()
    
    # display the current level
    displayCurrentLevel(levelNum)
    Draw.setFontBold(True)
    
    # display time elapsed since beginning of level
    Draw.setColor(Draw.WHITE)
    Draw.setFontFamily("Caecilia LT Std")
    Draw.setFontSize(45)    
    # :02d makes the seconds always display as two digits (0:05 and not 0:5)    
    Draw.string(f"Time: {currentTime // 60}:{currentTime % 60:02d}", 25, 675)
    
    # display 'UNDO' button (with blue background)
    Draw.setColor(Draw.CYAN)                   
    Draw.filledRect(525, 665, 160, 60) 
    Draw.setColor(Draw.WHITE)                   
    Draw.filledRect(530, 670, 150, 50)
    Draw.setColor(Draw.BLACK)               
    Draw.string("UNDO", 535, 668)
    
    # display 'RESTART' button (with magenta background)
    Draw.setColor(Draw.MAGENTA)    
    Draw.filledRect(725, 665, 250, 60)
    Draw.setColor(Draw.WHITE)    
    Draw.filledRect(730, 670, 240, 50)    
    Draw.setColor(Draw.BLACK)               
    Draw.string("RESTART", 746, 668)    
    
    # draw the tubes for the balls
    drawTubes(len(puzzle), leftMargin)
    drawBalls(puzzle, leftMargin, clicks) 
    
    Draw.show()
    
# --------------------------------------------------------------------------- #
## sub-functions of drawBoard that handle animations for the game ##  

def drawDecorativeBalls():
    """
    This function is called by drawBoard and draws small colored balls on both
    sides of 'current level'
    """
    
    # list to index through colors of the balls
    ballColors = ["R", "O", "Y", "G", "B", "M"]
    
    # balls on the left side of 'current level' (starts at x=90)
    for i in range(3):
        Draw.setColor(COLORS[ballColors[i]])
        Draw.filledOval(90 + (i*75), 125, 30, 30)
    
    # balls on the right side of 'current level' (starts at x=725)
    for i in range(3):
        Draw.setColor(COLORS[ballColors[i+3]])
        Draw.filledOval(725 + (i*75), 125, 30, 30)    

def displayCurrentLevel(levelNum):
    """
    This function is called by drawBoard and displays the current level 
    """
    
    Draw.setFontSize(110)
    Draw.setFontFamily("Arial")
    Draw.setColor(Draw.WHITE)
    Draw.setFontBold(True)
    
    # set the x and y coordinates of the string 'current level'
    # numbers are chosen so that the text is centered
    x = 317
    y = 75      
    
    if levelNum == 10:          
        # the double digit of 10 makes the string offcenter
        x -= 35 
    Draw.string(f"Level {levelNum}", x, y)
    
       
def drawTubes(tubes, leftMargin):
    """
    This function draws the empty tube outlines for the current level.
    The position of the tubes depends on how many tubes the current level has
    as the tubes are centered horizontally
    """
    for tube in range(tubes):

        # coordinates of the tube (to center the tubes horizontally)
        x = leftMargin + (tube * (TUBE_WIDTH*2))
        y = TUBE_TOP
        
        # black background to block out the background 
        Draw.setColor(Draw.BLACK)
        Draw.filledRect(x-1, y-1, TUBE_WIDTH+2, 224)
       
        # white frame of the tube
        Draw.setColor(Draw.WHITE)
        Draw.rect(x, y, TUBE_WIDTH+2, 225)
        
def drawBalls(puzzle, leftMargin, clicks): 
    """
    This function draws all the balls currently inside each tube. 
    If the tube has been clicked on, the top ball is drawn higher to 
    show it has been selected
    """

    for tube in range(len(puzzle)):
        for ball in range(len(puzzle[tube])):
            
            # x and y coordinates of the balls (based on the placement of the tubes)
            x = leftMargin + (TUBE_WIDTH * (tube*2))
            y = TUBE_BOTTOM - ((ball+1)*50)
            
            # render the last ball of the tube that was clicked on higher
            if len(clicks) > 0 and tube == clicks[0] and ball == len(puzzle[tube]) - 1:
                y -= 80
                
            # retrieve the correct color for the corresponding ball              
            Draw.setColor(COLORS[puzzle[tube][ball]])
            Draw.filledOval(x+2, y, 48, 48)
# --------------------------------------------------------------------------- #   
## the following functions deal with the user interactions (sub-functions of playgame) ##

def getTubeNumber(x, y, puzzle, leftMargin):
    """
    This function converts a mouse click (x, y) to a tube index.
    It returns the tube number clicked on or -1 if no valid tube was clicked
    """
    # invalid click if above or below the tubes
    if y < TUBE_TOP or y > TUBE_BOTTOM: return -1
 
    # how far the click is from the start of the first tube on the board
    relativeX = x - leftMargin
      
    # divide by tubewidth to find which column (tube-width segmant) was clicked 
    # (each column is one tube wide)
    # (its an int to get a clean index number)
    tubeNumber = int(relativeX / TUBE_WIDTH)
    
    if tubeNumber >= len(puzzle)*2: return -1 # tube is to the right of all tubes
    if tubeNumber % 2 == 1:         return -1 # click is between the tubes
    if tubeNumber < 0:              return -1 # click is to the left of all tubes
       
    # divide by 2 to convert column number to tube index
    # (every other column is a gap. so tube 0 is column 0, tube 1 is column 2 etc.)    
    return tubeNumber // 2

def validClicks(clicks, puzzle):
    """
    This function checks whether the user's clicks were a valid move.
    A move is valid if: the top balls of the two tubes are the same color,
    or if the to-tube is empty. 
    move is invalid if either the from-tube is empty (no balls to move),
    or the to-tube is full (no room to move the ball),
    or the player clicked the same tube twice
    
    Returns True if the move is valid, otherwise returns False
    """

    # clicks[0] is the from-tube
    # clicks[1] is the to-tube
    
    # from-tube can't be empty and to-tube can't be full
    if len(puzzle[clicks[0]]) == 0 or len(puzzle[clicks[1]]) == 4:
        return False
    
    # to-tube is empty 
    if len(puzzle[clicks[1]]) == 0: return True
    
    # clicked on the same tube twice
    if clicks[0] == clicks[1]: return False
    
    # colors of balls must match 
    if puzzle[clicks[0]][-1] == puzzle[clicks[1]][-1]: return True
    
    return False

def transferBall(clicks, puzzle):
    """
    This function translates the clicks and adjusts the lists accordingly.
    It moves the top ball from the first clicked tube to the second
    """
    
    # remove top ball from the first clicked tube
    lastBall = puzzle[clicks[0]].pop(-1)
    
    # append to the second clicked tube
    puzzle[clicks[1]].append(lastBall)
    
def gameOver(puzzle):
    """
    This function determines if the level is complete.
    The game is over if all the tubes are either empty or contains 
    4 of the same colored balls
   
    Returns True if level is complete, otherwise returns False
    """
        
    for tube in range(len(puzzle)):
        # must be an empty or full tube
        if len(puzzle[tube]) != 0 and len(puzzle[tube]) != 4: return False
        
        # check that every ball in the tube matches the one below it 
        # (# starts index at 1 so each ball can be compared to the one below it)
        for ball in range(1, len(puzzle[tube]), 1):
            if puzzle[tube][ball] != puzzle[tube][ball-1]:
                return False
            
    return True
# --------------------------------------------------------------------------- # 
## functions that display the messages for before and end of the game ##
def beginGame():
    """
    This function displays a welcome message at the beginning of the game with 
    a title, instructions and START button. Once player clicks START, 
    it returns True to begin the game
    """
    while True:
        
        if Draw.mousePressed():
            
            # retrieve the x,y of the click
            x = Draw.mouseX()
            y = Draw.mouseY()
            
            # check if clicked the START button
            if x >= 400 and x<= 600 and y >= 640 and y <= 710:
                return True
        
        Draw.clear()
        Draw.setBackground(Draw.BLACK)
        
        # colors of balls on the top of the welcome display
        ballColors = ["R", "O", "Y", "G", "B", "M"]
        
        # balls at the top
        for x in range(0, 450, 75):
            # x//75 converts x into a balls list index (0, 1, 2...)
            Draw.setColor(COLORS[ballColors[x//75]])                    
            Draw.filledOval(287.5 + x, 75, 50, 50)
        
        # title of the game
        Draw.setFontFamily("Arial")       
        Draw.setFontSize(70)
        Draw.setFontBold(True)
        Draw.setColor(Draw.WHITE)
        Draw.string("Sort It!", 387.5, 130)
        
        Draw.setFontFamily("Caecilia LT Std")                
        Draw.setFontSize(25)    
        Draw.setFontBold(False)
        Draw.string("The colorful ball sorting puzzle", 315, 215)    
        
        Draw.line(450, 265, 550, 265)
        
        Draw.setFontSize(50)
        Draw.string("How to Play", 355, 290)
        
        # create four insruction boxes arranged in a 2x2 grid 
        # (colored background with white box on top) 
        i = 0 # tracker for ballColors indices        
        for x in range(50, 950, 475):
            for y in range(385, 600, 125):
                # colored background
                Draw.setColor(COLORS[ballColors[i]])            
                Draw.filledRect(x, y, 425, 100)
               
                # white box
                Draw.setColor(Draw.WHITE)
                Draw.filledRect(x+5, y+5, 415, 90)
                
                Draw.setFontSize(30)            
                Draw.setColor(Draw.BLACK)            
                Draw.string(f" Step {i+1}:", x+10, y+30)
                i += 1
        
        Draw.setFontSize(15) 
        
        # instructions (\n to format the words so they fit in the appropriate boxes)
        Draw.string("Select a tube to pick up the top ball \nin that tube", 180, 415)
        Draw.string("Tap another tube to move the ball. \nYou may only stack a ball on its \nmatching color or in an empty tube", 177, 530)  
        Draw.string("Sort all the tubes. To complete the \nlevel, each tube must contain four \nballs of the same color", 655, 407) 
        
        Draw.string("Each level increases in diffuclty. \nComplete all 10 level to win the \ngame! Good Luck! ", 655, 530)
        
        # START button box and background
        Draw.setColor(Draw.CYAN)
        Draw.filledRect(400, 640, 200, 70)
        Draw.setColor(Draw.WHITE)
        Draw.filledRect(405, 645, 190, 60)    
        
        # word 'START'
        Draw.setColor(Draw.BLACK)
        Draw.setFontBold(True)
        Draw.setFontSize(50)
        Draw.string("START", 415, 645)
        
        Draw.show()

def endOfLevelDisplay(currentLevel):
    """
    This function displays a congrats message when a level is completed
    It shows the completed level number and pauses for 3 seconds
    before letting the next level begin
    (message is on a white box with a yellow 'frame')
    """
    
    Draw.setColor(Draw.YELLOW)
    Draw.filledRect(125, 75, 750, 500)
    Draw.setColor(Draw.WHITE)    
    Draw.filledRect(135, 85, 730, 480)
    Draw.setFontFamily("Caecilia LT Std")            
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(100)
    
    Draw.string("GREAT JOB!", 200, 150)    
    Draw.string(f"Level {currentLevel}", 335, 300)
    Draw.string("is complete", 225, 400)
    
    Draw.show()
    time.sleep(3)

def endOfGameDisplay():
    """
    This function displays a final congrats message when all levels are complete
    It pauses for 5 seconds before the program ends
    (message is on a white box with green 'frame')
    """
        
    Draw.setFontFamily("Caecilia LT Std")        
    Draw.setColor(Draw.GREEN)
    Draw.filledRect(125, 75, 750, 500)
    Draw.setColor(Draw.WHITE)    
    Draw.filledRect(135, 85, 730, 480)
    Draw.setColor(Draw.BLACK)
    Draw.setFontSize(90)
    
    Draw.string("CONGRATS!", 235, 150)    
    Draw.string("You completed", 165, 300)
    Draw.string("all the levels", 215, 400)
    
    Draw.show()
    time.sleep(5)

# --------------------------------------------------------------------------- #
def playGame(puzzle, level):
    """
    This function runs the loop for one level at a time. It handles the 
    mouse clicking for selecting tubes, undoing moves, and restarting the level
    
    note: undo button only undoes the most recent move.
    
    Function returns True when the level is complete, and False if the user clicked restart
    """
    clicks = [ ]
    lastClicks = [ ]
    
    # adjust margin to center the board horizontally based on number of tubes the level has
    leftMargin = (CANVAS_WIDTH - (((len(puzzle) * 2) - 1) * TUBE_WIDTH)) / 2            
        
    # get start time
    startTime = time.time()

    while not gameOver(puzzle):
        if Draw.mousePressed():
            
            # retrieve the (x,y) of the click
            x = Draw.mouseX()
            y = Draw.mouseY()

         
            # check if the mouse clicked on a tube
            tubeNumber = getTubeNumber(x, y, puzzle, leftMargin)
            if tubeNumber != - 1:
                clicks.append(tubeNumber) 
                
            # each game play only uses 2 clicks:
            # the tube to take the ball from and the tube to deposit the ball 
            # (from-tube and to-tube) 
            if len(clicks) == 2:
                if validClicks(clicks, puzzle):
                    transferBall(clicks, puzzle)

                    # store clicks so can undo if necessary    
                    lastClicks = copy.deepcopy(clicks)    
                clicks = [ ]
        
      
            # check if clicked on the UNDO button (based on x,y of UNDO button)
            if x >= 525 and x <= 675 and y >= 675 and y <= 725:
                
                # reset clicks if only one tube was clicked on (no move made yet)
                if len(clicks) == 1: 
                    clicks = [ ] 
                
                # otherwise reverse last move
                elif len(lastClicks) > 0: 
                    lastClicks.reverse() # swap from and to-tubes to reverse move
                    transferBall(lastClicks, puzzle) # transfer the balls back i.e undo the move
                
                lastClicks = [ ]
            
        
            # if clicked RESTART, return False to tell main() to 
            # restart the current level from the beginning:
            if x >= 725 and x <= 975 and y >= 675 and y<= 725:
                return False        
        drawBoard(puzzle, clicks, level, leftMargin, startTime)
    
  
    # return True to indicate that level is complete
    return True

# --------------------------------------------------------------------------- #
def main():
    """
    This function sets up the canvas, shows the welcome display, 
    and loops through all the levels in order. It also displays the end of level 
    message after each level and end of game message when the game is completed
    """

    Draw.setCanvasSize(CANVAS_WIDTH, CANVAS_LENGTH)
    Draw.show() # prevent the game from animating when it begins
    
    beginGame()   

    for level in range(len(PUZZLES)):
        
        # make a copy of puzzle[level] so its possible to restart a level if necessary 
        # meaning the original puzzle isn't modified
        while not playGame( copy.deepcopy(PUZZLES[level]), level+1 ):  
            # (level+1 bcause level begins at 0)
            pass
        
        
        # display end of game message when all levels are completed
        if level != len(PUZZLES) - 1:
            endOfLevelDisplay((level + 1)) # +1 bcause level begins at 0
            
            
        else: endOfGameDisplay()
            
                    

main()