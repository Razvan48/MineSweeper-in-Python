import pygame
import random

pygame.init()

screenWidth = 768
screenHeight = 1024
backGroundColor1 = (0, 0, 128)
backGroundColor2 = (0, 0,   0)

screen = pygame.display.set_mode((screenWidth, screenHeight))

pygame.display.set_caption("MineSweeper")
icon = pygame.image.load("Assets/Sprites/bomb.png")
pygame.display.set_icon(icon)

running = True
canClickOnSquares = True
wonGame = False

boardStartY = screenHeight * 0.25
margin = screenWidth * 0.05

epsilonBoardWidth = margin * 0.7
epsilonBoardHeight = margin * 0.7

numSquaresOnRow = 20
numSquaresOnColumn = 20

rectWidth = (screenWidth - 2 * margin) / numSquaresOnRow
rectHeight = (screenHeight - boardStartY - margin) / numSquaresOnColumn

epsilonSquareWidth = rectWidth * 0.07
epsilonSquareHeight = rectHeight * 0.07

buttonWidth = screenWidth * 0.1
buttonHeight = screenHeight * 0.05

bombSprite = pygame.image.load("Assets/Sprites/bomb.png")
bombSprite = pygame.transform.scale(bombSprite, (rectWidth - 2 * epsilonSquareWidth, rectHeight - 2 * epsilonSquareHeight))
flagSprite = pygame.image.load("Assets/Sprites/flag.png")
flagSprite = pygame.transform.scale(flagSprite, (rectWidth - 2 * epsilonSquareWidth, rectHeight - 2 * epsilonSquareHeight))
quitButton = pygame.image.load("Assets/Buttons/quitButton.png")
quitButton = pygame.transform.scale(quitButton, (buttonWidth, buttonHeight))
backButton = pygame.image.load("Assets/Buttons/backButton.png")
backButton = pygame.transform.scale(backButton, (buttonWidth, buttonHeight))
resetButton = pygame.image.load("Assets/Buttons/resetButton.png")
resetButton = pygame.transform.scale(resetButton, (buttonWidth, buttonHeight))

font20 = pygame.font.Font("freesansbold.ttf", 20)
font50 = pygame.font.Font("freesansbold.ttf", 50)

digitText = [font20.render(str(x), True, (0, 255, 255)) for x in range(9)]
digitTextRect = [digitText[x].get_rect() for x in range(9)]

buttonMarginY = buttonHeight * 0.25

quitButtonPos = (margin - epsilonBoardWidth, margin - epsilonBoardHeight + 2 * buttonHeight + 2 * buttonMarginY, buttonWidth, buttonHeight)
backButtonPos = (margin - epsilonBoardWidth, margin - epsilonBoardHeight, buttonWidth, buttonHeight)
resetButtonPos = (margin - epsilonBoardWidth, margin - epsilonBoardHeight + buttonHeight + buttonMarginY, buttonWidth, buttonHeight)

numOfBombs = 60
numOfFlags = numOfBombs

dx = [1, -1, 0,  0, 1, -1,  1, -1]
dy = [0,  0, 1, -1, 1, -1, -1,  1]

waitingTime = 100

visibleSquare = [[False for y in range(numSquaresOnRow)] for x in range(numSquaresOnColumn)]
bombSquare = [[False for y in range(numSquaresOnRow)] for x in range(numSquaresOnColumn)]
numOfBombsAround = [[0 for y in range(numSquaresOnRow)] for x in range(numSquaresOnColumn)]
flagOnSquare = [[False for y in range(numSquaresOnRow)] for x in range(numSquaresOnColumn)]


def initialize():
    global numOfFlags
    global canClickOnSquares
    global wonGame

    for x in range(numSquaresOnRow):
        for y in range(numSquaresOnColumn):
            visibleSquare[x][y] = False
            bombSquare[x][y] = False
            numOfBombsAround[x][y] = 0
            flagOnSquare[x][y] = False

    for i in range(numOfBombs):
        x = random.randint(0, numSquaresOnRow - 1)
        y = random.randint(0, numSquaresOnColumn - 1)
        while bombSquare[x][y]:
            x = random.randint(0, numSquaresOnRow - 1)
            y = random.randint(0, numSquaresOnColumn - 1)
        bombSquare[x][y] = True

    for x in range(numSquaresOnRow):
        for y in range(numSquaresOnColumn):
            if not bombSquare[x][y]:
                for i in range(len(dx)):
                    x2 = x + dx[i]
                    y2 = y + dy[i]
                    if x2 >= 0 and y2 >= 0 and x2 < numSquaresOnRow and y2 < numSquaresOnColumn and bombSquare[x2][y2]:
                        numOfBombsAround[x][y] += 1

    numOfFlags = numOfBombs
    canClickOnSquares = True
    wonGame = False

def fillCells(x, y):

    global numOfFlags

    visibleSquare[x][y] = True
    if flagOnSquare[x][y]:
        flagOnSquare[x][y] = False
        numOfFlags += 1
    if not numOfBombsAround[x][y]:
        for i in range(len(dx)):
            x2 = x + dx[i]
            y2 = y + dy[i]
            if x2 >= 0 and y2 >= 0 and x2 < numSquaresOnRow and y2 < numSquaresOnColumn and not visibleSquare[x2][y2]:
                fillCells(x2, y2)


