import time
import color

def drawBoard(dimensions, posMap, won):
    if won:
        x=0.35
    else:
        x=0
    board = [[color.bcolors.WARNING + "." + color.bcolors.ENDC for i in range(dimensions[0])] for j in range(dimensions[1])]
    board[posMap["xPos"][1]][posMap["xPos"][0]]=color.bcolors.OKCYAN+ "X" +color.bcolors.ENDC
    board[posMap["oPos"][1]][posMap["oPos"][0]]=color.bcolors.OKBLUE+ "O" +color.bcolors.ENDC
    for i in posMap["xStones"]:
        board[i[1]][i[0]]=color.bcolors.OKCYAN + "x" + color.bcolors.ENDC
    for i in posMap["oStones"]:
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
    move=input(f"Player {player}: ")
    while not validity(move, player, positions[f"{player}Pos"][0], positions[f"{player}Pos"][1]):
        print(color.bcolors.OKRED + "Invalid move! >:( Please enter again." + color.bcolors.ENDC)
        move=input(f"Player {player}: ")
    if move=="w" or move=="e" or move=="d" or move=="x" or move=="z" or move=="a":
        pushAStone(positions[f"{player}Pos"][0]+direction[move][0], positions[f"{player}Pos"][1]+direction[move][1], move)
        positions[f"{player}Pos"][0]+=direction[move][0]
        positions[f"{player}Pos"][1]+=direction[move][1]
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
    
def validity(move, player, x, y):
    direction={"w": [-((y+1)%2), -1, (x==0 and not y%2) or y==0], "e": [y%2, -1, (x==dims[0]-1 and y%2) or y==0], "z": [-((y+1)%2), 1, (x==0 and not y%2) or y==dims[1]-1], "x": [(y%2), 1, (x==dims[0]-1 and  y%2) or y==dims[1]-1], "a": [-1, 0, x==0], "d": [1, 0, x==dims[0]-1]}
    if not move in ["d","e","w","a","z","x","1"]:
        return False
    elif move == "1":
        return True
    elif direction[move][2] or [x+direction[move][0], y+direction[move][1]]==positions["xPos"] or [x+direction[move][0], y+direction[move][1]]==positions["oPos"]:
        return False
    elif [x+direction[move][0], y+direction[move][1]] in positions["xStones"] or [x+direction[move][0], y+direction[move][1]] in positions["oStones"]:
        return validity(move, player, x+direction[move][0], y+direction[move][1])
    else:
        return True

def checkWin(player):
    if player=="x" and any(i[1]==0 for i in positions["xStones"]) or player=="o" and any(i[1]==dims[1]-1 for i in positions["oStones"]):
        return True
    else:
        return False

def checkDraw():
    if all((i[1]==0 or (i[0]+i[1]%2)%(dims[0])==0) for i in positions["oStones"]) and all((i[1]==dims[1]-1 or (i[0]+i[1]%2)%(dims[0])==0) for i in positions["xStones"]):
        return True

positions={"xPos": [3, 6], "oPos": [3, 0], "xStones": [[1, 5], [2, 5], [3, 5], [4, 5]], "oStones": [[1, 1], [2, 1], [3, 1], [4, 1]]}
dims=[7, 7]

def initializePositions():
    return [7, 7], {"xPos": [3, 6], "oPos": [3, 0], "xStones": [[1, 5], [2, 5], [3, 5], [4, 5]], "oStones": [[1, 1], [2, 1], [3, 1], [4, 1]]}
    
