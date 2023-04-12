import levelOne
import customLevel
import rules
import color
import title
import time
from os import system

inp=""
title.title()
time.sleep(2)
print(color.bcolors.OKGREEN + "Welcome to PUSHING STONES...\n")
time.sleep(2)
while True:
    inp = input(color.bcolors.OKGREEN + "Enter 'q' for classic game mode, 'w' for custom mode or 'e' for the rules of the game."  + color.bcolors.ENDC)
    if inp=="q":
        levelOne.dims, levelOne.positions = levelOne.initializePositions()
        player='x'
        while True:  
            system('clear')
            levelOne.drawBoard(levelOne.dims, levelOne.positions, False)
            lastMove = levelOne.makeMove(player)
            won=levelOne.checkWin(player)
            drawn=levelOne.checkDraw()
            if lastMove=="1":
                print("End of game!")
                break
            if drawn:
                levelOne.drawBoard(levelOne.dims, levelOne.positions, True)
                print("Draw!")
                break
            if won:
                levelOne.drawBoard(levelOne.dims, levelOne.positions, True)
                print(f"Player {player} wins!")
                break
            if player=='x':
                player='o'
            else:
                player='x'
    if inp=="w":
        customLevel.dims, customLevel.positions = customLevel.initializePositions()
        customLevel.powerups, blind =customLevel.choosePowerUps()
        player='x'
        while True:  
            system('clear')
            customLevel.drawBoard(customLevel.dims, customLevel.positions, False, blind)
            lastMove = customLevel.makeMove(player)
            won, playerWhoWon=customLevel.checkWin(player)
            drawn=customLevel.checkDraw()
            if lastMove=="1":
                print("End of game!")
                break
            if drawn:
                customLevel.drawBoard(customLevel.dims, customLevel.positions, True, False)
                print("Draw!")
                break
            if won:
                customLevel.drawBoard(customLevel.dims, customLevel.positions, True, False)
                if playerWhoWon != player:
                    print("Interesting move...")
                print(f"Player {playerWhoWon} wins!")
                break
            if player=='x':
                player='o'
            else:
                player='x'
    if inp=="e":
        rules.rule()
        input("Enter any key to go back to main menu. ")



