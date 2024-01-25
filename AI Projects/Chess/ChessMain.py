"""
Get available moves
Check if each move is valid
Is position in check if move is played
Need to get all opponents available moves to check
Get available moves

"""
import pygame, math, random, sys, os, io

class game:
    def __init__(self) -> None:
        self.__colours = ["white", "black"]
        self.__cellSize = 100
        self.__windowSize = 8 * self.__cellSize, 8 * self.__cellSize
        self.__refreshRate = pygame.time.Clock()

        self.__players = self.__generatePlayers()
        self.__currentPlayer = self.__players[0]
        
        self.__win = pygame.display.set_mode(self.__windowSize)
        self.__board = board(self)
        self.__playGame()
    
    def getColours(self):
        return self.__colours
    
    def getCellSize(self):
        return self.__cellSize
    
    def getPlayers(self):
        return self.__players
    
    def getCurrentPlayer(self):
        return self.__currentPlayer
    
    def getBoard(self):
        return self.__board
    
    def convertToPlayer(self, colour):
        if self.__players[0].getColour() == colour: return self.__players[0]
        elif self.__players[1].getColour() == colour: return self.__players[1]

    
    @staticmethod
    def getOTherColour(colour):
        c = ["black", "white"]
        return c[1 - c.index(colour)]

    @staticmethod
    def loadSVG(filename, scale):
        filename = os.path.join(os.path.dirname(__file__), 'Sprites', filename)
        svg_string = open(filename, "rt").read()

        start = svg_string.find('<svg')
        width = svg_string.find('width=')
        height = svg_string.find('height=')
        endHeight = svg_string[height+8:].find('"')
        newWidth = int(int(svg_string[width+7:height - 2]) * scale)
        newHeight = int(int(svg_string[height+8:height+8+endHeight]) * scale)

        if start > 0 and width > start and height > width:
            svg_string = svg_string[:start+4] + f' transform="scale({scale})"' + svg_string[start+4:width] + f' width="{newWidth}"  height="{newHeight}" ' + svg_string[height+9+endHeight:]
        
        return pygame.image.load(io.BytesIO(svg_string.encode()))
    
    def __generatePlayers(self):
        return [player(self.__colours[i], ["player", "bot"][i], [-1, 1][i]) for i in range(2)]

    @staticmethod
    def gridToFen(grid):
        fen = ""
        for row in grid:
            for cell in row:
                if cell.getContains() == None:
                    fen += "_"
                else:
                    fen += cell.getContains().getSymbol()
            fen += "|"
        return fen[:-1]
    
    @staticmethod
    def fenToGrid(fen, player1, player2):
        grid =  [[cell(["white", "grey"][(i + y) % 2], [i, y]) for i in range(8)] for y in range(8)]
        fen = fen.split('|')
        for r in range(len(fen)):
            for c in range(len(fen[r])):
                s = fen[r][c]
                player = None
                colour = None
                if s != "_":
                    if s.lower() == s:
                        player = player2
                        colour = "black"
                    else:
                        player = player1
                        colour = "white"
                    
                    if s.lower() == "k": grid[r][c].setContains(king(player, s, [c, r], colour, f'{colour}_king.svg'))
                    elif s.lower() == "q": grid[r][c].setContains(queen(player, s, [c, r], colour, f"{colour}_queen.svg"))
                    elif s.lower() == "b": grid[r][c].setContains(bishop(player, s, [c, r], colour, f"{colour}_bishop.svg"))
                    elif s.lower() == "h": grid[r][c].setContains(knight(player, s, [c, r], colour, f"{colour}_knight.svg"))
                    elif s.lower() == "r": grid[r][c].setContains(rook(player, s, [c, r], colour, f"{colour}_rook.svg"))
                    elif s.lower() == "p": grid[r][c].setContains(pawn(player, s, [c, r],  colour, f"{colour}_pawn.svg"))
        return grid


    def __drawBoard(self):
        for row in self.__board.getGrid():
            for cell in row:
                position = [cell.getLocation()[0] * self.__cellSize, cell.getLocation()[1] * self.__cellSize, self.__cellSize, self.__cellSize]
                pygame.draw.rect(self.__win, cell.getColour(), position)
    
    def __drawPieces(self):
        for piece in self.__board.getPieces():
            location = (self.__cellSize * piece.getLocation()[0], self.__cellSize * piece.getLocation()[1])
            self.__win.blit(piece.getImg(), location)
    
    @staticmethod
    def isLocationValid(location):
        return 0 <= location[0] <= 7 and 0 <= location[1] <= 7
    
    @staticmethod
    def getNewLocation(move, piece):
        currentLocation = piece.getLocation()
        newLocation = [currentLocation[0] + move[0],
                       currentLocation[1] + move[1] * piece.getPlayer().getDirection()]
        
        if game.isLocationValid(newLocation):
            return newLocation
        else:
            return None
    

    @staticmethod
    def generateDifferences(startingLocation, endingLocation):
        differences = [0, 0]

        if endingLocation[1] < startingLocation[1]: differences[1] = -1
        elif endingLocation[1] > startingLocation[1]: differences[1] = 1

        if endingLocation[0] < startingLocation[0]: differences[0] = -1
        elif endingLocation[0] > startingLocation[0]: differences[0] = 1

        return differences

    def getSquaresBetween(self, startingLocation, endingLocation, player):
        """Returns all of the squares between 2 locations"""
        if startingLocation == None or endingLocation == None:
            return [False]
        squares = []
        differences = game.generateDifferences(startingLocation, endingLocation)

        currentLocation = [startingLocation[0], startingLocation[1]]
        
        while currentLocation != endingLocation:
            currentLocation[0] += differences[0]
            currentLocation[1] += differences[1]

            currentCell = self.__board.getGrid()[currentLocation[1]][currentLocation[0]]

            if currentCell.getContains() == None:
                squares.append([])
                squares[-1] += currentLocation
            elif currentCell.getContains().getPlayer() == self.getOtherPlayer(player):
                squares.append([])
                squares[-1] += currentLocation
                break
            elif currentCell.getContains().getPlayer() == player:
                break
        return squares
    
    def generateCopyOfGrid(self, grid):
        newFen = game.gridToFen(grid)
        newGrid = game.fenToGrid(newFen, self.__players[0], self.__players[1])
        return newGrid
    
    
    def applyMoveToFen(self, fen, piece, move):
        """Assumes move is valid"""
        newFen = fen.split('|')
        pI = piece.getLocation()
        eI = game.getNewLocation(move, piece)
        newFen[pI[1]] = newFen[pI[1]][:pI[0]] + "_" + newFen[pI[1]][pI[0]+ 1:]
        newFen[eI[1]] = newFen[eI[1]][:eI[0]] + piece.getSymbol() + newFen[eI[1]][eI[0]+ 1:]
        holder = ""
        for row in newFen:
            holder += row
            holder += "|"
        
        return holder[:-1]

    @staticmethod
    def getKing(fen, player):
        """Returns a arr of locations"""
        """Player 1 == lowerCase Player 2 == upperCase"""
        if player.getColour() == "white": symbol = "k"
        else: symbol = "K"

        newFen = fen
        newFen = newFen.split("|")
        for i in range(len(newFen)):
            for ii in range(len(newFen[i])):
                if newFen[i][ii] == symbol:
                        return [ii, i]
    
    def getPieceAtLocation(self, location):
        """Assumes the tile isnt empty"""
        return self.__board.getGrid()[location[1]][location[0]].getContains()
    

    
    def isCheck(self, fen, player):
        """Method wil return if the inputted player is in check"""
        """Probably best to use a fen since it can then generate a board from that impliment after"""
        """Cycle through each piece, if it can land on the opponents king, check has occured"""
        king = game.getKing(fen, player)
        grid = self.fenToGrid(fen, self.__players[0], self.__players[1])
        print("________________________________")
        print("king: ", king)
        print("fen: ", fen)
        for row in grid:
            for tile in row:
                if tile.getContains() != None and tile.getContains().getPlayer() != player:
                    validMoves = self.getAvailableMoves(tile.getContains(), False)
                    targetTiles = [game.getNewLocation(move, tile.getContains()) for move in validMoves]
                    print(targetTiles, "piece: ", tile.getContains().getSymbol(), "colour: ", tile.getContains().getPlayer().getColour())
                    if king in targetTiles:
                        print("isCheck")
                        return True
        return False

    
    def isMoveValid(self, piece, move, needCheck):
        """Major logic needed for this function""" 
        """May wanna rename to 'canPieceMoveThere'"""
        """Now need to add logic to allow for checks"""
        newLocation = game.getNewLocation(move, piece)
        if newLocation != None:
            cell = self.__board.getGrid()[newLocation[1]][newLocation[0]]
            if cell.getContains() == None or cell.getContains().getPlayer() != piece.getPlayer():
                if needCheck:
                    checked = self.isCheck(self.applyMoveToFen(self.__board.getFen(), piece, move), piece.getPlayer())
                elif not needCheck:
                    checked = False
                if not checked:
                    #piece can be placed there
                    if piece.getSymbol().lower() != "h" and newLocation in self.getSquaresBetween(piece.getLocation(), newLocation, piece.getPlayer()):
                        #piece can move there
                        return True
                    elif piece.getSymbol().lower() == "h":
                        return True
        return False
    
    def getAvailableMoves(self, piece, needCheck):
        validMoves = []
        for move in piece.getMoves():
            if self.isMoveValid(piece, move, needCheck):
                validMoves.append(move)

        return validMoves
    
    def __drawAvailableMoves(self):
        selectedPiece = self.__currentPlayer.getSelectedPiece()
        if selectedPiece != None:
            for move in selectedPiece.getLegalMoves():
                location = game.getNewLocation(move, selectedPiece)
                location = [(location[0] + 0.5) * self.__cellSize, (location[1] + 0.5) * self.__cellSize]
                pygame.draw.circle(self.__win, "yellow", (location[0], location[1]), 20)
                
    
    def getOtherPlayer(self, player):
        return self.__players[1 - self.__players.index(player)]
    
    def getSelectedSquare(self, mousePosition):
        x = mousePosition[0] // self.__cellSize
        y = mousePosition[1] // self.__cellSize
        return self.__board.getGrid()[y][x]

    def __playGame(self):
        while True:
            self.__refreshRate.tick(60)
            mousePosition = pygame.mouse.get_pos()
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    selectedSquare = self.getSelectedSquare(mousePosition)
                    if selectedSquare.getContains() == None:
                        if self.__currentPlayer.getSelectedPiece() != None:
                            validLocations = [game.getNewLocation(item, self.__currentPlayer.getSelectedPiece()) for item in self.__currentPlayer.getSelectedPiece().getLegalMoves()]
                            if selectedSquare.getLocation() in validLocations:
                                self.__board.getGrid()[self.__currentPlayer.getSelectedPiece().getLocation()[1]][self.__currentPlayer.getSelectedPiece().getLocation()[0]].setContains(None)
                                self.__currentPlayer.getSelectedPiece().setLocation(selectedSquare.getLocation())
                                selectedSquare.setContains(self.__currentPlayer.getSelectedPiece())
                                self.__currentPlayer.setSelectedPiece(None)
                                self.__currentPlayer = self.getOtherPlayer(self.__currentPlayer)
                                self.__board.setFen(self.gridToFen(self.__board.getGrid()))
                            else:
                                self.__currentPlayer.setSelectedPiece(None)

                    elif selectedSquare.getContains().getPlayer() == self.__currentPlayer:
                        self.__currentPlayer.setSelectedPiece(selectedSquare.getContains())
                        self.__currentPlayer.getSelectedPiece().setLegalMoves(self.getAvailableMoves(self.__currentPlayer.getSelectedPiece(), True))

                    elif selectedSquare.getContains().getPlayer() == self.getOtherPlayer(self.__currentPlayer):
                        #Selected the other players piece
                        pass
                        

            self.__drawBoard()
            self.__drawPieces()
            self.__drawAvailableMoves()

            pygame.display.flip()

