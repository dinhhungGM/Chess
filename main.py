import pygame as pg
from chess import Chess

pg.init()
WIDTH, HEIGHT = 800, 800
DISPLAYWINDOW = pg.display.set_mode((WIDTH, HEIGHT))
ChessObj = Chess()


def get_square_under_mouse():
    mouse_pos = pg.mouse.get_pos()
    x, y = (pos // ChessObj.sizeOfSquare for pos in mouse_pos)
    return (x, y)

def GameLoop():
    sqSelected = ()
    playerClicks = []
    clock = pg.time.Clock()
    displayPossibleMove = []

    while 1:

        ChessObj.Display(DISPLAYWINDOW)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                quit()
            if event.type == pg.MOUSEBUTTONDOWN:

                y, x = get_square_under_mouse()

                if sqSelected == (x, y):
                    sqSelected = ()
                    playerClicks = []
                else:
                    sqSelected = (x, y)
                    playerClicks.append(sqSelected)


                possbileMoves = ChessObj.GetPossibleMove(x, y)
                try:
                    displayPossibleMove = [pos for pos in possbileMoves]
                except TypeError:
                    displayPossibleMove = []

        # Draw Possible move
        for pos in displayPossibleMove:
            pg.draw.circle(DISPLAYWINDOW, (255, 0, 0), ((pos[1] + .5) * ChessObj.sizeOfSquare,
                                                        (pos[0] + .5) * ChessObj.sizeOfSquare), 10)

        if len(playerClicks) >= 2:
            if ChessObj.Move(playerClicks[len(playerClicks) - 2], playerClicks[len(playerClicks) - 1], DISPLAYWINDOW):
                playerClicks = []
                sqSelected = ()
            if ChessObj.isPromotion:
                if ChessObj.Move(playerClicks[len(playerClicks) - 2], playerClicks[len(playerClicks) - 1], DISPLAYWINDOW, sqSelected):
                    playerClicks = []
                    sqSelected = ()


        # Draw Bound Red Square
        x, y = get_square_under_mouse()
        pg.draw.rect(DISPLAYWINDOW, (255, 0, 0), (x * ChessObj.sizeOfSquare,
                                                  y * ChessObj.sizeOfSquare,
                                                  ChessObj.sizeOfSquare,
                                                  ChessObj.sizeOfSquare), 6)
        clock.tick(60)
        pg.display.flip()


if __name__ == '__main__':
    GameLoop()