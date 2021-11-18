
#we need a main function if __name__ == '__main__':

#basically we need functions to run the game in this class then...
#this function should be in game class. no separate class for a start function....
#end game would also be in the game class
#not needed

from GUI import GUI

class Player:
    def __init__(self, name, role):
        self.name = str(name)
        self.role = str(role)

    def getPlayerName(self):
        return self.name

    def changeRole(self, role):
        if role=="drawer":
            self.role="guesser"
        elif role=="guesser":
            self.role="drawer"

    def getRole(self):
        return self.role

    #getter (return the variable that is found in the class)
    #setter (pass variable in the function and save it in the class)


class Team:
    def __init__(self, name, player1, player2):
        self.name = str(name)
        self.score =0
        self.outcome = -1
        self.players = [player1, player2]

    def getPlayers(self):
        return self.players

    def addScore(self):
        self.score = self.score+1

    def setOutcome(self, outcome):
        self.outcome=outcome

    def getName(self):
        return self.name

    def getScore(self):
        return self.score

    def __str__(self):
        return self.name + ": " +self.players[0].getPlayerName()+", "+ self.players[1].getPlayerName()+" - scpre:"+self.score

    #function that sets the score +1
    #function that sets the final outcome (boolean OR int)
    #tostring method to print the team: "NameExampe: Player1Example Player2Example - score"


