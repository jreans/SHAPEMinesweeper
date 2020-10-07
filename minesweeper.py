"""
Ebow and Jeannie
July 2017 
SHAPE CS Session 1
"""
from tkinter import *
from tkinter import simpledialog
import random
import math

####################################
# Helper Functions
####################################

def getCellBounds(row, col, data):
    # aka "Model to View"
    # returns (x0, y0, x1, y1) corners/bounding box of given cell in grid
    gridWidth  = data.width - 2*data.margin
    gridHeight = data.height - 2*data.margin
    x0 = data.margin + gridWidth * col / data.cols
    x1 = data.margin + gridWidth * (col+1) / data.cols
    y0 = data.margin + gridHeight * row / data.rows
    y1 = data.margin + gridHeight * (row+1) / data.rows
    return (x0, y0, x1, y1)


def withInCell(x,y,data):
    row=int(x/50)
    col=int(y/50)
    # aka "View to Model"
    # given x,y coordinates and game data, calculates and returns (row, col)
    # of the cell that the coordinates are within
    return (row,col)

####################################
# Model
####################################

def init(data):
    data.rows=10
    data.cols=10
    data.margin=20
    data.time=0
    data.timerDelay=1000
    data.gameOver=False
    data.paused=False
    data.win=False
    data.info=[[None for x in range(data.rows)] for y in range (data.cols)]
    data.minesleft=0
    data.flagged=[[False for x in range(data.rows)] for y in range (data.cols)]
    buryMines(data)
    data.leaderboard=[]
    data.sortedleader=[]
    data.windowbool=False

    # set initial game information
    return

def buryMines(data):
    for i in range (0,10):
        for counter in range (0,2):
            data.info[i][random.randint(0,data.cols-1)]=-1
            data.minesleft+=1
    # randomly select spots in the grid to place one or two mines per row
    return

def recursiveShow(row,col,data):
    if not (0<=row<data.rows and 0<=col<data.cols):
        return
    count=countAround(row,col,data)
    if data.info[row][col] == None:
        if count!=0:
            data.info[row][col]=count
        else:
            data.info[row][col]=count
            recursiveShow(row-1,col-1,data)
            recursiveShow(row-1,col,data)
            recursiveShow(row-1,col+1,data)
            recursiveShow(row,col-1,data)
            recursiveShow(row,col+1,data)
            recursiveShow(row+1,col-1,data)
            recursiveShow(row+1,col,data)
            recursiveShow(row+1,col+1,data)
    #Your code here
    return
    
        
def countAround(row,col,data):
    count=0
    for i in [-1,0,1]:
        for j in [-1,0,1]:
            if (0<=row+i<data.rows and 0<=col+j<data.cols):
                if data.info[row+i][col+j]==-1:
                    count+=1
    # count the number of mines around the cell at (row, col), 
    # return integer 
    return count

####################################
# Controller
####################################

def leftMousePressed(event, data):
    if data.gameOver==False and data.paused==False:
        x=event.x
        y=event.y
        row,col=withInCell(x,y,data)
        if data.info[row][col]==-1:
            data.gameOver=True
            data.win=False
        else:
            recursiveShow(row,col,data)
    # recognize left click, if the cell clicked is not a mine, check all the c
    # cells around it, if it is a mine, game over
    return

def rightMousePressed(event,data):
    if data.gameOver==False:
        x=event.x
        y=event.y
        row,col=withInCell(x,y,data)
        if data.flagged[row][col]==False:
            data.flagged[row][col]=True
            data.minesleft-=1
        else:
            data.flagged[row][col]=False
            data.minesleft+=1
    if data.gameOver==True:
        return
    #Bonus
    #Your code here
    return

def keyPressed(event, data):
    if data.gameOver==False:
        if event.keysym=="p":
            if data.paused==True:
                data.paused=False
            else:
                data.paused=True
    if event.keysym=="r":
        init(data)
    #Your code here  
    # recognize pressed key, if it is "p" pause the game     
    return
    
def timerFired(data):
    if data.gameOver==False and data.paused==False:
        data.time +=1
    
    for i in range (0,10):
        for j in range(0,10):
            if data.info[j][i]==None:
                data.win=False
                return
    data.win=True
    data.gameOver=True
    
    # check if the user has visited all the non-mine cells
    # if so, user wins the game
    return data.time

####################################
# View
####################################