class board:
    def __init__(self, game) -> None:
        self.__game = game
        self.__grid = self.generateGrid()
        self.__pieces = self.setUpBoard()
        self.__fen = game.gridToFen(self.__grid)
    
    def getGrid(self):
        return self.__grid
    
    def getPieces(self):
        return self.__pieces
    
    def getFen(self):
        return self.__fen
    
    def setFen(self, fen):
        self.__fen = fen
        
    
    def generateGrid(self):
        return [[cell(["white", "grey"][(i + y) % 2], [i, y]) for i in range(8)] for y in range(8)]
    
    def setUpBoard(self):
        pieces = []
        for i in range(2):
            player = self.__game.getPlayers()[1 - i]
            colour = self.__game.getColours()[1 - i]

            kingPiece = king(player, ["k", "K"][i], [4,i * 7], colour, f'{colour}_king.svg')
            queenPiece = queen(player, ["q", "Q"][i], [3,i * 7], colour, f"{colour}_queen.svg")

            self.__grid[i * 7][4].setContains(kingPiece)
            self.__grid[i * 7][3].setContains(queenPiece)

            pieces.append(kingPiece)
            pieces.append(queenPiece)

            for ii in range(2):
                rookPiece = rook(player, ["r", "R"][i], [[0, 7][ii], i * 7], colour, f"{colour}_rook.svg")
                knightPiece = knight(player, ["h", "H"][i], [[1, 6][ii], i * 7], colour, f"{colour}_knight.svg")
                bishopPiece = bishop(player, ["b", "B"][i], [[2, 5][ii], i * 7], colour, f"{colour}_bishop.svg")

                self.__grid[i * 7][[0, 7][ii]].setContains(rookPiece)
                self.__grid[i * 7][[1, 6][ii]].setContains(knightPiece)
                self.__grid[i * 7][[2, 5][ii]].setContains(bishopPiece)

                pieces.append(rookPiece)
                pieces.append(knightPiece)
                pieces.append(bishopPiece)
            
            for ii in range(8):
                pawnPiece = pawn(player, ["p", "P"][i], [ii, 1 + i * 5], colour, f"{colour}_pawn.svg")

                self.__grid[1 + i * 5][ii].setContains(pawnPiece)

                pieces.append(pawnPiece)
            
        return pieces
        
                