def inBoard(x, y):
    return x > margin and x < screenWidth - margin and y > boardStartY


initialize()

while running:
    screen.fill(backGroundColor1)
    pygame.draw.rect(screen, backGroundColor2, pygame.Rect(margin - epsilonBoardWidth, boardStartY - epsilonBoardHeight, screenWidth - 2 * margin + 2 * epsilonBoardWidth, screenHeight - boardStartY - margin + 2 * epsilonBoardHeight))

    screen.blit(quitButton, quitButtonPos)
    screen.blit(backButton, backButtonPos)
    screen.blit(resetButton, resetButtonPos)

    #
    text = font20.render(str("Number of remaining flags: " + str(numOfFlags)), True, (255, 255, 255))
    textRect = text.get_rect()
    textRect.center = (3 * screenWidth / 4, screenHeight / 20)
    screen.blit(text, textRect)
    #

    for x in range(numSquaresOnRow):
        for y in range(numSquaresOnColumn):
            if not visibleSquare[x][y]:
                pygame.draw.rect(screen, (128, 128, 128), pygame.Rect(margin + x * rectWidth + epsilonSquareWidth, boardStartY + y * rectHeight + epsilonSquareHeight, rectWidth - 2 * epsilonSquareWidth, rectHeight - 2 * epsilonSquareHeight))
                if flagOnSquare[x][y]:
                    screen.blit(flagSprite, (margin + x * rectWidth + epsilonSquareWidth, boardStartY + y * rectHeight + epsilonSquareHeight))
            else:
                if bombSquare[x][y]:
                     screen.blit(bombSprite, (margin + x * rectWidth + epsilonSquareWidth, boardStartY + y * rectHeight + epsilonSquareHeight))
                else:
                    pygame.draw.rect(screen, (0, 128, 0), pygame.Rect(margin + x * rectWidth + epsilonSquareWidth, boardStartY + y * rectHeight + epsilonSquareHeight, rectWidth - 2 * epsilonSquareWidth, rectHeight - 2 * epsilonSquareHeight))
                    if numOfBombsAround[x][y] != 0:
                        digitTextRect[numOfBombsAround[x][y]].center = (margin + x * rectWidth + rectWidth / 2, boardStartY + y * rectHeight + rectHeight / 2)
                        screen.blit(digitText[numOfBombsAround[x][y]], digitTextRect[numOfBombsAround[x][y]])


    if not wonGame:
        if canClickOnSquares:
            if pygame.mouse.get_pressed()[0]:
                x = int(pygame.mouse.get_pos()[0])
                y = int(pygame.mouse.get_pos()[1])
                if inBoard(x, y):
                    x = int((x - margin) / rectWidth)
                    y = int((y - boardStartY) / rectHeight)
                    if not bombSquare[x][y]:
                        if not visibleSquare[x][y] and not flagOnSquare[x][y]:
                            fillCells(x, y)
                    elif not flagOnSquare[x][y]:
                        canClickOnSquares = False
                        for x in range(numSquaresOnRow):
                            for y in range(numSquaresOnColumn):
                                if bombSquare[x][y] and not flagOnSquare[x][y]:
                                    visibleSquare[x][y] = True
            if pygame.mouse.get_pressed()[2]:
                x = int(pygame.mouse.get_pos()[0])
                y = int(pygame.mouse.get_pos()[1])
                if inBoard(x, y):
                    x = int((x - margin) / rectWidth)
                    y = int((y - boardStartY) / rectHeight)
                    if not visibleSquare[x][y]:
                        if flagOnSquare[x][y]:
                            flagOnSquare[x][y] = False
                            numOfFlags += 1
                        elif numOfFlags > 0:
                            flagOnSquare[x][y] = True
                            numOfFlags -= 1
                        pygame.time.wait(waitingTime)

    if pygame.mouse.get_pressed()[0]:
        x = int(pygame.mouse.get_pos()[0])
        y = int(pygame.mouse.get_pos()[1])
        if x > quitButtonPos[0] and x < quitButtonPos[0] + buttonWidth and y > quitButtonPos[1] and y < quitButtonPos[1] + buttonHeight:
            running = False
        if not wonGame and x > backButtonPos[0] and x < backButtonPos[0] + buttonWidth and y > backButtonPos[1] and y < backButtonPos[1] + buttonHeight:
            canClickOnSquares = True
            for x in range(numSquaresOnRow):
                for y in range(numSquaresOnColumn):
                    if bombSquare[x][y] and visibleSquare[x][y]:
                        visibleSquare[x][y] = False
        if x > resetButtonPos[0] and x < resetButtonPos[0] + buttonWidth and y > resetButtonPos[1] and y < resetButtonPos[1] + buttonHeight:
            initialize()
            pygame.time.wait(waitingTime)

        numOfVisibleSquares = 0
        for x in range(numSquaresOnRow):
            for y in range(numSquaresOnColumn):
                if visibleSquare[x][y]:
                    numOfVisibleSquares += 1

    if canClickOnSquares and numOfFlags == 0 and numOfVisibleSquares + numOfBombs == numSquaresOnRow * numSquaresOnColumn:
        wonGame = True

    if wonGame:
        text = font50.render("YOU WON!", True, (0, 255, 0))
        textRect = text.get_rect()
        textRect.center = (screenWidth / 2, screenHeight / 2)
        screen.blit(text, textRect)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    pygame.display.flip()

pygame.quit()