def drawBoard(canvas, data):
    canvas.create_rectangle(0,500,500,575,fill="#606060")
    canvas.create_text(100,525, fill="white", font="Arial 18 bold", text="Time elapsed: ")
    canvas.create_text(200,525, fill="white", font="Arial 18 bold", text=str(data.time))
    canvas.create_text(150,550, fill="white", font="Arial 12 bold", text="press 'p' to pause")
    canvas.create_text(375,525, fill="white", font="Arial 18 bold", text="Mines left: ")
    canvas.create_text(460,525, fill="white", font="Arial 18 bold", text=str(data.minesleft))
    canvas.create_text(350,550, fill="white", font="Arial 12 bold", text="press 'r' to restart")
    #^^information in gray box below game (mines left, time, how to press pause)
    canvas.create_rectangle(500,0,750,70,fill="#9ffcf3")
    canvas.create_rectangle(500,70,750,575,fill="#cef29f")
    canvas.create_text(625,35,fill="black", font="Arial 18 bold", text="LEADERBOARD")
    data.sortedleader=sorted(data.leaderboard,key=lambda x: x[1])
    print(data.sortedleader)
    window=0
    while window+1<=len(data.sortedleader) and window<10:
        canvas.create_text(610,100+50*window, fill="black", font="Arial 18", text=data.sortedleader[window])
        window+=1
    for i in range (0,10):
        for j in range(0,10):
            canvas.create_rectangle(0+50*j,0+50*i,50+50*j,50+50*i,fill='white')
            if (data.info[j][i]!=None and data.info[j][i]!=-1):
                canvas.create_rectangle(0+50*j,0+50*i,50+50*j,50+50*i,fill='#f8ff82')
    for row in range (data.rows):
        for col in range (data.cols):
            if data.info[row][col]!=-1:
                if data.info[row][col]==1:         
                    canvas.create_text(row*50+50/2, col*50+50/2,fill="#9242f4", font="Arial 18 bold", text=str(data.info[row][col]))
                if data.info[row][col]==2:
                    canvas.create_text(row*50+50/2,col*50+50/2, fill="green", font="Arial 18 bold", text=str(data.info[row][col]))
                if data.info[row][col]==3:
                    canvas.create_text(row*50+50/2,col*50+50/2, fill="#42b3f4", font="Arial 18 bold", text=str(data.info[row][col]))
                if data.info[row][col]==4:
                    canvas.create_text(row*50+50/2,col*50+50/2, fill="magenta", font="Arial 18 bold", text=str(data.info[row][col]))
                if data.info[row][col]==5:
                    canvas.create_text(row*50+50/2,col*50+50/2, fill="red", font="Arial 18 bold", text=str(data.info[row][col]))
                if data.info[row][col]==6:
                    canvas.create_text(row*50+50/2,col*50+50/2, fill="#e88420", font="Arial 18 bold", text=str(data.info[row][col]))
            if data.flagged[row][col]==True:
                canvas.create_polygon((row*50+10,col*50+10),(row*50+40,col*50+25),(row*50+10,col*50+40), fill="blue")
                canvas.create_rectangle(row*50+10,col*50+10,row*50+15,col*50+47,fill="black")
    # draw individual cells on the board. Mine, non-mine, visited, 
    # and unvisited cells should all look different
    return
       
def drawPaused(canvas,data):
    if data.paused==True:
         canvas.create_text(250,250,fill="black", font="Arial 45 bold",text="PAUSED")
    # show text in the center of the board that tells the user the game
    # is paused if data.paused is True
    return

def drawGameOver(canvas, data):
    if data.gameOver==True:
        for i in range (0,10):
            for j in range(0,10):
                if data.info[j][i]==-1:
                    canvas.create_oval(10+50*j,10+50*i,40+50*j,40+50*i,fill='red')
    if data.win==True:
        canvas.create_text(250,250,fill="darkblue", font="Arial 26 bold",
                                         text="CONGRATS! YOU WIN!")
    elif data.win==False and data.gameOver==True:
        canvas.create_text(250,250,fill="#721313", font="Arial 26 bold",
                                         text="YOU LOSE! TRY AGAIN!")
    if data.win==True and data.windowbool==False:
        userName=simpledialog.askstring("Question","What is your name?")
        data.leaderboard.append((userName,data.time))
        data.leaderboard.append(("Jeannie",25))
        data.leaderboard.append(("Kate", 50))
        data.leaderboard.append(("Maria",45))
        data.leaderboard.append(("Ebow", 30))
        data.sortedleader=sorted(data.leaderboard,key=lambda x: x[1])
        data.windowbool=True
    winnerfile=open("minesweeperleaderboard.txt","w+")
    for i in range (0,len(data.sortedleader)):
        winnerfile.write(str(data.sortedleader[i]))
        winnerfile.write("\n")
    winnerfile.close()
        
    # show text in the center of the board that tells the user the game
    # is over if data.gameOver is True. Show different messages for winning
    # and losing
    return

def redrawAll(canvas, data):
    drawBoard(canvas, data)
    drawPaused(canvas,data)
    drawGameOver(canvas, data)

####################################
# Use the run function as-is
####################################

def run(width=500, height=500):
    # Run function adapted from David Kosbie's 
    # snake-demo.py for 15-112 (CarpeDiem!)
    def redrawAllWrapper(canvas, data):
        canvas.delete(ALL)
        redrawAll(canvas, data)
        canvas.update()    

    def leftMousePressedWrapper(event, canvas, data):
        leftMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def rightMousePressedWrapper(event, canvas, data):
        rightMousePressed(event, data)
        redrawAllWrapper(canvas, data)

    def keyPressedWrapper(event, canvas, data):
        keyPressed(event, data)
        redrawAllWrapper(canvas, data)

    def timerFiredWrapper(canvas, data):
        timerFired(data)
        redrawAllWrapper(canvas, data)
        # pause, then call timerFired again
        canvas.after(data.timerDelay, timerFiredWrapper, canvas, data)

    # Set up data and call init
    class Struct(object): pass

    data = Struct()
    data.width = width
    data.height = height
    data.timerDelay = 1000 # milliseconds
    init(data)
    # create the root and the canvas
    root = Tk()
    canvas = Canvas(root, width=data.width, height=data.height)
    canvas.pack()
    # set up events
    root.bind("<Button-1>", lambda event:
                            leftMousePressedWrapper(event, canvas, data))
    root.bind("<Button-3>", lambda event:
                            rightMousePressedWrapper(event, canvas, data))
    root.bind("<Key>", lambda event:
                            keyPressedWrapper(event, canvas, data))
    timerFiredWrapper(canvas, data)
    # and launch the app
    root.mainloop()  # blocks until window is closed
    print("bye!")

run(750, 575)