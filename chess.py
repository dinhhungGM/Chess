import pygame as pg
import os

class Chess:
    def __init__(self):
        self.sizeOfSquare = 100
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["00", "00", "00", "00", "00", "00", "00", "00"],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]

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
        if self.board[x - 1][y] == "00":
            possibleMove.append((x - 1, y))
        if x == 6 and self.board[x - 2][y] == "00": # Nam o hang ban dau chua di chuyen
            possibleMove.append((x - 2, y))
        return possibleMove

    def GetPossibleMove(self, x, y):
        square = self.board[x][y]
        if square[1] == "P":
            return self.GetPawnPossibleMove(x, y)
        return []

    def IsValidMove(self, start, end):
        if end in self.GetPossibleMove(start[0], start[1]):
            return True
        return False

    def Move(self, square1, square2):
        # params: square1: coordinate before move
        #         square2: coordinate after move
        if self.IsValidMove(square1, square2):
            tmp = self.board[square1[0]][square1[1]]
            self.board[square1[0]][square1[1]] = "00"
            self.board[square2[0]][square2[1]] = tmp
            return True
        return False