class cell:
    def __init__(self, colour, location) -> None:
        self.__contains = None
        self.__colour = colour
        self.__location = location
    
    def getContains(self):
        return self.__contains
    
    def getColour(self):
        return self.__colour
    
    def getLocation(self):
        return self.__location
    
    def setContains(self, value):
        self.__contains = value



class player:
    def __init__(self, colour, type, direction) -> None:
        self.__colour = colour
        self.__type = type
        self.__selectedPiece = None
        self.__direction = direction
    
    def getColour(self):
        return self.__colour
    
    def getType(self):
        return self.__type
    
    def getSelectedPiece(self):
        return self.__selectedPiece
    
    def getDirection(self):
        return self.__direction
    
    def setSelectedPiece(self, piece):
        self.__selectedPiece = piece
    


class piece:
    def __init__(self, player, symbol, location, colour, img) -> None:
        self._player = player
        self._symbol = symbol
        self._location = location
        self._colour = colour
        self._img = game.loadSVG(img, 100 / 45)#should make it not need 45
        self._legalMoves = []
    
    def getPlayer(self):
        return self._player
    
    def getSymbol(self):
        return self._symbol

    def getLocation(self):
        return self._location
    
    def getColour(self):
        return self._colour
    
    def getImg(self):
        return self._img
    
    def getLegalMoves(self):
        return self._legalMoves
    
    def setLocation(self, location):
        self._location = location
    
    def setLegalMoves(self, moves):
        self._legalMoves = moves
    
    @staticmethod
    def getDiagonals(limit):
        moves = []
        types = [
            [-1, -1],
            [1, -1],
            [1, 1],
            [-1, 1]
        ]
        for i in range(1, min(limit + 1, 8)):
            for item in types:
                moves.append([value * i for value in item])
        return moves

    @staticmethod
    def getCardinals(limit):
        moves = []
        types = [
            [-1, 0],
            [1, 0],
            [0, 1],
            [0, -1]
        ]
        for i in range(1, min(limit + 1, 8)):
            for item in types:
                moves.append([value * i for value in item])
        return moves
    

        

