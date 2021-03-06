import pygame as pg
import os

class Chess:
    def __init__(self):
        self.sizeOfSquare = 100
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "wP"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "bP"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

        self.positionT0Castling = [[[7, 0], [7, 4], [7, 7]], ## Rook left(far), King, Rook Right(near)
                              [[0, 0], [0, 4]], [0, 7]]

        self.whiteKingPos = [7, 0]
        self.blackKingPos = [0, 4]
        self.Turn = "w"
        self.isPromotion = False
        self.cnt = 0
        self.piecesDirections = {"R": ((-1, 0), (0, -1), (1, 0), (0, 1)),
                                 "B": ((-1, -1), (-1, 1), (1, 1), (1, -1)),
                                 "N": ((2, 1), (1, 2), (-1, 2), (-2, 1),
                                       (-2, -1), (-1, -2), (1, -2), (2, -1)
                                       ),
                                 "K": ((-1, -1), (-1, 0), (-1, 1), (0, -1),
                                       (0, 1), (1, -1), (1, 0), (1, 1)
                                       )
                                 }
        self.chessImages = {item.strip(".png"):pg.image.load(f"img/{item}") for item in os.listdir("img")}
        self.moveLog = []

        self.getPiecesPossibleMoves = {"P": self.GetPawnPossibleMove,
                                       "K": self.GetKingPossibleMove,
                                       "Q": self.GetQueenPossibleMove,
                                       "N": self.GetKnightPossibleMove,
                                       "R": self.GetRookPossibleMove,
                                       "B": self.GetBishopPossibleMove
                                       }

        self.listOfPromotion = ["Q", "N", "R", "B"]

    def Display(self, displayWindow):

        # Draw chess broad
        tmp = True
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):

                if tmp:
                    pg.draw.rect(displayWindow, (126, 211, 0),
                                 (x * self.sizeOfSquare, y * self.sizeOfSquare, self.sizeOfSquare, self.sizeOfSquare))
                else:
                    pg.draw.rect(displayWindow, (240, 236, 242),
                                 (x * self.sizeOfSquare, y * self.sizeOfSquare, self.sizeOfSquare, self.sizeOfSquare))
                tmp = not tmp
                if self.board[y][x] != "00":
                    displayWindow.blit(self.chessImages[self.board[y][x]], ((x + .1) * self.sizeOfSquare , (y + .1) * self.sizeOfSquare))

            tmp = not tmp

    def GetPawnPossibleMove(self, x, y):
        # params: x, y is current pos of that pawn
        # return: list of possible move of that pawn

        possibleMove = []
        if self.board[x][y][0] == "w":
            if self.board[x - 1][y] == "00":
                possibleMove.append((x - 1, y))
            if x == 6 and self.board[x - 2][y] == "00": # Nam o hang ban dau chua di chuyen
                possibleMove.append((x - 2, y))

            if self.board[x - 1][y - 1][0] == "b": # left
                possibleMove.append((x-1, y-1))

            if y + 1 < 8:
                if self.board[x - 1][y + 1][0] == "b": # right
                    possibleMove.append((x-1, y+1))

        else:
            if self.board[x + 1][y] == "00":
                possibleMove.append((x + 1, y))
            if x == 1 and self.board[x + 2][y] == "00": # Nam o hang ban dau chua di chuyen
                possibleMove.append((x + 2, y))

            if self.board[x + 1][y - 1][0] == "w": # left
                possibleMove.append((x+1, y-1))

            if y + 1 < 8:
                if self.board[x + 1][y + 1][0] == "w": # right
                    possibleMove.append((x+1, y+1))

        return possibleMove

    def DisplayPopUpPromotion(self, DISPLAYWINDOW, square, color):
        '''

        :param DISPLAYWINDOW: window to display pieces for promotion
        :param square:  Position to display pop-up
        :param color: Color of pieces
        :return:
        '''
        for i in range(len(self.listOfPromotion)):
            pg.draw.rect(DISPLAYWINDOW, (255, 255, 255),
                         (square[1] * self.sizeOfSquare,square[0] + self.sizeOfSquare * i ,
                          self.sizeOfSquare, self.sizeOfSquare))
            DISPLAYWINDOW.blit(self.chessImages[color + self.listOfPromotion[i]],
                               (square[1] * self.sizeOfSquare,square[0] + self.sizeOfSquare * i ))

    def SelectPromotion(self, index):
        return self.listOfPromotion[index]

    def GetKnightPossibleMove(self, x, y):
        possibleMove = []
        for direction in self.piecesDirections["N"]:
            posx, posy = x + direction[0], y + direction[1]
            if (0 <= posx <= 7 and 0 <= posy <= 7) and \
                    (self.board[posx][posy][0] != self.board[x][y][0] or self.board[posx][posy] == "00"):
                possibleMove.append((posx, posy))
        return possibleMove

    def GetRookPossibleMove(self, x, y):
        possibleMove = []

        for direction in self.piecesDirections["R"]:
            for i in range(1, 8):
                posx, posy = x + direction[0] * i, y + direction[1] * i

                if (0 <= posx <= 7 and 0 <= posy <= 7):
                    endPiece = self.board[posx][posy]
                    if endPiece == "00":  # empty space valid
                        possibleMove.append((posx, posy))
                    elif endPiece[0] != self.board[x][y][0]:  # enemy piece is valid
                        possibleMove.append((posx, posy))
                        break
                    else:
                        break
                else:  # off broad
                    break
        return possibleMove

    def GetBishopPossibleMove(self, x, y):
        possibleMove = []
        for direction in self.piecesDirections["B"]:
            for i in range(1, 8):
                posx, posy = x + direction[0] * i, y + direction[1] * i

                if (0 <= posx <= 7 and 0 <= posy <= 7):
                    endPiece = self.board[posx][posy]
                    if endPiece == "00":  # empty space valid
                        possibleMove.append((posx, posy))
                    elif endPiece[0] != self.board[x][y][0]:
                        possibleMove.append((posx, posy))
                        break
                    else:
                        break
                else:  # off broad
                    break
        return possibleMove

    def GetQueenPossibleMove(self, x, y):
        return self.GetBishopPossibleMove(x, y) + self.GetRookPossibleMove(x, y)

    def GetKingPossibleMove(self, x, y):
        possibleMove = []
        for direction in self.piecesDirections["K"]:
            posx, posy = x + direction[0], y + direction[1]
            if (0 <= posx <= 7 and 0 <= posy <= 7) and \
                    (self.board[posx][posy][0] != self.board[x][y][0] or self.board[posx][posy] == "00"):
                possibleMove.append((posx, posy))

        possibleMove.append((x, y + 2))
        possibleMove.append((x, y-2))
        return possibleMove

    def GetPossibleMove(self, x, y):
        square = self.board[x][y]
        try:
            if self.board[x][y][0] == self.Turn:
                return self.getPiecesPossibleMoves[square[1]](x, y)
        except KeyError:
            return []

    def IsValidMove(self, start, end):
        try:
            return end in self.GetPossibleMove(start[0], start[1])
        except TypeError:
            return False

    def Move(self, square1, square2, DISPLAYWINDOW, promotionSq=()):
        # params: square1: coordinate before move
        #         square2: coordinate after move

        if self.isPromotion:
            if 0 <= promotionSq[0] <= 3:
                select = self.SelectPromotion(promotionSq[0])
                if select != None:
                    select = self.board[square1[0]][square1[1]][0] + select
                    self.isPromotion = False
                    self.board[square1[0]][square1[1]] = "00"
                    self.board[square2[0]][square2[1]] = select
                    self.Turn = "w" if self.Turn == "b" else "b"
                    print("pro")
                    return True
            return False

        if self.IsValidMove(square1, square2):
            tmp = self.board[square1[0]][square1[1]]

            if (tmp[1] == "P") and (square2[0] == 7 or square2[0] == 0): ## Neu la tot va o hang cuoi cung thi tien hanh phong cap
                    self.DisplayPopUpPromotion(DISPLAYWINDOW, square2, tmp[0])
                    self.isPromotion = True
                    return False

            self.board[square1[0]][square1[1]] = "00"
            self.board[square2[0]][square2[1]] = tmp
            self.Turn = "w" if self.Turn == "b" else "b"
            return True
        return False

    def CastlingKingSide(self, square1, square2):


        posOfWhiteKing = self.positionT0Castling[0][0]
        posOfBlackKing = self.positionT0Castling[1][0]

        kingPos = posOfWhiteKing if square1 == posOfWhiteKing else posOfBlackKing

        if square2 == pg.Vector2(kingPos) + (0, 2):
            tmp = self.board[kingPos[0]][kingPos[1]]
            self.board[kingPos[0]][kingPos[1]] = "00"
            self.board[kingPos[0]][kingPos[1] + 2] = tmp
            self.board[kingPos[0]][kingPos[1] + 1] = "R"
            return True
        return False

    def IsKingChecked(self):
        # Kiem tra xem co bi ma ben dich chieu hay khong
        for direction in self.piecesDirections["N"]:
            pass

    def SquareIsUnderAttack(self):
        pass

    def CastlingQueenSide(self, square1, square2):
        posOfWhiteKing = self.positionT0Castling[0][0]
        posOfBlackKing = self.positionT0Castling[1][0]

        kingPos = posOfWhiteKing if square1 == posOfWhiteKing else posOfBlackKing

        if square2 == pg.Vector2(kingPos) - (0, 2):
            tmp = self.board[kingPos[0]][kingPos[1]]
            self.board[kingPos[0]][kingPos[1]] = "00"
            self.board[kingPos[0]][kingPos[1] - 2] = tmp
            self.board[kingPos[0]][kingPos[1] - 1] = "R"
            return True
        return False

    def CheckSignalSquareToCastling(self, square1, square2):
        posOfWhiteKing = self.positionT0Castling[0][0]
        posOfBlackKing = self.positionT0Castling[1][0]
        if square1 == posOfWhiteKing or square1 == posOfBlackKing: # Click into white kings or black kings
            if square2 == pg.Vector2(posOfWhiteKing) + (0, 2) \
                    or square2 == pg.Vector2(posOfWhiteKing) - (0, 2) \
                    or square2 == pg.Vector2(posOfBlackKing) - (0, 2) \
                    or square2 == pg.Vector2(posOfBlackKing) + (0, 2):
                    return True
                    # Check castling queenside or kingside for both black and white
        return False

    def Castling(self, square1, square2):
        if self.CheckSignalSquareToCastling(square1, square2):
            print("Enter here")
            return self.CastlingKingSide(square1, square2) or self.CastlingQueenSide()
