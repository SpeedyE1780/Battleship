from tkinter import *
import tkinter.messagebox
from tkinter.ttk import Combobox
import random
import tkinter.simpledialog
from tkinter.filedialog import asksaveasfilename , askopenfilename
from winsound import *
import pygame.mixer

pygame.init()

class BattleShip:

    def __init__(Self):

        pygame.mixer.music.load("Sounds/Background.wav")
        Self.hit_sound = pygame.mixer.Sound("Sounds/Hit.wav")
        Self.miss_sound = pygame.mixer.Sound("Sounds/Miss.wav")
        
	##Initial Window
        Self.Window = Tk()
        Self.Window.resizable(False , False)
        Self.Window.title("BATTLESHIP!")
        
        ##Create Menu
        Menubar = Menu(Self.Window)
        Self.Window.config(menu = Menubar)
        FileMenu = Menu(Menubar , tearoff = 0)
        Menubar.add_cascade(label = "File" , menu =FileMenu)
        FileMenu.add_command(label = "Open" , command = Self.OpenSaveGame)
        FileMenu.add_command(label = "Save" , command = Self.SaveGame)

        FileMenu.add_separator()
        FileMenu.add_command(label = "Help" , command = Self.showHelp)

        FileMenu.add_separator()
        FileMenu.add_command(label = "Exit" , command = exit)

        ##Main Menu Frame
        Self.MainMenu = Frame(Self.Window)
        Self.MainMenu.pack()

        Self.MM = PhotoImage(file = "Images/BattleShip_Background.gif")
        Self.MainMenuBG = Label(Self.MainMenu , image = Self.MM)
        Self.MainMenuBG.pack()

        Self.StartGamebtn = Button(Self.MainMenu , text = "Start" ,
                                   command = Self.start)
        Self.StartGamebtn.pack()

        Self.nbPlayers = IntVar()

        Self.Player1RB = Radiobutton(Self.MainMenu , text = "1 Player " ,
                                     variable = Self.nbPlayers , value = 1)
        Self.Player1RB.pack()

        Self.Player2RB = Radiobutton(Self.MainMenu , text = "2 Player " ,
                                     variable = Self.nbPlayers , value = 2)
        Self.Player2RB.pack()

        Self.SFX = False
        Self.SoundCHK = Checkbutton(Self.MainMenu , text =  "Sound Effects" , variable = Self.SFX , command = Self.playSFX)
        Self.SoundCHK.pack()

        ##Game Frame
        Self.GameFrame = Frame(Self.Window)
        Self.Ships = ("Carrier" , "Battleship" , "Cruiser" , "Submarine" , "Destroyer")
        Self.Orient = ("Vertical" , "Horizontal")

        """
        Ships Position on the grid:
        Opponent Miss = 9
        Empty Space = 0
        Damaged Ship = 1
        Carrier = 2
        Battleship = 3
        Cruiser = 4
        Submarine = 5
        Destroyer = 6
        """
        Self.player1_ship = []
        Self.player1_Carrierlife = 5
        Self.player1_Battleshiplife = 4
        Self.player1_Cruiserlife = 3
        Self.player1_Submarinelife = 3
        Self.player1_Destroyerlife = 2
        
        Self.player2_ship = []
        Self.player2_Carrierlife = 5
        Self.player2_Battleshiplife = 4
        Self.player2_Cruiserlife = 3
        Self.player2_Submarinelife = 3
        Self.player2_Destroyerlife = 2
        
        Self.computer_ship = []
        Self.computer_Carrierlife = 5
        Self.computer_Battleshiplife = 4
        Self.computer_Cruiserlife = 3
        Self.computer_Submarinelife = 3
        Self.computer_Destroyerlife = 2

        for i in range(0 , 10):
            Self.player1_ship.append([0])
            Self.player2_ship.append([0])
            Self.computer_ship.append([0])
            for j in range(0 , 9):
                Self.player1_ship[i].append(0)
                Self.player2_ship[i].append(0)
                Self.computer_ship[i].append(0)
                

        """
        Hits Position on the grid:
        No Hit = 0
        Hit = 1
        Miss = 2
        """
        Self.player1_hits = []
        Self.player2_hits = []
        Self.computer_hits = []

        for i in range(0 , 10):
            Self.player1_hits.append([0])
            Self.player2_hits.append([0])
            Self.computer_hits.append([0])
            for j in range(0 , 9):
                Self.player1_hits[i].append(0)
                Self.player2_hits[i].append(0)
                Self.computer_hits[i].append(0)

        ##The total number of hits needed to destroy every ship: 5 + 4 + 3 + 3 + 2 = 17
        Self.player1life = 17
        Self.player2life = 17
        Self.computerlife = 17

        Self.P1name = ""
        Self.P1password = ""

        Self.P2name = ""
        Self.P2password = ""

        Self.canOpen = True
        Self.canSave = False

        Self.sMainMenu()

        Self.Window.mainloop()

    def OpenSaveGame(Self):

        if Self.canOpen:

            try:
                filepath = askopenfilename()
                file = open(filepath , "r")
                Content = file.read()
                Content = Content.split("/")

                ##Check that it's a savefile
                if Content[0] == "Battleship":

                    Self.MainMenu.pack_forget()
                    Self.GameFrame.pack()
                    Self.canOpen = False

                    if int(Content[1]) == 1:
                        
                        ##Player 1 Data
                        Self.PlayerFrame = Frame(Self.GameFrame)
                        Self.PlayerFrame.pack()

                        ##Player Ships Frame
                        Self.PlayerShips = Frame(Self.PlayerFrame)
                        Self.PlayerShips.pack()

                        label = Label(Self.PlayerShips , text = "Player Ships")
                        label.grid(row = 0 , column = 0)
                        ##Place the column coordinates
                        for i in range(1 , 11):

                            label = Label(Self.PlayerShips , text = str(i))
                            label.grid(row = 1 , column = i + 1)

                        ##Place the row coordinates
                        lrow = 1
                        for i in range(ord("A") , (ord("A") + 10)):

                            label = Label(Self.PlayerShips , text = chr(i))
                            label.grid(row = lrow + 1 , column = 1)
                            lrow += 1
                            
                        ##Player Hits Frame
                        Self.PlayerHitsFrame = Frame(Self.PlayerFrame)
                        Self.PlayerHitsFrame.pack()
                        
                        label = Label(Self.PlayerHitsFrame , text = "Player Hits")
                        label.grid( row = 0 , column = 0)
                        ##Place the column coordinates
                        for i in range(1 , 11):

                            label = Label(Self.PlayerHitsFrame , text = str(i))
                            label.grid(row = 1 , column = i + 1)

                        ##Place the row coordinates
                        lrow = 1
                        for i in range(ord("A") , (ord("A") + 10)):

                            label = Label(Self.PlayerHitsFrame , text = chr(i))
                            label.grid(row = lrow + 1 , column = 1)
                            lrow += 1

                        ##Fill The Player's variable
                        counter = 0
                        for i in range(0 , len(Self.player1_hits)):
                            for j in range(0 , len(Self.player1_hits[0])):
                                
                                Self.player1_ship[i][j] = int(Content[2][counter])

                                if Self.player1_ship[i][j] > 1 and Self.player1_ship[i][j] <9:
                                    label = Label(Self.PlayerShips , text = "X")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player1_ship[i][j] == 1:
                                    label = Label(Self.PlayerShips , text = "*")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player1_ship[i][j] == 9:
                                    label = Label(Self.PlayerShips , text = "O")
                                    label.grid(row = i + 2 , column = j + 2)

                                else:
                                    label = Label(Self.PlayerShips , text = " ")
                                    label.grid(row = i + 2 , column = j + 2)

                                Self.player1_hits[i][j] = int(Content[3][counter])

                                if Self.player1_hits[i][j] == 1:
                                    label = Label(Self.PlayerHitsFrame , text = "X")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player1_hits[i][j] == 2:
                                    label = Label(Self.PlayerHitsFrame , text = "O")
                                    label.grid(row = i + 2 , column = j + 2)

                                else:
                                    label = Label(Self.PlayerHitsFrame , text = " ")
                                    label.grid(row = i + 2 , column = j + 2)

                                counter += 1

                        ##Enter Hit Coordinates

                        Self.rowcoordinate = Label(Self.PlayerFrame , text = "Row")
                        Self.rowcoordinate.pack()

                        Self.rowhit = StringVar()
                        Self.rowentry = Entry(Self.PlayerFrame , textvariable = Self.rowhit)
                        Self.rowentry.pack()

                        Self.columncoordinate = Label(Self.PlayerFrame , text = "Column")
                        Self.columncoordinate.pack()

                        Self.columnhit = StringVar()
                        Self.columnentry = Entry(Self.PlayerFrame , textvariable = Self.columnhit)
                        Self.columnentry.pack()

                        Self.hitbutton = Button(Self.PlayerFrame , text = "HIT!" , command = Self.playerhit)
                        Self.hitbutton.pack()

                        ##Player Life
                        Self.player1life = int(Content[4])
                        Self.player1_Carrierlife = int(Content[5])
                        Self.player1_Battleshiplife = int(Content[6])
                        Self.player1_Cruiserlife = int(Content[7])
                        Self.player1_Submarinelife = int(Content[8])
                        Self.player1_Destroyerlife = int(Content[9])

                        ##Computer Data

                        ##Computer Ships and Hits
                        counter = 0
                        for i in range(0 , len(Self.computer_ship)):
                            for j in range(0 , len(Self.computer_ship[0])):
                                Self.computer_ship[i][j] = int(Content[10][counter])
                                Self.computer_hits[i][j] = int(Content [11][counter])
                                counter += 1

                        ##Computer Life
                        Self.computerlife = int(Content [12])
                        Self.computer_Carrierlife = int(Content[13])
                        Self.computer_Battleshiplife = int(Content[14])
                        Self.computer_Cruiserlife = int(Content[15])
                        Self.computer_Submarinelife = int(Content[16])
                        Self.computer_Destroyerlife = int(Content[17])

                    else:

                        ##Player 1 Data
                        Self.Player1Frame = Frame(Self.GameFrame)

                        ##Player 1 Info
                        Self.P1name = Content[18]
                        Self.P1password = Content[19]

                        ##Player1 Ships Frame
                        Self.Player1Ships = Frame(Self.Player1Frame)
                        Self.Player1Ships.pack()

                        label = Label(Self.Player1Ships , text = Self.P1name + "'s Ships: ")
                        label.grid(row = 0 , column = 0)
                        ##Place the column coordinates
                        for i in range(1 , 11):

                            label = Label(Self.Player1Ships , text = str(i))
                            label.grid(row = 1 , column = i + 1)

                        ##Place the row coordinates
                        lrow = 1
                        for i in range(ord("A") , (ord("A") + 10)):

                            label = Label(Self.Player1Ships , text = chr(i))
                            label.grid(row = lrow + 1 , column = 1)
                            lrow += 1
                            
                        ##Player Hits Frame
                        Self.Player1HitsFrame = Frame(Self.Player1Frame)
                        Self.Player1HitsFrame.pack()
                        
                        label = Label(Self.Player1HitsFrame , text = Self.P1name + "'s Hits:")
                        label.grid( row = 0 , column = 0)
                        ##Place the column coordinates
                        for i in range(1 , 11):

                            label = Label(Self.Player1HitsFrame , text = str(i))
                            label.grid(row = 1 , column = i + 1)

                        ##Place the row coordinates
                        lrow = 1
                        for i in range(ord("A") , (ord("A") + 10)):

                            label = Label(Self.Player1HitsFrame , text = chr(i))
                            label.grid(row = lrow + 1 , column = 1)
                            lrow += 1

                        ##Fill The Player's variable
                        counter = 0
                        for i in range(0 , len(Self.player1_hits)):
                            for j in range(0 , len(Self.player1_hits[0])):
                                
                                Self.player1_ship[i][j] = int(Content[2][counter])

                                if Self.player1_ship[i][j] > 1 and Self.player1_ship[i][j] < 9:
                                    label = Label(Self.Player1Ships , text = "X")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player1_ship[i][j] == 1:
                                    label = Label(Self.Player1Ships , text = "*")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player1_ship[i][j] == 9:
                                    label = Label(Self.Player1Ships , text = "O")
                                    label.grid(row = i + 2 , column = j + 2)

                                else:
                                    label = Label(Self.Player1Ships , text = " ")
                                    label.grid(row = i + 2 , column = j + 2)

                                Self.player1_hits[i][j] = int(Content[3][counter])

                                if Self.player1_hits[i][j] == 1:
                                    label = Label(Self.Player1HitsFrame , text = "X")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player1_hits[i][j] == 2:
                                    label = Label(Self.Player1HitsFrame , text = "O")
                                    label.grid(row = i + 2 , column = j + 2)

                                else:
                                    label = Label(Self.Player1HitsFrame , text = " ")
                                    label.grid(row = i + 2 , column = j + 2)

                                counter += 1

                        ##Enter Hit Coordinates

                        Self.rowcoordinate = Label(Self.Player1Frame , text = "Row")
                        Self.rowcoordinate.pack()

                        Self.P1rowhit = StringVar()
                        Self.rowentry = Entry(Self.Player1Frame , textvariable = Self.P1rowhit)
                        Self.rowentry.pack()

                        Self.columncoordinate = Label(Self.Player1Frame , text = "Column")
                        Self.columncoordinate.pack()

                        Self.P1columnhit = StringVar()
                        Self.columnentry = Entry(Self.Player1Frame , textvariable = Self.P1columnhit)
                        Self.columnentry.pack()

                        Self.hitbutton = Button(Self.Player1Frame , text = "HIT!" , command = Self.player1hit)
                        Self.hitbutton.pack()

                        ##Player Life
                        Self.player1life = int(Content[4])
                        Self.player1_Carrierlife = int(Content[5])
                        Self.player1_Battleshiplife = int(Content[6])
                        Self.player1_Cruiserlife = int(Content[7])
                        Self.player1_Submarinelife = int(Content[8])
                        Self.player1_Destroyerlife = int(Content[9])

                        ##Player 2 Data
                        Self.Player2Frame = Frame(Self.GameFrame)

                        ##Player 2 Info
                        Self.P2name = Content[20]
                        Self.P2password = Content[21]

                        ##Player2 Ships Frame
                        Self.Player2Ships = Frame(Self.Player2Frame)
                        Self.Player2Ships.pack()

                        label = Label(Self.Player2Ships , text = Self.P2name + "'s Ships:")
                        label.grid(row = 0 , column = 0)
                        ##Place the column coordinates
                        for i in range(1 , 11):

                            label = Label(Self.Player2Ships , text = str(i))
                            label.grid(row = 1 , column = i + 1)

                        ##Place the row coordinates
                        lrow = 1
                        for i in range(ord("A") , (ord("A") + 10)):

                            label = Label(Self.Player2Ships , text = chr(i))
                            label.grid(row = lrow + 1 , column = 1)
                            lrow += 1
                            
                        ##Player Hits Frame
                        Self.Player2HitsFrame = Frame(Self.Player2Frame)
                        Self.Player2HitsFrame.pack()
                        
                        label = Label(Self.Player2HitsFrame , text = Self.P2name + "'s Hits")
                        label.grid( row = 0 , column = 0)
                        ##Place the column coordinates
                        for i in range(1 , 11):

                            label = Label(Self.Player2HitsFrame , text = str(i))
                            label.grid(row = 1 , column = i + 1)

                        ##Place the row coordinates
                        lrow = 1
                        for i in range(ord("A") , (ord("A") + 10)):

                            label = Label(Self.Player2HitsFrame , text = chr(i))
                            label.grid(row = lrow + 1 , column = 1)
                            lrow += 1

                        ##Fill The Player's variable
                        counter = 0
                        for i in range(0 , len(Self.player2_hits)):
                            for j in range(0 , len(Self.player2_hits[0])):
                                
                                Self.player2_ship[i][j] = int(Content[10][counter])

                                if Self.player2_ship[i][j] > 1 and Self.player2_ship[i][j] < 9:
                                    label = Label(Self.Player2Ships , text = "X")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player2_ship[i][j] == 1:
                                    label = Label(Self.Player2Ships , text = "*")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player2_ship[i][j] == 9:
                                    label = Label(Self.Player2Ships , text = "O")
                                    label.grid(row = i + 2 , column = j + 2)

                                else:
                                    label = Label(Self.Player2Ships , text = " ")
                                    label.grid(row = i + 2 , column = j + 2)

                                Self.player2_hits[i][j] = int(Content[11][counter])

                                if Self.player2_hits[i][j] == 1:
                                    label = Label(Self.Player2HitsFrame , text = "X")
                                    label.grid(row = i + 2 , column = j + 2)

                                elif Self.player2_hits[i][j] == 2:
                                    label = Label(Self.Player2HitsFrame , text = "O")
                                    label.grid(row = i + 2 , column = j + 2)

                                else:
                                    label = Label(Self.Player2HitsFrame , text = " ")
                                    label.grid(row = i + 2 , column = j + 2)

                                counter += 1

                        ##Enter Hit Coordinates

                        Self.rowcoordinate = Label(Self.Player2Frame , text = "Row")
                        Self.rowcoordinate.pack()

                        Self.P2rowhit = StringVar()
                        Self.rowentry = Entry(Self.Player2Frame , textvariable = Self.P2rowhit)
                        Self.rowentry.pack()

                        Self.columncoordinate = Label(Self.Player2Frame , text = "Column")
                        Self.columncoordinate.pack()

                        Self.P2columnhit = StringVar()
                        Self.columnentry = Entry(Self.Player2Frame , textvariable = Self.P2columnhit)
                        Self.columnentry.pack()

                        Self.hitbutton = Button(Self.Player2Frame , text = "HIT!" , command = Self.player2hit)
                        Self.hitbutton.pack()

                        ##Player Life
                        Self.player2life = int(Content[12])
                        Self.player2_Carrierlife = int(Content[13])
                        Self.player2_Battleshiplife = int(Content[14])
                        Self.player2_Cruiserlife = int(Content[15])
                        Self.player2_Submarinelife = int(Content[16])
                        Self.player2_Destroyerlife = int(Content[17])

                        ##Player 1 Enters his password to resume the game
                        Self.password = tkinter.simpledialog.askstring("Password" , Self.P1name + " Enter Your Password:")

                        while not Self.password == Self.P1password:

                            tkinter.messagebox.showerror("Wrong Password" , "Enter Your Password")
                            Self.password = tkinter.simpledialog.askstring("Password" , Self.P1name + " Enter Your Password:")
                        
                        Self.Player1Frame.pack()

                else:
                    tkinter.messagebox.showerror("Invalid Save File" , "Please Choose A Battleship Save File")
            except FileNotFoundError:
                tkinter.messagebox.showerror("Can't Open File" , "No File Selected")

        else:
            tkinter.messagebox.showerror("Can't Open File" , "You Must be at main menu to open file")

        
    def SaveGame(Self):

        if Self.canSave:
            filepath = asksaveasfilename()
            file = open(filepath , "w")

            nb = Self.nbPlayers.get()

            ##Tag to check later that it's a save file
            file.write("Battleship/")
            file.write(str(nb) + "/")
                
            ##Save The Player Ships & Hits
            for i in range(0 , len(Self.player1_ship)):
                for j in range(0 , len(Self.player1_ship[0])):
                    file.write(str(Self.player1_ship[i][j]))
            file.write("/")

            for i in range(0 , len(Self.player1_hits)):
                for j in range(0 , len(Self.player1_hits[0])):
                    file.write(str(Self.player1_hits[i][j]))
            file.write("/")

            ##Save The Player's Life
            file.write(str(Self.player1life) + "/")

            file.write(str(Self.player1_Carrierlife) + "/")
            file.write(str(Self.player1_Battleshiplife) + "/")
            file.write(str(Self.player1_Cruiserlife) + "/")
            file.write(str(Self.player1_Submarinelife) + "/")
            file.write(str(Self.player1_Destroyerlife) + "/")

            if nb == 1:

                ##Save The Computer Ships & Hits
                for i in range(0 , len(Self.computer_ship)):
                    for j in range(0 , len(Self.computer_ship[0])):
                        file.write(str(Self.computer_ship[i][j]))
                file.write("/")

                for i in range(0 , len(Self.computer_hits)):
                    for j in range(0 , len(Self.computer_hits[0])):
                        file.write(str(Self.computer_hits[i][j]))
                file.write("/")

                ##Save The Computer's Life
                file.write(str(Self.computerlife) + "/")

                file.write(str(Self.computer_Carrierlife) + "/")
                file.write(str(Self.computer_Battleshiplife) + "/")
                file.write(str(Self.computer_Cruiserlife) + "/")
                file.write(str(Self.computer_Submarinelife) + "/")
                file.write(str(Self.computer_Destroyerlife))

            else:

                

                ##Save The Player Ships & Hits
                for i in range(0 , len(Self.player2_ship)):
                    for j in range(0 , len(Self.player2_ship[0])):
                        file.write(str(Self.player2_ship[i][j]))
                file.write("/")

                for i in range(0 , len(Self.player2_hits)):
                    for j in range(0 , len(Self.player2_hits[0])):
                        file.write(str(Self.player2_hits[i][j]))
                file.write("/")

                ##Save The Player's Life
                file.write(str(Self.player2life) + "/")

                file.write(str(Self.player2_Carrierlife) + "/")
                file.write(str(Self.player2_Battleshiplife) + "/")
                file.write(str(Self.player2_Cruiserlife) + "/")
                file.write(str(Self.player2_Submarinelife) + "/")
                file.write(str(Self.player2_Destroyerlife) + "/")

                ##Save Player 1 name and password
                file.write(str(Self.P1name) + "/" + str(Self.P1password)+"/")
                ##Save Player 2 name and password
                file.write(str(Self.P2name) + "/" + str(Self.P2password))
                

                
            

        else:
            tkinter.messagebox.showerror("Error Saving" , "Cannot Save")
            

    def showHelp(Self):

        if Self.Stage == 1:
            helptext = "This is the main menu choose wether to:\nStart a single player game\nStart a 2 player game\nContinue a saved game"
        elif Self.Stage == 2:
            helptext= "Place your ship the coordinate is for the first coordinate of the ship\nCarrier has 5 lifes\nBattleship has 4 lifes\nCruiser has 3 lifes\nSubmarine has 3 lifes \nDestroyer has 2 lifes"
        else:
            helptext = "Choose a coordinate to hit\nYou can save the game by choosing File -> Save and save the file as a txt"

        tkinter.messagebox.showinfo("Help" , helptext)
        
    def playSFX(Self):

        if not Self.SFX:
            Self.SFX = True
            pygame.mixer.music.play(-1)
            
        else:
            Self.SFX = False
            pygame.mixer.music.stop()

    ##Go to main menu
    def sMainMenu(Self):

        Self.GameFrame.pack_forget()
        Self.canSave = False
        Self.canOpen = True
        Self.MainMenu.pack()
        Self.Stage = 1

    ##Start Game Mode
    def start(Self):

        Self.canOpen = False
        Self.Stage = 2
        
        ##Single Player
        if Self.nbPlayers.get() == 1:
            
            Self.MainMenu.pack_forget()
            Self.GameFrame = Frame(Self.Window)
            Self.GameFrame.pack()

            ##Reset the hits and ships and life
            Self.player1life = 17
            Self.player1_Carrierlife = 5
            Self.player1_Battleshiplife = 4
            Self.player1_Cruiserlife = 3
            Self.player1_Submarinelife = 3
            Self.player1_Destroyerlife = 2

            Self.computerlife = 17
            Self.computer_Carrierlife = 5
            Self.computer_Battleshiplife = 4
            Self.computer_Cruiserlife = 3
            Self.computer_Submarinelife = 3
            Self.computer_Destroyerlife = 2

            
            for i in range(0 , 10):
                for j in range(0 , 10):
                    Self.player1_ship[i][j] = 0
                    Self.computer_ship[i][j] = 0
                    Self.player1_hits[i][j] = 0
                    Self.computer_hits[i][j] = 0

            Self.StartSinglePlayer()

        ##Two Player
        elif Self.nbPlayers.get() == 2:
            
            Self.MainMenu.pack_forget()
            Self.GameFrame = Frame(Self.Window)
            Self.GameFrame.pack()

            ##Reset the hits and ships and life
            Self.player1life = 17
            Self.player1_Carrierlife = 5
            Self.player1_Battleshiplife = 4
            Self.player1_Cruiserlife = 3
            Self.player1_Submarinelife = 3
            Self.player1_Destroyerlife = 2

            Self.player2life = 17
            Self.player2_Carrierlife = 5
            Self.player2_Battleshiplife = 4
            Self.player2_Cruiserlife = 3
            Self.player2_Submarinelife = 3
            Self.player2_Destroyerlife = 2
            
            for i in range(0 , 10):
                for j in range(0 , 10):
                    Self.player1_ship[i][j] = 0
                    Self.player2_hits[i][j] = 0
                    Self.player1_hits[i][j] = 0
                    Self.player2_hits[i][j] = 0

            Self.P1name = ""
            Self.P1password = ""

            Self.P2name = ""
            Self.P2password = ""

            Self.StartMultiPlayer()

        ##Invalid Game Mode
        else:
            
            tkinter.messagebox.showerror("Invalid Game Mode" , "No Game Mode Selected")
            Self.canOpen = True
            Self.Stage = 1

    ##Start Single Player Mode
    def StartSinglePlayer(Self):

        Self.PlayerFrame = Frame(Self.GameFrame)
        Self.PlayerFrame.pack()

        Self.PlayerShips = Frame(Self.PlayerFrame)
        Self.PlayerShips.pack()

        label = Label(Self.PlayerShips , text = "Player Ships")
        label.grid(row = 0 , column = 0)
        ##Place the column coordinates
        for i in range(1 , 11):

            label = Label(Self.PlayerShips , text = str(i))
            label.grid(row = 1 , column = i + 1)

        ##Place the row coordinates
        lrow = 1
        for i in range(ord("A") , (ord("A") + 10)):

            label = Label(Self.PlayerShips , text = chr(i))
            label.grid(row = lrow + 1 , column = 1)
            lrow += 1

        for i in range(0 , len(Self.player1_ship)):
            for j in range(0 , len(Self.player1_ship[0])):
                label = Label(Self.PlayerShips , text = " ")
                label.grid(row = i + 2 , column = j + 2)

        Self.ShipsFrame = Frame(Self.PlayerFrame)
        Self.ShipsFrame.pack()
        Self.PlacedShips = []
        for i in range(0 , len(Self.Ships)):
            Self.PlacedShips.append(Self.Ships[i])
        Self.ShipSelection = Combobox(Self.ShipsFrame , values = Self.PlacedShips)
        Self.ShipSelection.set("Select Ship")
        Self.ShipSelection.grid(row = 1 , column = 1)

        Self.Selectbtn = Button(Self.ShipsFrame , text = "Select" , command = Self.getship)
        Self.Selectbtn.grid(row = 2 , column = 0)

    ##Get Ship
    def getship(Self):

        ##Get Ship and remove it from the combobox
        Ship = Self.ShipSelection.get()

        ##Verify that a ship was selected
        if Ship == "Select Ship" or not Ship in Self.Ships:
            tkinter.messagebox.showerror("No Ship Selected" , "Please A Select Ship")

        else:
            Self.PlacedShips.remove(Ship)

            Self.ShipsFrame.pack_forget()

            if Ship == "Carrier":

                Self.CurrentShip = (Ship , 5)

            elif Ship == "Battleship":

                Self.CurrentShip = (Ship , 4)

            elif Ship == "Cruiser":

                Self.CurrentShip = (Ship , 3)

            elif Ship == "Submarine":

                Self.CurrentShip = (Ship , 3)

            else:

                Self.CurrentShip = (Ship , 2)

            
            Self.GetCoordinates()

            ##Create a new combobox without the selected ship
            Self.ShipSelection = Combobox(Self.ShipsFrame , values = Self.PlacedShips)
            Self.ShipSelection.set("Select Ship")
            Self.ShipSelection.grid(row = 1 , column = 1)


    def GetCoordinates(Self):

        Self.positionFrame = Frame(Self.PlayerFrame)
        Self.positionFrame.pack()

        ##Row Entry
        Self.rowposition = StringVar()
        Self.rowLabel = Label(Self.positionFrame , text = "Row:")
        Self.rowEntry = Entry(Self.positionFrame , textvariable = Self.rowposition)

        ##Column Entry
        Self.columnposition = StringVar()
        Self.columnLabel = Label(Self.positionFrame , text = "Column:")
        Self.columnEntry = Entry(Self.positionFrame , textvariable = Self.columnposition)

        ##Get Button
        Self.getbtn = Button(Self.positionFrame , text = "Enter" , command = Self.PlaceShip)

        ##Orientation Combo Box
        Self.Orientation = Combobox(Self.positionFrame , values = Self.Orient)
        Self.Orientation.set("Choose Orientation")
        
        ##Position Widgets
        Self.rowLabel.grid(row = 0 , column = 0)
        Self.rowEntry.grid(row = 0 , column = 1)
        Self.columnLabel.grid(row = 0 , column = 2)
        Self.columnEntry.grid(row = 0 , column = 3)
        Self.Orientation.grid(row = 0 , column = 4)
        Self.getbtn.grid(row = 1 , column = 2)


    def PlaceShip(Self):

        ##Get the orientation
        Self.ShipOrientation = Self.Orientation.get()
        ValidOrientation = True
        if Self.ShipOrientation == "Choose Orientation" or not Self.ShipOrientation in Self.Orient:
            ValidOrientation = False
            tkinter.messagebox.showerror("No Orientation Selected" , "Please Select An Orientation")
        
        ##Get the row value
        ValidRow = True
        Self.row = Self.rowEntry.get()

        ##Verify only one letter is entered
        if not len(Self.row) == 1:
            if len(Self.row) > 1:
                tkinter.messagebox.showerror("Wrong Entry" , "Please Enter Only One Letter")
                ValidRow = False
            else:
                tkinter.messagebox.showerror("No Entry" , "Please Enter A Letter")
                ValidRow = False

        else:
            if Self.row.isupper():
                
                Self.row = (ord(Self.row) - ord("A"))

            else:

                Self.row = (ord(Self.row) - ord("a"))

            
            if Self.ShipOrientation == "Vertical":
                if Self.row < 0 or Self.row + Self.CurrentShip[1] > (len(Self.player1_ship)):
                    tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                    ValidRow = False
            else:
                if Self.row < 0 or Self.row > (len(Self.player1_ship) - 1):
                    tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                    ValidRow = False

        ##Get the column value
        ValidColumn = True
        Self.column = Self.columnEntry.get()

        ##Verify the entry
        if len(Self.column) == 0:
            tkinter.messagebox.showerror("No Entry" , "Please Enter A Number")
        else:
            
            try:
                
                Self.column = (int(Self.column) - 1)

            except ValueError:

                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False

            if ValidColumn:
                if Self.ShipOrientation == "Horizontal":
                    if Self.column < 0 or Self.column + Self.CurrentShip[1] > (len(Self.player1_ship)):
                        tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                        ValidColumn = False
                else:
                    if Self.column < 0 or Self.column > (len(Self.player1_ship) - 1):
                        tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                        ValidColumn = False

        ##Places The Ship
        if ValidOrientation:
            if ValidColumn and ValidRow:
                if not Self.ShipPositionCheck():

                    ##Vertical Orientation
                    if Self.ShipOrientation == "Vertical":
                        if Self.CurrentShip[0] == "Carrier":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 2
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)
                                
                                                        
                                
                        elif Self.CurrentShip[0] == "Battleship":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 3
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)
                                

                        elif Self.CurrentShip[0] == "Cruiser":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 4
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        elif Self.CurrentShip[0] == "Submarine":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 5
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        else:
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 6
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                    ##Horizontal Orientation
                    else:
                        if Self.CurrentShip[0] == "Carrier":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 2
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                                
                        elif Self.CurrentShip[0] == "Battleship":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 3
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        elif Self.CurrentShip[0] == "Cruiser":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 4
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        elif Self.CurrentShip[0] == "Submarine":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 5
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                                
                        else:
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 6
                                label = Label(Self.PlayerShips , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                                        
                    Self.positionFrame.pack_forget()
                    if len(Self.PlacedShips) > 0:
                        Self.ShipsFrame.pack()
                        

                    else:

                        Self.StartSingleBattle()
                    
    ##Check if the positions are free
    def ShipPositionCheck(Self):

        status = False

        if Self.ShipOrientation == "Vertical":
            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                if not Self.player1_ship[i][Self.column] == 0:
                    status = True

        else:
            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                if not Self.player1_ship[Self.row][i] == 0:
                    status = True

        if status:
            tkinter.messagebox.showerror("Invalid Position" , "Ship Is Colliding With Another Ship")
        
        return status

    def StartSingleBattle(Self):

        Self.PlayerHitsFrame = Frame(Self.PlayerFrame)
        Self.PlayerHitsFrame.pack()
        
        label = Label(Self.PlayerHitsFrame , text = "Player Hits")
        label.grid( row = 0 , column = 0)
        ##Place the column coordinates
        for i in range(1 , 11):

            label = Label(Self.PlayerHitsFrame , text = str(i))
            label.grid(row = 1 , column = i + 1)

        ##Place the row coordinates
        lrow = 1
        for i in range(ord("A") , (ord("A") + 10)):

            label = Label(Self.PlayerHitsFrame , text = chr(i))
            label.grid(row = lrow + 1 , column = 1)
            lrow += 1

        for i in range(0 , len(Self.player1_hits)):
            for j in range(0 , len(Self.player1_hits[0])):
                label = Label(Self.PlayerHitsFrame , text = " ")
                label.grid(row = i + 2 , column = j + 2)

        Self.PlaceComputerShips()

        Self.canSave = True
        Self.Stage = 3

        ##Enter Hit Coordinates

        Self.rowcoordinate = Label(Self.PlayerFrame , text = "Row")
        Self.rowcoordinate.pack()

        Self.rowhit = StringVar()
        Self.rowentry = Entry(Self.PlayerFrame , textvariable = Self.rowhit)
        Self.rowentry.pack()

        Self.columncoordinate = Label(Self.PlayerFrame , text = "Column")
        Self.columncoordinate.pack()

        Self.columnhit = StringVar()
        Self.columnentry = Entry(Self.PlayerFrame , textvariable = Self.columnhit)
        Self.columnentry.pack()

        Self.hitbutton = Button(Self.PlayerFrame , text = "HIT!" , command = Self.playerhit)
        Self.hitbutton.pack()

    ##Hit Check
    def playerhit(Self):

        ##Get the row value
        ValidRow = True
        Self.row = Self.rowhit.get()

        ##Verify only one letter is entered
        if not len(Self.row) == 1:
            if len(Self.row) > 1:
                tkinter.messagebox.showerror("Wrong Entry" , "Please Enter Only One Letter")
                ValidRow = False
            else:
                tkinter.messagebox.showerror("No Entry" , "Please Enter A Letter")
                ValidRow = False

        else:
            if Self.row.isupper():
                
                Self.row = (ord(Self.row) - ord("A"))

            else:

                Self.row = (ord(Self.row) - ord("a"))


            ##Check that row ranges from A to J
            if Self.row <0 or Self.row > (len(Self.computer_ship) - 1):
                tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                ValidRow = False

        ##Get the column value
        ValidColumn = True
        Self.column = Self.columnhit.get()

        ##Verify the entry
        if len(Self.column) == 0:
            tkinter.messagebox.showerror("No Entry" , "Please Enter A Number")
            ValidColumn = False

        else:
            
            try:
                
                Self.column = (int(Self.column) - 1)

            except ValueError:

                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False
                

        ##Check Column Is Valid
        if ValidColumn:
            if Self.column <0 or Self.column > (len(Self.computer_ship) - 1):
                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False

        UnhitCoordinate = True
        Hit = True
        ComputerHit = True

        ##Check Hit
        if ValidColumn:
            if ValidRow:
                if not Self.player1_hits[Self.row][Self.column] == 0:
                    UnhitCoordinate = False
                    tkinter.messagebox.showerror("Hit Coordinate" , "This Coordinate Has Already Been Hit")

                if UnhitCoordinate:    
                    if Self.computer_ship[Self.row][Self.column] > 1:
                        
                        Self.player1_hits[Self.row][Self.column] = 1
                        label = Label(Self.PlayerHitsFrame , text = "X")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.hit_sound)

                        tkinter.messagebox.showinfo("Hit Result" , "Hit")
                        Self.computerlife -= 1
                        Hit = True

                        ##Check if ship is destroyed
                        if Self.computer_ship[Self.row][Self.column] == 2:
                            Self.computer_Carrierlife -= 1
                            if Self.computer_Carrierlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Carrier Destroyed")

                        elif Self.computer_ship[Self.row][Self.column] == 3:
                            Self.computer_Battleshiplife -= 1
                            if Self.computer_Battleshiplife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Battleship Destroyed")

                        elif Self.computer_ship[Self.row][Self.column] == 4:
                            Self.computer_Cruiserlife -= 1
                            if Self.computer_Cruiserlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Cruiser Destroyed")

                        elif Self.computer_ship[Self.row][Self.column] == 5:
                            Self.computer_Submarinelife -= 1
                            if Self.computer_Submarinelife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Submarine Destroyed")

                        else:
                            Self.computer_Destroyerlife -= 1
                            if Self.computer_Destroyerlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Destroyer Destroyed")

                        Self.computer_ship[Self.row][Self.column] = 1
                        

                    else:

                        Self.player1_hits[Self.row][Self.column] = 2
                        label = Label(Self.PlayerHitsFrame , text = "O")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.miss_sound)
                            
                        tkinter.messagebox.showinfo("Hit Result" , "Miss")
                        Hit = False

            ##Computer Hit
            if not Hit:

                while ComputerHit:
                    column = random.randint(0 , 9)
                    row = random.randint(0 , 9)

                    while not Self.computer_hits[row][column] == 0:
                        column = random.randint(0 , 9)
                        row = random.randint(0 , 9)
                    
                    if Self.player1_ship[row][column] > 1:
                        
                        Self.computer_hits[row][column] = 1

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.hit_sound)
                            
                        tkinter.messagebox.showwarning("Computer Hit Result" , "Hit At: " + chr(ord("A") + row) + str(int(column + 1)))
                        label = Label(Self.PlayerShips , text = "*")
                        label.grid(row = row + 2 , column = column + 2)
                        Self.player1life -= 1
                        
                        ##Check if a ship has been destroyed
                        if Self.player1_ship[row][column] == 2:
                            Self.player1_Carrierlife -= 1
                            if Self.player1_Carrierlife == 0:
                                tkinter.messagebox.showwarning("Destroyed Ship" , "Carrier Destroyed")

                        elif Self.player1_ship[row][column] == 3:
                            Self.player1_Battleshiplife -= 1
                            if Self.player1_Battleshiplife == 0:
                                tkinter.messagebox.showwarning("Destroyed Ship" , "Battleship Destroyed")

                        elif Self.player1_ship[row][column] == 4:
                            Self.player1_Cruiserlife -= 1
                            if Self.player1_Cruiserlife == 0:
                                tkinter.messagebox.showwarning("Destroyed Ship" , "Cruiser Destroyed")

                        elif Self.player1_ship[row][column] == 5:
                            Self.player1_Submarinelife -= 1
                            if Self.player1_Submarinelife == 0:
                                tkinter.messagebox.showwarning("Destroyed Ship" , "Submarine Destroyed")
                        else:
                            Self.player1_Destroyerlife -= 1
                            if Self.player1_Destroyerlife == 0:
                                tkinter.messagebox.showwarning("Destroyed Ship" , "Destroyer Destroyed")

                        Self.player1_ship[row][column] = 1
                            
                    else:
                        Self.computer_hits[row][column] = 2
                        Self.player1_ship[row][column] = 9

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.miss_sound)
                            
                        tkinter.messagebox.showwarning("Computer Hit Result" , "Miss At: " + chr(ord("A") + row) + str(int(column + 1)))
                        label = Label(Self.PlayerShips , text = "O")
                        label.grid(row = row + 2 , column = column + 2)
                        ComputerHit = False
                    
                    
        ##End of Game
        if Self.computerlife == 0:
            tkinter.messagebox.showinfo("Game Over" , "You Won")
            Self.sMainMenu()

        if Self.player1life == 0:
            tkinter.messagebox.showinfo("Game Over" , "You Lost")
            Self.sMainMenu()

    ##Computer Functions

    ##Place Computer Ships
    def PlaceComputerShips(Self):

        ##Carrier
        Self.Computershipsize = 5
        Self.ComputerShipOrientation = random.randint(1 , 2)
        Self.computerrow = 0
        Self.computercolumn = 0

        if Self.ComputerShipOrientation == 1:

            Self.computercolumn = random.randint(0 , 9)
            Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , 9)
                Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            for i in range(Self.computerrow , Self.Computershipsize + Self.computerrow):
                Self.computer_ship[i][Self.computercolumn] = 2

        else:

            Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
            Self.computerrow = random.randint(0 , 9)

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
                Self.computerrow = random.randint(0 , 9)

            for i in range(Self.computercolumn , Self.Computershipsize + Self.computercolumn):
                Self.computer_ship[Self.computerrow][i] = 2

        ##Battleship
        Self.Computershipsize = 4
        Self.ComputerShipOrientation = random.randint(1 , 2)
        Self.computerrow = 0
        Self.computercolumn = 0

        if Self.ComputerShipOrientation == 1:

            Self.computercolumn = random.randint(0 , 9)
            Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , 9)
                Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            for i in range(Self.computerrow , Self.Computershipsize + Self.computerrow):
                Self.computer_ship[i][Self.computercolumn] = 3

        else:

            Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
            Self.computerrow = random.randint(0 , 9)

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
                Self.computerrow = random.randint(0 , 9)

            for i in range(Self.computercolumn , Self.Computershipsize + Self.computercolumn):
                Self.computer_ship[Self.computerrow][i] = 3

        ##Cruiser
        Self.Computershipsize = 3
        Self.ComputerShipOrientation = random.randint(1 , 2)
        Self.computerrow = 0
        Self.computercolumn = 0

        if Self.ComputerShipOrientation == 1:

            Self.computercolumn = random.randint(0 , 9)
            Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , 9)
                Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            for i in range(Self.computerrow , Self.Computershipsize + Self.computerrow):
                Self.computer_ship[i][Self.computercolumn] = 4

        else:

            Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
            Self.computerrow = random.randint(0 , 9)

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
                Self.computerrow = random.randint(0 , 9)

            for i in range(Self.computercolumn , Self.Computershipsize + Self.computercolumn):
                Self.computer_ship[Self.computerrow][i] = 4

        ##Submarine
        Self.Computershipsize = 3
        Self.ComputerShipOrientation = random.randint(1 , 2)
        Self.computerrow = 0
        Self.computercolumn = 0

        if Self.ComputerShipOrientation == 1:

            Self.computercolumn = random.randint(0 , 9)
            Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , 9)
                Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            for i in range(Self.computerrow , Self.Computershipsize + Self.computerrow):
                Self.computer_ship[i][Self.computercolumn] = 5

        else:

            Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
            Self.computerrow = random.randint(0 , 9)

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
                Self.computerrow = random.randint(0 , 9)

            for i in range(Self.computercolumn , Self.Computershipsize + Self.computercolumn):
                Self.computer_ship[Self.computerrow][i] = 5

        ##Destroyer
        Self.Computershipsize = 2
        Self.ComputerShipOrientation = random.randint(1 , 2)
        Self.computerrow = 0
        Self.computercolumn = 0

        if Self.ComputerShipOrientation == 1:

            Self.computercolumn = random.randint(0 , 9)
            Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , 9)
                Self.computerrow = random.randint(0 , (10 - Self.Computershipsize))

            for i in range(Self.computerrow , Self.Computershipsize + Self.computerrow):
                Self.computer_ship[i][Self.computercolumn] = 6

        else:

            Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
            Self.computerrow = random.randint(0 , 9)

            while Self.ComputerCheckPosition():

                Self.computercolumn = random.randint(0 , (10 - Self.Computershipsize))
                Self.computerrow = random.randint(0 , 9)

            for i in range(Self.computercolumn , Self.Computershipsize + Self.computercolumn):
                Self.computer_ship[Self.computerrow][i] = 6

    def ComputerCheckPosition(Self):

        ##Check if space available for ship
        status = False
        if Self.ComputerShipOrientation == 1:
            for i in range(Self.computerrow , Self.Computershipsize + Self.computerrow):
                if not Self.computer_ship[i][Self.computercolumn] == 0:
                    status = True

        else:
            for i in range(Self.computercolumn , Self.Computershipsize + Self.computercolumn):
                if not Self.computer_ship[Self.computerrow][i] == 0:
                    status = True

        return status

    ##Multiplayer
    def StartMultiPlayer(Self):

        ##Ask Player1 Name And Password:
        InvalidName = True

        while InvalidName:
            try:
                Self.P1name = tkinter.simpledialog.askstring("P1 Name" , "Enter Your Name")
                while len(Self.P1name) < 1:
                    Self.P1name = tkinter.simpledialog.askstring("P1 Name" , "Enter Your Name")

                InvalidName = False
            except:
                tkinter.messagebox.showerror("Invalid Name" , "No Name Entered")

        Self.Checkpass = 1
        invalidpass = True

        while invalidpass:

            Self.P1password = tkinter.simpledialog.askstring("Enter Password" , "Your password must follow these conditions:\n1- 1 Letter between [a-z].\2- 1 Letter between [A-Z].\n3- 1 Number between [0-9].\n4- 1 Special character from [$#@?*].\n5- Minimum length 6 characters.\n6- Maximum length 16 characters.")
            try:

                while len(Self.P1password) < 6 or len(Self.P1password) > 16:

                    if len(Self.P1password) < 6:
                        tkinter.messagebox.showerror("Invalid Password" , "Password is too short")
                        Self.P1password = tkinter.simpledialog.askstring("Enter Password" , "At least 6 characters long")

                    else:
                        tkinter.messagebox.showerror("Invalid Password" , "Password is too long")
                        Self.P1password = tkinter.simpledialog.askstring("Enter Password" , "Maximum 16 characters long")

                invalidpass = Self.CheckPassword()
                        

            except TypeError:
                tkinter.messagebox.showerror("Invalid Password" , "No Password Entered")

        Self.Player1Frame = Frame(Self.GameFrame)
        Self.Player1Frame.pack()

        Self.Player1Ships = Frame(Self.Player1Frame)
        Self.Player1Ships.pack()

        label = Label(Self.Player1Ships , text = Self.P1name + "'s Ships:")
        label.grid(row = 0 , column = 0)
        ##Place the column coordinates
        for i in range(1 , 11):

            label = Label(Self.Player1Ships , text = str(i))
            label.grid(row = 1 , column = i + 1)

        ##Place the row coordinates
        lrow = 1
        for i in range(ord("A") , (ord("A") + 10)):

            label = Label(Self.Player1Ships , text = chr(i))
            label.grid(row = lrow + 1 , column = 1)
            lrow += 1

        for i in range(0 , len(Self.player1_ship)):
            for j in range(0 , len(Self.player1_ship[0])):
                label = Label(Self.Player1Ships , text = " ")
                label.grid(row = i + 2 , column = j + 2)

        Self.P1ShipsFrame = Frame(Self.Player1Frame)
        Self.P1ShipsFrame.pack()
        Self.P1PlacedShips = []
        for i in range(0 , len(Self.Ships)):
            Self.P1PlacedShips.append(Self.Ships[i])
        Self.P1ShipSelection = Combobox(Self.P1ShipsFrame , values = Self.P1PlacedShips)
        Self.P1ShipSelection.set("Select Ship")
        Self.P1ShipSelection.grid(row = 1 , column = 1)

        Self.P1Selectbtn = Button(Self.P1ShipsFrame , text = "Select" , command = Self.P1getship)
        Self.P1Selectbtn.grid(row = 2 , column = 0)

    def P1getship(Self):

        ##Get Ship and remove it from the combobox
        Ship = Self.P1ShipSelection.get()

        ##Verify that a ship was selected
        if Ship == "Select Ship" or not Ship in Self.Ships:
            tkinter.messagebox.showerror("No Ship Selected" , "Please A Select Ship")

        else:
            Self.P1PlacedShips.remove(Ship)

            Self.P1ShipsFrame.pack_forget()

            if Ship == "Carrier":

                Self.CurrentShip = (Ship , 5)

            elif Ship == "Battleship":

                Self.CurrentShip = (Ship , 4)

            elif Ship == "Cruiser":

                Self.CurrentShip = (Ship , 3)

            elif Ship == "Submarine":

                Self.CurrentShip = (Ship , 3)

            else:

                Self.CurrentShip = (Ship , 2)

            
            Self.P1GetCoordinates()

            ##Create a new combobox without the selected ship
            Self.P1ShipSelection = Combobox(Self.P1ShipsFrame , values = Self.P1PlacedShips)
            Self.P1ShipSelection.set("Select Ship")
            Self.P1ShipSelection.grid(row = 1 , column = 1)


    def P1GetCoordinates(Self):

        Self.P1positionFrame = Frame(Self.Player1Frame)
        Self.P1positionFrame.pack()

        ##Row Entry
        Self.rowposition = StringVar()
        Self.rowLabel = Label(Self.P1positionFrame , text = "Row:")
        Self.rowEntry = Entry(Self.P1positionFrame , textvariable = Self.rowposition)

        ##Column Entry
        Self.columnposition = StringVar()
        Self.columnLabel = Label(Self.P1positionFrame , text = "Column:")
        Self.columnEntry = Entry(Self.P1positionFrame , textvariable = Self.columnposition)

        ##Get Button
        Self.getbtn = Button(Self.P1positionFrame , text = "Enter" , command = Self.P1PlaceShip)

        ##Orientation Combo Box
        Self.Orientation = Combobox(Self.P1positionFrame , values = Self.Orient)
        Self.Orientation.set("Choose Orientation")
        
        ##Position Widgets
        Self.rowLabel.grid(row = 0 , column = 0)
        Self.rowEntry.grid(row = 0 , column = 1)
        Self.columnLabel.grid(row = 0 , column = 2)
        Self.columnEntry.grid(row = 0 , column = 3)
        Self.Orientation.grid(row = 0 , column = 4)
        Self.getbtn.grid(row = 1 , column = 2)

    def P1PlaceShip(Self):

        ##Get the orientation
        Self.ShipOrientation = Self.Orientation.get()
        ValidOrientation = True
        if Self.ShipOrientation == "Choose Orientation" or not Self.ShipOrientation in Self.Orient:
            ValidOrientation = False
            tkinter.messagebox.showerror("No Orientation Selected" , "Please Select An Orientation")
        
        ##Get the row value
        ValidRow = True
        Self.row = Self.rowEntry.get()

        ##Verify only one letter is entered
        if not len(Self.row) == 1:
            if len(Self.row) > 1:
                tkinter.messagebox.showerror("Wrong Entry" , "Please Enter Only One Letter")
                ValidRow = False
            else:
                tkinter.messagebox.showerror("No Entry" , "Please Enter A Letter")
                ValidRow = False

        else:
            if Self.row.isupper():
                
                Self.row = (ord(Self.row) - ord("A"))

            else:

                Self.row = (ord(Self.row) - ord("a"))

            
            if Self.ShipOrientation == "Vertical":
                if Self.row < 0 or Self.row + Self.CurrentShip[1] > (len(Self.player1_ship)):
                    tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                    ValidRow = False
            else:
                if Self.row < 0 or Self.row > (len(Self.player1_ship) - 1):
                    tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                    ValidRow = False

        ##Get the column value
        ValidColumn = True
        Self.column = Self.columnEntry.get()

        ##Verify the entry
        if len(Self.column) == 0:
            tkinter.messagebox.showerror("No Entry" , "Please Enter A Number")
        else:
            
            try:
                
                Self.column = (int(Self.column) - 1)

            except ValueError:

                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False

            if ValidColumn:
                if Self.ShipOrientation == "Horizontal":
                    if Self.column < 0 or Self.column + Self.CurrentShip[1] > (len(Self.player1_ship)):
                        tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                        ValidColumn = False
                else:
                    if Self.column < 0 or Self.column > (len(Self.player1_ship) - 1):
                        tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                        ValidColumn = False

        ##Places The Ship
        if ValidOrientation:
            if ValidColumn and ValidRow:
                if not Self.P1ShipPositionCheck():

                    ##Vertical Orientation
                    if Self.ShipOrientation == "Vertical":
                        if Self.CurrentShip[0] == "Carrier":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 2
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)
                                
                        elif Self.CurrentShip[0] == "Battleship":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 3
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        elif Self.CurrentShip[0] == "Cruiser":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 4
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        elif Self.CurrentShip[0] == "Submarine":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 5
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        else:
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player1_ship[i][Self.column] = 6
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                    ##Horizontal Orientation
                    else:
                        if Self.CurrentShip[0] == "Carrier":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 2
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                                
                        elif Self.CurrentShip[0] == "Battleship":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 3
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        elif Self.CurrentShip[0] == "Cruiser":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 4
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        elif Self.CurrentShip[0] == "Submarine":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 5
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        else:
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player1_ship[Self.row][i] = 6
                                label = Label(Self.Player1Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                    
                    Self.P1positionFrame.pack_forget()

                    if len(Self.P1PlacedShips) > 0:
                            Self.P1ShipsFrame.pack()       

                    else:

                        Self.Player1Frame.pack_forget()
                        Self.P2Start()

    def P1ShipPositionCheck(Self):

        status = False

        if Self.ShipOrientation == "Vertical":
            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                if not Self.player1_ship[i][Self.column] == 0:
                    status = True

        else:
            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                if not Self.player1_ship[Self.row][i] == 0:
                    status = True

        if status:
            tkinter.messagebox.showerror("Invalid Position" , "Ship Is Colliding With Another Ship")
        
        return status

    def P2Start(Self):

        ##Ask Player2 Name And Password:
        InvalidName = True

        while InvalidName:
            try:
                Self.P2name = tkinter.simpledialog.askstring("P2 Name" , "Enter Your Name")
                while len(Self.P2name) < 1:
                    Self.P2name = tkinter.simpledialog.askstring("P2 Name" , "Enter Your Name")

                InvalidName = False
            except:
                tkinter.messagebox.showerror("Invalid Name" , "No Name Entered")

        Self.Checkpass = 2
        invalidpass = True

        while invalidpass:

            Self.P2password = tkinter.simpledialog.askstring("Enter Password" , "Your password must follow these conditions:\n1- 1 Letter between [a-z].\2- 1 Letter between [A-Z].\n3- 1 Number between [0-9].\n4- 1 Special character from [$#@?*].\n5- Minimum length 6 characters.\n6- Maximum length 16 characters.")
            try:

                while len(Self.P2password) < 6 or len(Self.P2password) > 16:

                    if len(Self.P2password) < 6:
                        tkinter.messagebox.showerror("Invalid Password" , "Password is too short")
                        Self.P2password = tkinter.simpledialog.askstring("Enter Password" , "At least 6 characters long")

                    else:
                        tkinter.messagebox.showerror("Invalid Password" , "Password is too long")
                        Self.P2password = tkinter.simpledialog.askstring("Enter Password" , "Maximum 16 characters long")

                invalidpass = Self.CheckPassword()
                        

            except TypeError:
                tkinter.messagebox.showerror("Invalid Password" , "No Password Entered")

        Self.Player2Frame = Frame(Self.GameFrame)
        Self.Player2Frame.pack()

        Self.Player2Ships = Frame(Self.Player2Frame)
        Self.Player2Ships.pack()

        label = Label(Self.Player2Ships , text = Self.P2name + "'s Ships :")
        label.grid(row = 0 , column = 0)
        ##Place the column coordinates
        for i in range(1 , 11):

            label = Label(Self.Player2Ships , text = str(i))
            label.grid(row = 1 , column = i + 1)

        ##Place the row coordinates
        lrow = 1
        for i in range(ord("A") , (ord("A") + 10)):

            label = Label(Self.Player2Ships , text = chr(i))
            label.grid(row = lrow + 1 , column = 1)
            lrow += 1

        for i in range(0 , len(Self.player2_ship)):
            for j in range(0 , len(Self.player2_ship[0])):
                label = Label(Self.Player2Ships , text = " ")
                label.grid(row = i + 2 , column = j + 2)

        Self.P2ShipsFrame = Frame(Self.Player2Frame)
        Self.P2ShipsFrame.pack()
        Self.P2PlacedShips = []
        for i in range(0 , len(Self.Ships)):
            Self.P2PlacedShips.append(Self.Ships[i])
        Self.P2ShipSelection = Combobox(Self.P2ShipsFrame , values = Self.P2PlacedShips)
        Self.P2ShipSelection.set("Select Ship")
        Self.P2ShipSelection.grid(row = 1 , column = 1)

        Self.P2Selectbtn = Button(Self.P2ShipsFrame , text = "Select" , command = Self.P2getship)
        Self.P2Selectbtn.grid(row = 2 , column = 0)

    def P2getship(Self):

        ##Get Ship and remove it from the combobox
        Ship = Self.P2ShipSelection.get()

        ##Verify that a ship was selected
        if Ship == "Select Ship" or not Ship in Self.Ships:
            tkinter.messagebox.showerror("No Ship Selected" , "Please A Select Ship")

        else:
            Self.P2PlacedShips.remove(Ship)

            Self.P2ShipsFrame.pack_forget()

            if Ship == "Carrier":

                Self.CurrentShip = (Ship , 5)

            elif Ship == "Battleship":

                Self.CurrentShip = (Ship , 4)

            elif Ship == "Cruiser":

                Self.CurrentShip = (Ship , 3)

            elif Ship == "Submarine":

                Self.CurrentShip = (Ship , 3)

            else:

                Self.CurrentShip = (Ship , 2)

            
            Self.P2GetCoordinates()

            ##Create a new combobox without the selected ship
            Self.P2ShipSelection = Combobox(Self.P2ShipsFrame , values = Self.P2PlacedShips)
            Self.P2ShipSelection.set("Select Ship")
            Self.P2ShipSelection.grid(row = 1 , column = 1)

    def P2GetCoordinates(Self):

        Self.P2positionFrame = Frame(Self.Player2Frame)
        Self.P2positionFrame.pack()

        ##Row Entry
        Self.rowposition = StringVar()
        Self.rowLabel = Label(Self.P2positionFrame , text = "Row:")
        Self.rowEntry = Entry(Self.P2positionFrame , textvariable = Self.rowposition)

        ##Column Entry
        Self.columnposition = StringVar()
        Self.columnLabel = Label(Self.P2positionFrame , text = "Column:")
        Self.columnEntry = Entry(Self.P2positionFrame , textvariable = Self.columnposition)

        ##Get Button
        Self.getbtn = Button(Self.P2positionFrame , text = "Enter" , command = Self.P2PlaceShip)

        ##Orientation Combo Box
        Self.Orientation = Combobox(Self.P2positionFrame , values = Self.Orient)
        Self.Orientation.set("Choose Orientation")
        
        ##Position Widgets
        Self.rowLabel.grid(row = 0 , column = 0)
        Self.rowEntry.grid(row = 0 , column = 1)
        Self.columnLabel.grid(row = 0 , column = 2)
        Self.columnEntry.grid(row = 0 , column = 3)
        Self.Orientation.grid(row = 0 , column = 4)
        Self.getbtn.grid(row = 1 , column = 2)

    def P2PlaceShip(Self):

        ##Get the orientation
        Self.ShipOrientation = Self.Orientation.get()
        ValidOrientation = True
        if Self.ShipOrientation == "Choose Orientation" or not Self.ShipOrientation in Self.Orient:
            ValidOrientation = False
            tkinter.messagebox.showerror("No Orientation Selected" , "Please Select An Orientation")
        
        ##Get the row value
        ValidRow = True
        Self.row = Self.rowEntry.get()

        ##Verify only one letter is entered
        if not len(Self.row) == 1:
            if len(Self.row) > 1:
                tkinter.messagebox.showerror("Wrong Entry" , "Please Enter Only One Letter")
                ValidRow = False
            else:
                tkinter.messagebox.showerror("No Entry" , "Please Enter A Letter")
                ValidRow = False

        else:
            if Self.row.isupper():
                
                Self.row = (ord(Self.row) - ord("A"))

            else:

                Self.row = (ord(Self.row) - ord("a"))

            
            if Self.ShipOrientation == "Vertical":
                if Self.row < 0 or Self.row + Self.CurrentShip[1] > (len(Self.player2_ship)):
                    tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                    ValidRow = False
            else:
                if Self.row < 0 or Self.row > (len(Self.player2_ship) - 1):
                    tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                    ValidRow = False

        ##Get the column value
        ValidColumn = True
        Self.column = Self.columnEntry.get()

        ##Verify the entry
        if len(Self.column) == 0:
            tkinter.messagebox.showerror("No Entry" , "Please Enter A Number")
        else:
            
            try:
                
                Self.column = (int(Self.column) - 1)

            except ValueError:

                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False

            if ValidColumn:
                if Self.ShipOrientation == "Horizontal":
                    if Self.column < 0 or Self.column + Self.CurrentShip[1] > (len(Self.player2_ship)):
                        tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                        ValidColumn = False
                else:
                    if Self.column < 0 or Self.column > (len(Self.player2_ship) - 1):
                        tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                        ValidColumn = False
                    
        ##Places The Ship
        if ValidOrientation:
            if ValidColumn and ValidRow:
                if not Self.P2ShipPositionCheck():

                    ##Vertical Orientation
                    if Self.ShipOrientation == "Vertical":
                        if Self.CurrentShip[0] == "Carrier":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player2_ship[i][Self.column] = 2
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)
  
                        elif Self.CurrentShip[0] == "Battleship":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player2_ship[i][Self.column] = 3
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)  

                        elif Self.CurrentShip[0] == "Cruiser":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player2_ship[i][Self.column] = 4
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        elif Self.CurrentShip[0] == "Submarine":
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player2_ship[i][Self.column] = 5
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                        else:
                            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                                Self.player2_ship[i][Self.column] = 6
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = i + 2 , column = Self.column + 2)

                    ##Horizontal Orientation
                    else:
                        if Self.CurrentShip[0] == "Carrier":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player2_ship[Self.row][i] = 2
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                                
                        elif Self.CurrentShip[0] == "Battleship":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player2_ship[Self.row][i] = 3
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                                
                        elif Self.CurrentShip[0] == "Cruiser":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player2_ship[Self.row][i] = 4
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        elif Self.CurrentShip[0] == "Submarine":
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player2_ship[Self.row][i] = 5
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)

                        else:
                            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                                Self.player2_ship[Self.row][i] = 6
                                label = Label(Self.Player2Ships , text = "X")
                                label.grid(row = Self.row + 2 , column = i + 2)
                    
                    Self.P2positionFrame.pack_forget()
                    if len(Self.P2PlacedShips) > 0:
                        Self.P2ShipsFrame.pack()
                        
                    else:
                        Self.Player2Frame.pack_forget()
                        Self.StartMultiPlayerBattle()

    def P2ShipPositionCheck(Self):

        status = False

        if Self.ShipOrientation == "Vertical":
            for i in range(Self.row , Self.CurrentShip[1] + Self.row):
                if not Self.player2_ship[i][Self.column] == 0:
                    status = True

        else:
            for i in range(Self.column , Self.CurrentShip[1] + Self.column):
                if not Self.player2_ship[Self.row][i] == 0:
                    status = True

        if status:
            tkinter.messagebox.showerror("Invalid Position" , "Ship Is Colliding With Another Ship")
        
        return status

    def StartMultiPlayerBattle(Self):

        ##Player 1
        Self.Player1HitsFrame = Frame(Self.Player1Frame)
        Self.Player1HitsFrame.pack()
        
        label = Label(Self.Player1HitsFrame , text = Self.P1name+ "'s: Hits")
        label.grid( row = 0 , column = 0)
        ##Place the column coordinates
        for i in range(1 , 11):

            label = Label(Self.Player1HitsFrame , text = str(i))
            label.grid(row = 1 , column = i + 1)

        ##Place the row coordinates
        lrow = 1
        for i in range(ord("A") , (ord("A") + 10)):

            label = Label(Self.Player1HitsFrame , text = chr(i))
            label.grid(row = lrow + 1 , column = 1)
            lrow += 1

        for i in range(0 , len(Self.player1_hits)):
            for j in range(0 , len(Self.player1_hits[0])):
                label = Label(Self.Player1HitsFrame , text = " ")
                label.grid(row = i + 2 , column = j + 2)

        Self.canSave = True
        Self.Stage = 3

        ##Enter Hit Coordinates

        Self.rowcoordinate = Label(Self.Player1Frame , text = "Row")
        Self.rowcoordinate.pack()

        Self.P1rowhit = StringVar()
        Self.rowentry = Entry(Self.Player1Frame , textvariable = Self.P1rowhit)
        Self.rowentry.pack()

        Self.columncoordinate = Label(Self.Player1Frame , text = "Column")
        Self.columncoordinate.pack()

        Self.P1columnhit = StringVar()
        Self.columnentry = Entry(Self.Player1Frame , textvariable = Self.P1columnhit)
        Self.columnentry.pack()

        Self.hitbutton = Button(Self.Player1Frame , text = "HIT!" , command = Self.player1hit)
        Self.hitbutton.pack()

        Self.password = tkinter.simpledialog.askstring("Password" , Self.P1name + " Enter Your Password:")

        while not Self.password == Self.P1password:

            tkinter.messagebox.showerror("Wrong Password" , "Enter Your Password")
            Self.password = tkinter.simpledialog.askstring("Password" , Self.P1name + " Enter Your Password:")
            
        Self.Player1Frame.pack()

        ##Player 2
        Self.Player2HitsFrame = Frame(Self.Player2Frame)
        Self.Player2HitsFrame.pack()
        
        label = Label(Self.Player2HitsFrame , text = Self.P2name+ "'s: Hits")
        label.grid( row = 0 , column = 0)
        ##Place the column coordinates
        for i in range(1 , 11):

            label = Label(Self.Player2HitsFrame , text = str(i))
            label.grid(row = 1 , column = i + 1)

        ##Place the row coordinates
        lrow = 1
        for i in range(ord("A") , (ord("A") + 10)):

            label = Label(Self.Player2HitsFrame , text = chr(i))
            label.grid(row = lrow + 1 , column = 1)
            lrow += 1

        for i in range(0 , len(Self.player2_hits)):
            for j in range(0 , len(Self.player2_hits[0])):
                label = Label(Self.Player2HitsFrame , text = " ")
                label.grid(row = i + 2 , column = j + 2)

        ##Enter Hit Coordinates

        Self.rowcoordinate = Label(Self.Player2Frame , text = "Row")
        Self.rowcoordinate.pack()

        Self.P2rowhit = StringVar()
        Self.rowentry = Entry(Self.Player2Frame , textvariable = Self.P2rowhit)
        Self.rowentry.pack()

        Self.columncoordinate = Label(Self.Player2Frame , text = "Column")
        Self.columncoordinate.pack()

        Self.P2columnhit = StringVar()
        Self.columnentry = Entry(Self.Player2Frame , textvariable = Self.P2columnhit)
        Self.columnentry.pack()

        Self.hitbutton = Button(Self.Player2Frame , text = "HIT!" , command = Self.player2hit)
        Self.hitbutton.pack()

    def player1hit(Self):

        ##Get the row value
        ValidRow = True
        Self.row = Self.P1rowhit.get()

        ##Verify only one letter is entered
        if not len(Self.row) == 1:
            if len(Self.row) > 1:
                tkinter.messagebox.showerror("Wrong Entry" , "Please Enter Only One Letter")
                ValidRow = False
            else:
                tkinter.messagebox.showerror("No Entry" , "Please Enter A Letter")
                ValidRow = False

        else:
            if Self.row.isupper():
                
                Self.row = (ord(Self.row) - ord("A"))

            else:

                Self.row = (ord(Self.row) - ord("a"))


            ##Check that row ranges from A to J
            if Self.row <0 or Self.row > (len(Self.player2_ship) - 1):
                tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                ValidRow = False

        ##Get the column value
        ValidColumn = True
        Self.column = Self.P1columnhit.get()

        ##Verify the entry
        if len(Self.column) == 0:
            tkinter.messagebox.showerror("No Entry" , "Please Enter A Number")
            ValidColumn = False

        else:
            
            try:
                
                Self.column = (int(Self.column) - 1)

            except ValueError:

                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False
                

        ##Check Column Is Valid
        if ValidColumn:
            if Self.column <0 or Self.column > (len(Self.player2_ship) - 1):
                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False

        UnhitCoordinate = True
        Hit = True

        ##Check Hit
        if ValidColumn:
            if ValidRow:
                if not Self.player1_hits[Self.row][Self.column] == 0:
                    UnhitCoordinate = False
                    tkinter.messagebox.showerror("Hit Coordinate" , "This Coordinate Has Already Been Hit")

                if UnhitCoordinate:    
                    if Self.player2_ship[Self.row][Self.column] > 1:
                        
                        Self.player1_hits[Self.row][Self.column] = 1
                        label = Label(Self.Player1HitsFrame , text = "X")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.hit_sound)
                            
                        tkinter.messagebox.showinfo("Hit Result" , "Hit")
                        label = Label(Self.Player2Ships , text = "*")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)
                        Self.player2life -= 1
                        Hit = True

                        ##Check if ship is destroyed
                        if Self.player2_ship[Self.row][Self.column] == 2:
                            Self.player2_Carrierlife -= 1
                            if Self.player2_Carrierlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Carrier Destroyed")

                        elif Self.player2_ship[Self.row][Self.column] == 3:
                            Self.player2_Battleshiplife -= 1
                            if Self.player2_Battleshiplife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Battleship Destroyed")

                        elif Self.player2_ship[Self.row][Self.column] == 4:
                            Self.player2_Cruiserlife -= 1
                            if Self.player2_Cruiserlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Cruiser Destroyed")

                        elif Self.player2_ship[Self.row][Self.column] == 5:
                            Self.player2_Submarinelife -= 1
                            if Self.player2_Submarinelife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Submarine Destroyed")

                        else:
                            Self.player2_Destroyerlife -= 1
                            if Self.player2_Destroyerlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Destroyer Destroyed")

                        Self.player2_ship[Self.row][Self.column] = 1
                        

                    else:

                        Self.player1_hits[Self.row][Self.column] = 2
                        label = Label(Self.Player1HitsFrame , text = "O")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.miss_sound)
                            
                        tkinter.messagebox.showinfo("Hit Result" , "Miss")
                        Hit = False
                        Self.player2_ship[Self.row][Self.column] = 9
                        label = Label(Self.Player2Ships , text = "O")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

        if Self.player2life == 0:
            tkinter.messagebox.showinfo("End Of Game" , Self.P1name + " Won")
            Self.sMainMenu()

        if not Hit:
            Self.Player1Frame.pack_forget()
            Self.canSave = False

            Self.password = tkinter.simpledialog.askstring("Password" , Self.P2name + " Enter Your Password:")
            while not Self.password == Self.P2password:

                tkinter.messagebox.showerror("Wrong Password" , "Enter Your Password")
                Self.password = tkinter.simpledialog.askstring("Password" , Self.P2name + " Enter Your Password:")
                
            Self.Player2Frame.pack()


    def player2hit(Self):

        ##Get the row value
        ValidRow = True
        Self.row = Self.P2rowhit.get()

        ##Verify only one letter is entered
        if not len(Self.row) == 1:
            if len(Self.row) > 1:
                tkinter.messagebox.showerror("Wrong Entry" , "Please Enter Only One Letter")
                ValidRow = False
            else:
                tkinter.messagebox.showerror("No Entry" , "Please Enter A Letter")
                ValidRow = False

        else:
            if Self.row.isupper():
                
                Self.row = (ord(Self.row) - ord("A"))

            else:

                Self.row = (ord(Self.row) - ord("a"))


            ##Check that row ranges from A to J
            if Self.row <0 or Self.row > (len(Self.player2_ship) - 1):
                tkinter.messagebox.showerror("Invalid Row" , "Enter Valid Row")
                ValidRow = False

        ##Get the column value
        ValidColumn = True
        Self.column = Self.P2columnhit.get()

        ##Verify the entry
        if len(Self.column) == 0:
            tkinter.messagebox.showerror("No Entry" , "Please Enter A Number")
            ValidColumn = False

        else:
            
            try:
                
                Self.column = (int(Self.column) - 1)

            except ValueError:

                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False
                

        ##Check Column Is Valid
        if ValidColumn:
            if Self.column <0 or Self.column > (len(Self.player2_ship) - 1):
                tkinter.messagebox.showerror("Invalid Column" , "Enter Valid Column")
                ValidColumn = False

        UnhitCoordinate = True
        Hit = True

        ##Check Hit
        if ValidColumn:
            if ValidRow:
                if not Self.player2_hits[Self.row][Self.column] == 0:
                    UnhitCoordinate = False
                    tkinter.messagebox.showerror("Hit Coordinate" , "This Coordinate Has Already Been Hit")

                if UnhitCoordinate:    
                    if Self.player1_ship[Self.row][Self.column] > 1:
                        
                        Self.player2_hits[Self.row][Self.column] = 1
                        label = Label(Self.Player2HitsFrame , text = "X")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)
                        label = Label(Self.Player1Ships , text = "*")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.hit_sound)
                            
                        tkinter.messagebox.showinfo("Hit Result" , "Hit")
                        Self.player1life -= 1
                        Hit = True

                        ##Check if ship is destroyed
                        if Self.player1_ship[Self.row][Self.column] == 2:
                            Self.player1_Carrierlife -= 1
                            if Self.player1_Carrierlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Carrier Destroyed")

                        elif Self.player1_ship[Self.row][Self.column] == 3:
                            Self.player1_Battleshiplife -= 1
                            if Self.player1_Battleshiplife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Battleship Destroyed")

                        elif Self.player1_ship[Self.row][Self.column] == 4:
                            Self.player1_Cruiserlife -= 1
                            if Self.player1_Cruiserlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Cruiser Destroyed")

                        elif Self.player1_ship[Self.row][Self.column] == 5:
                            Self.player1_Submarinelife -= 1
                            if Self.player1_Submarinelife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Submarine Destroyed")

                        else:
                            Self.player1_Destroyerlife -= 1
                            if Self.player1_Destroyerlife == 0:
                                tkinter.messagebox.showinfo("Destroyed Ship" , "Destroyer Destroyed")

                        Self.player1_ship[Self.row][Self.column] = 1
                        

                    else:

                        Self.player2_hits[Self.row][Self.column] = 2
                        label = Label(Self.Player2HitsFrame , text = "O")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

                        ##Play Sound Effects
                        if Self.SFX:
                            
                            pygame.mixer.Sound.play(Self.miss_sound)
                            
                        tkinter.messagebox.showinfo("Hit Result" , "Miss")
                        Hit = False
                        Self.player1_ship[Self.row][Self.column] = 9
                        label = Label(Self.Player1Ships , text = "O")
                        label.grid(row = Self.row + 2 , column = Self.column + 2)

        if Self.player1life == 0:
            tkinter.messagebox.showinfo("End Of Game" , Self.P2name + " Won")
            Self.sMainMenu()

        if not Hit:

            Self.canSave = True
            Self.Player2Frame.pack_forget()

            Self.password = tkinter.simpledialog.askstring("Password" , Self.P1name + " Enter Your Password:")

            while not Self.password == Self.P1password:

                tkinter.messagebox.showerror("Wrong Password" , "Enter Your Password")
                Self.password = tkinter.simpledialog.askstring("Password" , Self.P1name + " Enter Your Password:")
            
            Self.Player1Frame.pack()


    def CheckPassword(Self):

        cond1 = False
        cond2 = False
        cond3 = False
        cond4 = False
        Cond = [cond1 , cond2 , cond3 , cond4]

        invalidpass = False
        SpecialCharacters = ("$" , "#" , "@" , "?" , "*")

        for x in range(0 , len(Cond)):
            Cond[x] = False

        if Self.Checkpass == 1:
                
            for x in range(0 , len(Self.P1password)):

                #One condition can be met per pass if a condition is met change to false

                if not Cond[0]:
                    if ord(Self.P1password[x]) in range(ord("a") , (ord("z") + 1)):
                        Cond[0] = True

                if not Cond[1]:
                    if ord(Self.P1password[x]) in range(ord("A") , (ord("Z") + 1)):
                        Cond[1] = True

                if not Cond[2]:
                    try:
                        if int(Self.P1password[x]) in range(0 , 10):
                            Cond[2] = True
                    except ValueError:
                        a = 1

                if not Cond[3]:
                    if Self.P1password[x] in SpecialCharacters:
                        Cond[3] = True

        else:

            for x in range(0 , len(Self.P2password)):

                #One condition can be met per pass if a condition is met change to false

                if not Cond[0]:
                    if ord(Self.P2password[x]) in range(ord("a") , (ord("z") + 1)):
                        Cond[0] = True

                if not Cond[1]:
                    if ord(Self.P2password[x]) in range(ord("A") , (ord("Z") + 1)):
                        Cond[1] = True

                if not Cond[2]:
                    try:
                        if int(Self.P2password[x]) in range(0 , 10):
                            Cond[2] = True
                    except ValueError:
                        a = 1

                if not Cond[3]:
                    if Self.P2password[x] in SpecialCharacters:
                        Cond[3] = True
            

        for x in range(0 , len(Cond)):
            if not Cond[x]:
                invalidpass = True

        if invalidpass:
            tkinter.messagebox.showerror("Invalid Password" , "Your password is invalid!")
            
            if not Cond[0]:
                tkinter.messagebox.showerror("Invalid Password" , "Your password doesn't contain a lower case letter")

            if not Cond[1]:
                tkinter.messagebox.showerror("Invalid Password" , "Your password doesn't contain an upper case letter")
                
            if not Cond[2]:
                tkinter.messagebox.showerror("Invalid Password" , "Your password doesn't contain a digit")

            if not Cond[3]:
                tkinter.messagebox.showerror("Invalid Password" , "Your password doesn't contain a special character")

        return invalidpass
        
        
        

        

        

a = BattleShip()

        