#work has to be done in the game class?
#initialize  teams and players, then scoreboard then start the actual game
class Game:
    def __init__(self):
        self.teams = []
        self.turns = 30
        self.guess = ""
        self.playingTeam = -1
        self.position = 1
        self.order = {}
        self.words = ["car", "house", "tree", "window", "star", "fish", 
                     "light bulb", "pizza","donut", "dog", "cat", "cake",
                     "candle", "cupid", "baby", "mug", "airplane","book", 
                     "rocket", "mouse", "TV", "iphone", "laptop", "crown", 
                     "bee", "bicycle", "cow", "flag", "heart", "boat"]

    def startGame(self): #user asked if want to proceed with the game
        x=input("Do you want to start the game?\nType Yes or No: ")
        print("\n")
        if x.lower() == "no":
            print("You did not start the game")
            return False
        elif x.lower() == "yes":
            print("The game has started")
            self.gui = GUI((800,600))
            return True

    def chooseGame(self): #user picks between 4 and 6 player game
        x = int(input("Do you want to create a 4 players game or 6 players game\nType 4 or 6: "))
        print("\n")
        if x==4:
            return 2
        elif x==6:
            return 3

    def createTeams(self,n): #creates the teams and players within the teams that will be playing in the game
        for i in range(1,n+1):
            question = "What do you want to call team #"+str(i)+"? "
            x=input(question)
            p1=input("First Player's name: ")
            p2=input("Second Player's name: ")
            print("\n")

            P1= Player(p1,"drawer")
            P2= Player(p2,"guesser")
            t= Team(x, P1, P2)
            self.teams+=[t]
        
        #shuffle teams
        self.chooseOrder()

        #to get teams' names
        self.t = []
        print(len(self.teams))
        for i in range(len(self.teams)):
            name = self.teams[i].getName()
            self.t+=[name]
            self.order[name] = i

        #send the team names to the GUI
        self.gui.setTeams(self.t)


    def setPlayingTeam(self): #setting the team that is actually playing at the moment
        if self.playingTeam==len(self.teams)-1:
            self.playingTeam=0
        else:
            self.playingTeam=self.playingTeam+1
        print("Team: "+self.teams[self.playingTeam].getName()+ " is now playing")
        print("\n")

    def setRoles(self):
        t=self.teams[self.playingTeam]
        players=t.getPlayers()
        pl1=players[0]
        pl2=players[1]

        pl1.changeRole(pl1.getRole())
        pl2.changeRole(pl2.getRole())
        print("Team: "+t.getName()+"\n\t"+ pl1.getPlayerName()+": "+pl1.getRole()+"\n\t"+pl2.getPlayerName()+": "+pl2.getRole())

    def continueGame(self):
        if self.checkForWinner() == True: #a team arrived to 5
            winningTeamIndex = self.ranking()
            continueGame = self.canContinue(winningTeamIndex)
            
            if continueGame == False: #if the length is 2 or if the other teams don't want to continue
                return
            else:
                self.playingTeam = -1 # resetting the team that starts 
                self.startTurn()
            
        elif self.turns == 0: #if game ends before they reach a score of 5
            if len(self.teams)==3: #check so we don't get out of bounds if 2 teams
                firstPlaceIndex = self.ranking()
                self.teams.remove(self.teams[firstPlaceIndex])
                secondPlaceIndex = self.ranking()
                self.teams.remove(self.teams[secondPlaceIndex])
                self.ranking()
            else:
                firstPlaceIndex = self.ranking()
                self.teams.remove(self.teams[firstPlaceIndex])
                secondPlaceIndex = self.ranking()
            
            if self.resetGame() == True:
                self.resetVariables()

        elif self.resetGame() == True:
            self.resetVariables()            

        elif self.endGame() == True:
            return

        else:
            #continue
            print("Next Team's Turn")
            self.startTurn()
            
    def canContinue(self,index): #checks if teams should proceed or not with the game (depending on number of teams)
        #check if length of teams is 2 or 3
        if len(self.teams)==2: 
            self.teams.remove(self.teams[index])
            self.ranking()
            return False #to end game
        else:
            x=input("Do you wish to continue without "+ self.teams[index].getName()+": ")
            if x.lower()=="yes":
                self.teams.remove(self.teams[index]) #removing the winning team so the others can continue
                return True
            elif x.lower()=="no": 
                #get rank of team in second place
                self.teams.remove(self.teams[index])
                index = self.ranking() #getting index of second place team to use in the next line

                #get rank of team in third place
                self.teams.remove(self.teams[index])
                self.ranking()
                return False #to end game

    def startTurn(self):
        print(" ")
        self.setPlayingTeam() #setting the team that starts at the turn
        self.setRoles()#setting the role of the team for that turn
        self.setWord() #picking the word for the turn

        print("You have 60 seconds to draw\nGo!")
        self.setTimer() #starts the timer for this turn


    def resetGame(self): #user is asked to reset the game at any point if they want
        user_input = input("\nDo you want to restart?\nType Yes or No: ")
        if user_input.lower() == "no":  # Converts input to lowercase for comparison
            return False
        elif user_input.lower() == "yes":
            return True

    def resetVariables(self):
        #reset all the values of the Game
        self.teams = []
        self.turns = 30
        self.guess = ""
        self.playingTeam = -1
        self.position = 1

        #restart the whole implementation
        self.run(True)

    def endGame(self): #user is asked to end the game at any pooint if they want
        x = input("Do you want to end the game?\nType Yes or No: ")
        if x.lower() == "no":
            return False
        elif x.lower() == "yes":
            return True

    def setWord(self): #provides the guesser with the word the drawer in its team should draw for him/her to guess
        import random
        self.guess = random.choice(self.words)
        print("Draw the word "+self.guess+"\n")
        self.words.remove(self.guess)
        return self.guess

    def guessWord(self): #the guesser's guess
        x=input("What's your guess? ")
        print("\n")
        return x

    def checkWord(self, x): # checks if the guesser guessed correctly
        if x==self.guess:
            self.teams[self.playingTeam].addScore() #in the teams list the team that's playing gets a point
            print("You guessed it!")
            return True
        else:
            print("Incorrect!")
            return False

    def setScore(self):
        score = self.teams[self.playingTeam].getScore()
        print("Your team's current score: "+str(score))
        name = self.teams[self.playingTeam].getName()

        #pass the GUI the score
        if self.order[name] == 0:
            self.gui.setScore1(score)
        elif self.order[name] == 1:
            self.gui.setScore2(score)
        else:
            self.gui.setScore3(score)

    def ranking(self): #gives the index of the highest ranked team
        highest = 0
        index = -1

        for i in range(len(self.teams)):
            currentScore = self.teams[i].getScore()

            if currentScore >= highest:
                highest = currentScore
                index=i

        #set the place of current team
        self.teams[index].setOutcome(self.position)
        print(self.teams[index].getName() +" ranked: "+ str(self.position)) 
        self.position += 1
        return index

    #recursive function
    def setTimer(self): #gives the drawer 60s to draw each word      
        #two things can happen:
        #either i attempted a guess
        #or times up (60)
        if self.gui.updateTimer() == -1:
            #check if word is correct
            x=self.guessWord()
            if self.checkWord(x) == True: #correct
                self.carryOn()
            else:
                print("Resuming timer")
                self.gui.resumeTimer()
                self.setTimer()

        else:
            self.timesUp()


    def chooseOrder(self): #gives the order of team turns
        import random
        random.shuffle(self.teams)
        print("The teams have been shuffled")

    def timesUp(self):
        print("Time's up!")

        #last chance to guess word
        x=self.guessWord()
        self.checkWord(x)
        self.carryOn() #continues...
        
    def carryOn(self):
        #reset gui timer
        self.gui.resetTimer()

        #set the score
        self.setScore()

        #remove a turn from the whole game
        self.decrementTurns()

        #check if we should start a new turn
        self.continueGame()

    def decrementTurns(self):
        self.turns -= 1
        print("A turn has passed\nThere are "+str(self.turns)+" left \n")

    def checkForWinner(self): #to check if a team has accumulated enough points to win
        for team in self.teams:
            if team.getScore() == 5:
                print("We found a winner!\n")
                return True
        print("No winner yet\nKeep Playing!\n")
        return False

    def run(self, reset=False): #whole implementation of the game
        if reset == False: #only happen in first run
            self.startGame()
        numberOfTeams = self.chooseGame()

        if numberOfTeams == -1:
            return False
        
        self.createTeams(numberOfTeams)
        self.startTurn()


    #4 or 6 players -> function teams 2 or 3
    #input the names of teams / players

    #function for starting game
    #function for ending game
    #function for getting players (turns of drawer and guesser)
    #function for getting teams (who starts and then setting each turn whose turn it is)
    #function for getting word (remove the word)
    #function for start and end timer
        #function for drawing / guessing
    #function for showing results
    #function for showing scores at every point.
    #decrement turn and check if we should stop of not
    #see if anyone won yet
    #get ranking

# def run():
#     numberOfTeams = g.startGame()

#     if numberOfTeams == -1:
#         return
        
#     g.createTeams(numberOfTeams)
#     g.startTurn()

g = Game()
g.run()


