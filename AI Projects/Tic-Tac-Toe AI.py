#type: ignore
from graphics import *
from random import *

def generateLine(p1, p2, c, w = 1):
    line = Line(p1, p2)
    line.setFill(c)
    line.setWidth(w)
    return line

def generateCircle(p1, c, r, w):
    circle = Circle(p1, r)
    circle.setOutline(c)
    circle.setWidth(w)
    return circle

class TicTacToe():
    def __init__(self, cellSize):
        self.win = GraphWin("Tic-Tac-Toe", cellSize * 3, cellSize * 3)
        self.cellSize = cellSize
        self.players = self.generatePlayers()
        self.currentPlayer = self.players[0]
        self.board = Board()
        self.drawBoard()
        self.playGame()
    
    def generatePlayers(self):
        players = []
        for symbol in ["X", "O"]:
            players.append(Player(symbol, ["Player", "Auto"][["X", "O"].index(symbol)]))
        return players

    def generateBoardFromFEN(self, FEN):
        board = []
        for row in FEN.split("|"):
            newRow = []
            for cell in row:
                newRow.append(Cell(self.getPlayerWithSymbol(row)))
            board.append(newRow)
        return board
    
    def generateFENFromBoard(self, board):
        fen = ""
        for row in board:
            for cell in row:
                if cell.player == None:
                    fen += "_"
                else:
                    fen += cell.player.symbol
            fen += "|"
        return fen[:-1]
    
    def displayFEN(self, fen):
        for row in fen.split("|"):
            print(row)
    
    def getPlayerWithSymbol(self, symbol):
        for player in self.players:
            if player.symbol == symbol:
                return player
    
    def applyMove(self, board, move, currentPlayer):
        newBoard = board
        for row in newBoard:
            for cell in row:
                if cell == move:
                    cell.player = currentPlayer
        return newBoard
    
    def getOtherPlayer(self, currentPlayer):
        i = self.players.index(currentPlayer)
        return self.players[1 - i]

    def getCellFromMouse(self, mouse):
        y = int(mouse.getY() // self.cellSize)
        x = int(mouse.getX() // self.cellSize)
        return self.board.grid[y][x]
    
    def isMoveValid(self, move):
        if move != None and move.player == None:
            return True
        else:
            return False

    def drawBoard(self):
        #Horizontal
        generateLine(Point(self.win.getWidth() / 3, 0), Point(self.win.getWidth() / 3, self.win.getHeight()), "black", 5).draw(self.win)
        generateLine(Point(2 * self.win.getWidth() / 3, 0), Point(2 * self.win.getWidth() / 3, self.win.getHeight()), "black", 5).draw(self.win)
        #Vertical
        generateLine(Point(0, self.win.getHeight() / 3), Point(self.win.getWidth(), self.win.getHeight() / 3), "black", 5).draw(self.win)
        generateLine(Point(0, 2 * self.win.getHeight() / 3), Point(self.win.getWidth(), 2 * self.win.getHeight() / 3), "black", 5).draw(self.win)
    
    def drawPiece(self, cell):
        if cell.player.symbol == "X":
            TLX = cell.location[0] * self.cellSize + self.cellSize * 0.1
            TLY = cell.location[1] * self.cellSize + self.cellSize * 0.1
            width = self.cellSize * 0.8
            generateLine(Point(TLX, TLY), Point(TLX + width, TLY + width), "black", 5).draw(self.win)#Neg
            generateLine(Point(TLX, TLY + width), Point(TLX + width, TLY), "black", 5).draw(self.win)#Pos
        else:
            centerX = (cell.location[0] + 0.5) * self.cellSize
            centerY = (cell.location[1] + 0.5) * self.cellSize
            generateCircle(Point(centerX, centerY), "black", self.cellSize * 0.4, 5).draw(self.win)
    
    def getMoveFromFEN(self, FEN):
        currentFEN = self.board.fen
        currentFEN = currentFEN.replace("|", "")
        newFEN = FEN
        newFEN = newFEN.replace("|", "")

        for c in range(len(currentFEN)):
            if currentFEN[c] != newFEN[c]:
                return self.board.grid[int(c // 3)][c % 3]

    
    def gameOver(self, FEN):        
        if (FEN[0] != "_" and FEN[0::5].count(FEN[0]) == 3) or (
            FEN[2] != "_" and FEN[2::3].count(FEN[2]) == 3):
            return self.getPlayerWithSymbol(FEN[5])
        for i in range(3):
            if FEN[i] != "_" and FEN[i::4].count(FEN[i]) == 3:
                return self.getPlayerWithSymbol(FEN[i])
            elif FEN[i * 4] != "_" and FEN[i*4:i*4+3].count(FEN[i*4]) == 3:
                return self.getPlayerWithSymbol(FEN[i * 4])
        if FEN.count("_") == 0:
            return None
        return False
    

    def playGame(self):
        while self.gameOver(self.generateFENFromBoard(self.board.grid)) == False:
            move = self.currentPlayer.getMove(self)
            if self.isMoveValid(move):
                self.board.grid = self.applyMove(self.board.grid, move, self.currentPlayer)
                self.board.fen = self.generateFENFromBoard(self.board.grid)
                self.drawPiece(move)
                self.currentPlayer = self.getOtherPlayer(self.currentPlayer)
        
        winner = self.gameOver(self.generateFENFromBoard(self.board.grid))
        if winner not in self.players:
            print(f'Draw')
        else:
            print(f'Winner was: {winner.symbol}')
        
        self.win.getMouse()


class Board():
    def __init__(self):
        self.grid = self.generateGrid()
        self.fen = "___|___|___"

    def generateGrid(self):
        grid = []
        for column in range(3):
            row = []
            for cell in range(3):
                row.append(Cell(None, [cell, column]))
            grid.append(row)
        return grid
    
    


class Cell():
    def __init__(self, player, location):
        self.player = player
        self.location = location
    

class Player():
    def __init__(self, symbol, type):
        self.symbol = symbol
        self.type = type
    
    def getMove(self, TicTacToe):
        if self.type == "Player":
            return self.getPlayerMove(TicTacToe)
        else:
            return self.getAutoMove(TicTacToe)

    
    def getPlayerMove(self, TicTacToe):
        cellSelection = TicTacToe.win.checkMouse()
        if cellSelection != None:
            selectedCell = TicTacToe.getCellFromMouse(cellSelection)
            return selectedCell
        return None
            

    def getAutoMove(self, TicTacToe):
        bot = MiniMax(11, TicTacToe.generateFENFromBoard(TicTacToe.board.grid), self, TicTacToe)
        bot.evalualteLayers()
        move = bot.getBestMove()
        #print("Bot Choice: ", move.fen)
        #bot.displayData()
        return TicTacToe.getMoveFromFEN(move.fen)

class MiniMax():
    def __init__(self, depth, startingFEN, currentPlayer, TicTacToe):
        self.startingDepth = depth
        self.startingFEN = startingFEN
        self.currentPlayer = currentPlayer
        self.TicTacToe = TicTacToe

        self.layers = self.generateLayers()
        self.layers[0].append(search(self.startingDepth, self.startingFEN, self.currentPlayer, self))
    
    def displayData(self):
        for position in self.layers[1]:
            print(f'FEN: {position.fen}   Rating: {position.rating}')

        print("_________________________\n")
    
    def generateLayers(self):
        layers = []
        for layer in range(self.startingDepth + 1):
            layers.append([])
        return layers
    
    def generatePossibleFENs(self, FEN, player):
        fens = []
        for i in range(len(FEN)):
            if FEN[i] == "_":
                newFEN = FEN[:i] + player.symbol + FEN[i + 1:]
                fens.append(newFEN)
        return fens
    
    def evaluatePosition(self, position):
        if position.children == []:
            outcome = self.TicTacToe.gameOver(position.fen)
            if outcome == self.currentPlayer:
                position.rating = 1
            elif outcome == self.TicTacToe.getOtherPlayer(self.currentPlayer):
                position.rating = -1
            elif outcome == None:
                position.rating = 0
            elif outcome == False:
                position.rating = 0

        elif position.player == self.currentPlayer:
            position.rating = max([child.rating for child in position.children])
        
        else:
            position.rating = min([child.rating for child in position.children])
    
    def getBestMove(self):
        bestScore = max([position.rating for position in self.layers[1]])
        bestMoves = []
        for position in self.layers[1]:
            if position.rating == bestScore:
                bestMoves.append(position)
        #print(f'BestMoves: {[pos.fen for pos in bestMoves]}')
        return choice(bestMoves)
    
    def evalualteLayer(self, layer):
        for position in layer:
            self.evaluatePosition(position)
        
    
    def evalualteLayers(self):
        for layer in self.layers[::-1]:
            self.evalualteLayer(layer)
    
    def displayLayers(self):
        for i in range(len(self.layers)):
            print(f'Layer {i}\n')
            for fen in self.layers[i]:
                print(fen.fen)

class search():
    def __init__(self, depth, FEN, player, MiniMax):
        self.depth = depth
        self.fen = FEN
        self.player = player
        self.MiniMax = MiniMax
        self.rating = 0
        self.children = self.generateChildren()
    
    def generateChildren(self):
        children = []
        if self.depth > 0 and self.MiniMax.TicTacToe.gameOver(self.fen) not in self.MiniMax.TicTacToe.players:
            for FEN in self.MiniMax.generatePossibleFENs(self.fen, self.player):
                child = search(self.depth - 1, FEN, self.MiniMax.TicTacToe.getOtherPlayer(self.player), self.MiniMax)
                children.append(child)
    
        index = -1 * self.depth
        if self.depth == 0:
            index = self.depth
        
        self.MiniMax.layers[index] += children
        return children

game = TicTacToe(200)