import time
import color

dims=[]
positions={}
powerups={}

def initializePositions():
    invalid=False
    rows=input(color.bcolors.OKBLUE + "enter number of rows (5-15): " + color.bcolors.ENDC)
    if rows not in ("5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"):
        invalid=True
    while invalid:
        rows=input(color.bcolors.OKBLUE + "invalid input, please enter integer from 5-15: " + color.bcolors.ENDC)
        if rows in ("5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"):
            invalid = False
    columns=input(color.bcolors.OKBLUE + "enter number of columns (5-15): " + color.bcolors.ENDC)
    if columns not in ("5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"):
        invalid=True
    while invalid:
        columns=input(color.bcolors.OKBLUE + "invalid input, please enter integer from 5-15: " + color.bcolors.ENDC)
        if columns in ("5", "6", "7", "8", "9", "10", "11", "12", "13", "14", "15"):
            invalid = False
    rows=int(rows)
    columns=int(columns)
    numberOfStones=columns-2-(columns%2)
    return [columns, rows], {"xPos": [(columns-1)//2, rows-1], "oPos": [(columns-1)-((columns-1)//2), 0], "xStones": [[i, rows-2] for i in range(1, 1+numberOfStones)], "oStones": [[i, 1] for i in range(1, 1+numberOfStones)]}

def choosePowerUps():
    blindMode=False
    invalid=False
    print(color.bcolors.OKBLUE + "s = swap, e = explosion, b = blind")
    powerups = input("Enter code for each powerup, separated by spaces (enter nothing for no powerup): "  + color.bcolors.ENDC).split()
    poweruplist=["s", "e", "b"]
    if any(i not in poweruplist for i in powerups):
        invalid=True
    while invalid:
        powerups=input(color.bcolors.OKBLUE + "Invalid input! Enter the powerup codes, separated by spaces.\ns = swap, e = explosion, b = blind: " + color.bcolors.ENDC).split()
        if not any(i not in poweruplist for i in powerups):
            invalid=False
    if "b" in powerups:
        blindMode=True
    return {i:[(dims[0]+5-(dims[0]%2))//7, (dims[0]+5-(dims[0]%2))//7] for i in powerups if i != "b"}, blindMode

def drawBoard(dimensions, posMap, won, blindMode):
    blindSet={"xPos": [(dims[0]-1)//2, dims[1]-1], "oPos": [(dims[0]-1)-((dims[0]-1)//2), 0], "xStones": [[i, dims[1]-2] for i in range(1, 1+dims[0]-2-(dims[0]%2))], "oStones": [[i, 1] for i in range(1, 1+dims[0]-2-(dims[0]%2))]}
    if won:
        x=0.35
    else:
        x=0
    board = [[color.bcolors.WARNING + "." + color.bcolors.ENDC for i in range(dimensions[0])] for j in range(dimensions[1])]
    if not blindMode:
        board[posMap["xPos"][1]][posMap["xPos"][0]]=color.bcolors.OKCYAN + "X" + color.bcolors.ENDC
        board[posMap["oPos"][1]][posMap["oPos"][0]]=color.bcolors.OKBLUE + "O" + color.bcolors.ENDC
        for i in posMap["xStones"]:
            board[i[1]][i[0]]=color.bcolors.OKCYAN + "x" + color.bcolors.ENDC
        for i in posMap["oStones"]:
            board[i[1]][i[0]]=color.bcolors.OKBLUE + "o" + color.bcolors.ENDC
    if blindMode:
        board[blindSet["xPos"][1]][blindSet["xPos"][0]]=color.bcolors.OKCYAN + "X" + color.bcolors.ENDC
        board[blindSet["oPos"][1]][blindSet["oPos"][0]]=color.bcolors.OKBLUE + "O" + color.bcolors.ENDC
        for i in blindSet["xStones"]:
            board[i[1]][i[0]]=color.bcolors.OKCYAN + "x" + color.bcolors.ENDC
        for i in blindSet["oStones"]:
            board[i[1]][i[0]]=color.bcolors.OKBLUE + "o" + color.bcolors.ENDC
    for i in range(len(board)):
        a=str(i)+ (3-len(str(i)))*" " + (i%2)*" "
        for j in range(len(board[0])):
            a+=board[i][j]
            a+= " "
        print(a)
        time.sleep(x)

def makeMove(player):
    direction={"w": [-((positions[f"{player}Pos"][1]+1)%2), -1], "e": [positions[f"{player}Pos"][1]%2, -1], "z": [-((positions[f"{player}Pos"][1]+1)%2), 1], "x": [(positions[f"{player}Pos"][1]%2), 1], "a": [-1, 0], "d": [1, 0]}
    move = input(f"Player {player}: ")
    while not validity(move, player, positions[f"{player}Pos"][0], positions[f"{player}Pos"][1], "regular"):
        print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
        move=input(f"Player {player}: ")
    if move=="w" or move=="e" or move=="d" or move=="x" or move=="z" or move=="a":
        pushAStone(positions[f"{player}Pos"][0]+direction[move][0], positions[f"{player}Pos"][1]+direction[move][1], move)
        positions[f"{player}Pos"][0]+=direction[move][0]
        positions[f"{player}Pos"][1]+=direction[move][1]
    if move=="p":
        if player=="x":
            a=0
        else:
            a=1
        print("powerups available: ", [(i, powerups[i][a]) for i in powerups.keys()])
        move=input(f"Enter powerup key or b to go back: ")
        while not validity(move, player, 0, 0, "choosingPowerUp"):
            print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
            move=input("Enter powerup key or b to go back: ")
        if move=="b":
            return makeMove(player)
        elif move=="e":
            powerUpReturn=["e"]
            move=input("Enter y coordinate for explosion: ")
            while not validity(move, player, 0, 0, "explosionY"):
                print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
                move=input("Enter valid y coordinate for explosion: ")
            powerUpReturn.append(int(move))
            move=input("Enter x coordinate for explosion: ")
            while not validity(move, player, 0, 0, "explosionX"):
                print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
                move=input("Enter valid x coordinate for explosion: ")
            powerUpReturn.insert(1, int(move))
            powerups["e"][a]-=1
            if [powerUpReturn[1], powerUpReturn[2]] in positions["xStones"]:
                positions["xStones"].remove([powerUpReturn[1], powerUpReturn[2]])
            if [powerUpReturn[1], powerUpReturn[2]] in positions["oStones"]:
                positions["oStones"].remove([powerUpReturn[1], powerUpReturn[2]])
            for i in direction.keys():
                if validity(i, player, powerUpReturn[1], powerUpReturn[2], "regular"):
                    powerDirection={"w": [-((powerUpReturn[2]+1)%2), -1], "e": [powerUpReturn[2]%2, -1], "z": [-((powerUpReturn[2]+1)%2), 1], "x": [(powerUpReturn[2]%2), 1], "a": [-1, 0], "d": [1, 0]}
                    pushAStone(powerUpReturn[1]+powerDirection[i][0], powerUpReturn[2]+powerDirection[i][1], i)
            move=powerUpReturn
        elif move=="s":
            powerUpReturn=["s"]
            move=input("Enter y coordinate of stone: ")
            while not validity(move, player, 0, 0, "swapY"):
                print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
                move=input("Enter valid y coordinate of stone: ")
            powerUpReturn.append(int(move))
            move=input("Enter x coordinate of stone: ")
            while not validity(move, player, 0, powerUpReturn[1], "swapX"):
                print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
                move=input("Enter valid X coordinate of stone: ")
            powerUpReturn.insert(1, int(move))
            powerups["s"][a]-=1
            if player=="x":
                positions["oStones"].remove([powerUpReturn[1], powerUpReturn[2]])
                positions["oStones"].append([positions["xPos"][0], positions["xPos"][1]])
                positions["xPos"].clear()
                positions["xPos"].append(powerUpReturn[1])
                positions["xPos"].append(powerUpReturn[2])
            if player=="o":
                positions["xStones"].remove([powerUpReturn[1], powerUpReturn[2]])
                positions["xStones"].append([positions["oPos"][0], positions["oPos"][1]])
                positions["oPos"].clear()
                positions["oPos"].append(powerUpReturn[1])
                positions["oPos"].append(powerUpReturn[2])
            move=powerUpReturn
    return move

def pushAStone(x, y, move):
    direction={"w": [-((y+1)%2), -1], "e": [y%2, -1], "z": [-((y+1)%2), 1], "x": [(y%2), 1], "a": [-1, 0], "d": [1, 0]}
    if [x, y] in positions["xStones"]:
        pushAStone(x+direction[move][0], y+direction[move][1], move)
        positions["xStones"].append([x+direction[move][0], y+direction[move][1]])
        positions["xStones"].remove([x, y])
    if [x, y] in positions["oStones"]:
        pushAStone(x+direction[move][0], y+direction[move][1], move)
        positions["oStones"].append([x+direction[move][0], y+direction[move][1]])
        positions["oStones"].remove([x, y])

def validity(move, player, x, y, moveType):
    if moveType=="regular":
        direction={"w": [-((y+1)%2), -1, (x==0 and not y%2) or y==0], "e": [y%2, -1, (x==dims[0]-1 and y%2) or y==0], "z": [-((y+1)%2), 1, (x==0 and not y%2) or y==dims[1]-1], "x": [(y%2), 1, (x==dims[0]-1 and  y%2) or y==dims[1]-1], "a": [-1, 0, x==0], "d": [1, 0, x==dims[0]-1]}
        if not move in ["d","e","w","a","z","x","1", "p"]:
            return False
        elif move == "1":
            return True
        elif move=="p":
            if player=="x":
                a=0
            else:
                a=1
            if all(powerups[i][a]==0 for i in powerups.keys()):
                return False
            else:
                return True
        elif direction[move][2] or [x+direction[move][0], y+direction[move][1]]==positions["xPos"] or [x+direction[move][0], y+direction[move][1]]==positions["oPos"]:
            return False
        elif [x+direction[move][0], y+direction[move][1]] in positions["xStones"] or [x+direction[move][0], y+direction[move][1]] in positions["oStones"]:
            return validity(move, player, x+direction[move][0], y+direction[move][1], "regular")
        else:
            return True
    elif moveType=="choosingPowerUp":
        if player=="x":
            a=0
        else:
            a=1
        availPowerUps=[i for i in powerups.keys() if powerups[i][a]>0]
        if move in availPowerUps or move=="b":
            return True
        else:
            return False
    elif moveType=="explosionX":
        if move in tuple(map(str, range(dims[0]))):
            return True
        else:
            return False
    elif moveType=="explosionY":
        if move in tuple(map(str, range(dims[1]))):
            return True
        else:
            return False
    elif moveType=="swapY":
        if player=="x":
            if any(str(i[1])==move for i in positions["oStones"]):
                return True
            else:
                return False
        else:
            if any(str(i[1])==move for i in positions["xStones"]):
                return True
            else:
                return False
    elif moveType=="swapX":
        if not move.isnumeric():
            return False
        if player=="x":
            if [int(move), y] in positions["oStones"]:
                return True
            else:
                return False
        else:
            if [int(move), y] in positions["xStones"]:
                return True
            else:
                return False

def checkDraw():
    if all((i[1]==0 or (i[0]+i[1]%2)%(dims[0])==0) for i in positions["oStones"]) and all((i[1]==dims[1]-1 or (i[0]+i[1]%2)%(dims[0])==0) for i in positions["xStones"]):
        return True
        
def checkWin(player):
    if any(i[1]==0 for i in positions["xStones"]):
        return True, "x"
    if any(i[1]==dims[1]-1 for i in positions["oStones"]):
        return True, "o"
    else:
        return False, ""
