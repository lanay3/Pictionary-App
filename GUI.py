from tkinter import *
from tkinter import colorchooser
import threading, time

class GUI(threading.Thread): #inheritance
    def __init__ (self,wh): #constructor
        #threading
        threading.Thread.__init__(self) #calling constructor in parent class
        self.start() #call the run function

        self.width = 3 #of pen
        self.color = "black" #of pen
        self.dimensions = wh #Tupple containing width and height of frame
        self.pointx = None
        self.pointy = None
        self.mostRecentColor = "black"
        
        #teams
        self.team1 = None
        self.team2 = None
        self.team3 = None

        #timer
        self.timeValue = 60
        self.pause = False


    #start function of the thread
    def run(self): #thread runs and uses it implicetly + runs GUI
        #using Tkinter
        t=Tk()
        t.title("Drawing") #parent
        t.protocol("WM_DELETE_WINDOW", self.end) #this is since i am using a thread -> to close the thread
        self.parent = t
        self.creatingElements() 
        self.createTimer()

        #binding events to functions  
        self.canvas.bind("<B1-Motion>", self.draw) #when canvas feels a motion, it lets us want to draw 
        self.canvas.bind("<ButtonRelease-1>", self.callibrate) #to avoid lagging when drawing
        self.parent.mainloop() 

    #end function of the thread
    def end(self): #exit the code
        self.parent.quit()

    def creatingElements(self): 
        #sidebar that will contain the buttons and scoreboard
        self.tools=Frame(self.parent, padx=5, pady=5) 

        #Buttons
        Label(self.tools, text=" ").grid(row=9, column=0)
        Button(self.tools,text="Clear", command=self.clear).grid(row=10,column=0)
        Label(self.tools, text=" ").grid(row=11, column=0)
        Button(self.tools, text="Pick Color", command=self.pickColor).grid(row=12, column=0)
        Label(self.tools, text=" ").grid(row=13, column=0)
        Button(self.tools, text="Eraser", command=self.erase).grid(row=14, column=0)
        Label(self.tools, text=" ").grid(row=15, column=0)
        Button(self.tools, text="Draw", command=self.pen).grid(row=16, column=0)

        Button(self.tools, text="Attempt guess", command=self.pauseTimer).grid(row=19, column=0)
        self.tools.pack(side=LEFT)

        #creating the canvas where we can draw
        self.canvas=Canvas(self.parent,width=self.dimensions[0],height=self.dimensions[1], bg="grey")
        self.canvas.pack(fill=BOTH, expand=TRUE)

    def clear(self): #clears the drawing
        self.canvas.delete(ALL)
    
    def pickColor(self): #enables user to pick the color they want to use
        self.color= colorchooser.askcolor(color=self.color)[1]
        self.mostRecentColor=self.color #storing the most recent color they used before erasing so they can use it again
    
    def draw(self,e): #e is for event/something it grabs
        if self.pointx and self.pointy: 
            self.canvas.create_line(self.pointx, self.pointy, e.x, e.y, width=self.width, fill=self.color, smooth=True, capstyle=ROUND)
        
        #update x and y
        self.pointx= e.x
        self.pointy= e.y

    def callibrate(self,e): #when draw again don't want to keep pointx and pointy and set it back to none
        self.pointx= None
        self.pointy= None

    def erase(self): #erases the drawing by click using the color white
        self.color = "grey"
        self.width = 20  

    def pen(self): #enables us to draw after erasing
        self.color = self.mostRecentColor #setting it to the most recent color used
        self.width = 3

    def createTimer(self): #creating the timer for the game
        Label(self.tools, text=" ").grid(row=17, column=0)
        Label(self.tools, text="Timer", font=("Times 24")).grid(row=18, column=0)
        Label(self.tools, text="{:02}".format(self.timeValue), font=("Times 20")).grid(row=18, column=1)

    #go back to classes - check word
    def pauseTimer(self):
        self.pause = True

    def resumeTimer(self):
        self.pause = False

    def resetTimer(self):
        self.timeValue = 60
        self.resumeTimer()

    #updates the timer
    def updateTimer(self):
        for i in range(self.timeValue,-1,-1): #decrementing the value from 60
            if self.pause == True: #this checks if i paused
                return -1

            self.timeValue = i
            self.createTimer()
            time.sleep(1) # this function pauses the for loop for 1 second

        return 200


    def createScoreboard(self): #creating the scoreboard for the game
        Label(self.tools, text="Scoreboard", font=("Times 24")).grid(row=0, column=0)
        Label(self.tools, text=" ").grid(row=1, column=0)
        Label(self.tools, text=" ").grid(row=2, column=0)

        #team1
        if self.team1:
            Label(self.tools, text=self.team1, font=("Times 16")).grid(row=3, column=0)
            self.score1 = Text(self.tools, height=1, width=1)
            self.score1.grid(row=3, column=1)
            self.score1.insert(END, 0)
            self.score1.config(state=DISABLED)
            Label(self.tools, text=" ").grid(row=4, column=0)

        #team2
        if self.team2:
            Label(self.tools, text=self.team2, font=("Times 16")).grid(row=5, column=0)
            self.score2 = Text(self.tools, height=1, width=1)
            self.score2.grid(row=5, column=1)
            self.score2.insert(END, 0)
            self.score2.config(state=DISABLED)
            Label(self.tools, text=" ").grid(row=6, column=0)

        #team3
        if self.team3:
            Label(self.tools, text=self.team3, font=("Times 16")).grid(row=7, column=0)
            self.score3 = Text(self.tools, height=1, width=1)
            self.score3.grid(row=7, column=1)
            self.score3.insert(END, 0)
            self.score3.config(state=DISABLED)
            Label(self.tools, text=" ").grid(row=8, column=0)

    def setTeams(self, teams): #it takes the teams from the classes and sets them in the GUI
        self.team1=teams[0]
        self.team2=teams[1]
        if len(teams)==3:
            self.team3=teams[2]
        
        self.createScoreboard()

    def setScore1(self, s1):
        self.score1.config(state=NORMAL)
        self.score1.delete(1.0, END)
        self.score1.insert(END, s1)
        self.score1.config(state=DISABLED)
    
    def setScore2(self, s2):
        self.score2.config(state=NORMAL)
        self.score2.delete(1.0, END)
        self.score2.insert(END, s2)
        self.score2.config(state=DISABLED)

    def setScore3(self, s3):
        self.score3.config(state=NORMAL)
        self.score3.delete(1.0, END)
        self.score3.insert(END, s3)
        self.score3.config(state=DISABLED)