class king(piece):
    def __init__(self, player, symbol, location, colour, img) -> None:
        super().__init__(player, symbol, location, colour, img)
        

    @staticmethod
    def getMoves():
        return piece.getCardinals(1) + piece.getDiagonals(1)
        

class queen(piece):
    def __init__(self, player, symbol, location, colour, img) -> None:
        super().__init__(player, symbol, location, colour, img)
    
    @staticmethod
    def getMoves():
        return piece.getCardinals(7) + piece.getDiagonals(7)

class knight(piece):
    def __init__(self, player, symbol, location, colour, img) -> None:
        super().__init__(player, symbol, location, colour, img)
    
    @staticmethod
    def getMoves():
        return [
            [-2, -1],
            [-1, -2],
            [-2, 1],
            [1, -2],
            [2, -1],
            [-1, 2],
            [2, 1],
            [1, 2]
        ]

class rook(piece):
    def __init__(self, player, symbol, location, colour, img) -> None:
        super().__init__(player, symbol, location, colour, img)
    
    @staticmethod
    def getMoves():
        return piece.getCardinals(7)

class bishop(piece):
    def __init__(self, player, symbol, location, colour, img) -> None:
        super().__init__(player, symbol, location, colour, img)

    @staticmethod
    def getMoves():
        return piece.getDiagonals(7)
    
class pawn(piece):
    def __init__(self, player, symbol, location, colour, img) -> None:
        super().__init__(player, symbol, location, colour, img)
    
    @staticmethod
    def getMoves():
        return [
            [0, 1],
            [0, 2]
        ]

pygame.init()
chess = game()

