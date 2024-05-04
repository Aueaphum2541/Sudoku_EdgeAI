import cv2
import numpy as np
import math

def detect_squares(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(gray, (5, 5), 0)
    edges = cv2.Canny(blur, 50, 150)
    contours, _ = cv2.findContours(edges, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    squares = []
    for contour in contours:
        perimeter = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.02 * perimeter, True)
        
        if len(approx) == 4 and cv2.contourArea(contour) > 1000:
            squares.append(approx)
    
    return squares

def find_square_corners(squares):
    points = [] 
    points.append((squares[0][0][0][0],squares[0][0][0][1]))
    points.append((squares[0][1][0][0],squares[0][1][0][1]))
    points.append((squares[0][2][0][0],squares[0][2][0][1]))
    points.append((squares[0][3][0][0],squares[0][3][0][1]))

    # Calculate center
    center_x = sum(point[0] for point in points) / len(points)
    center_y = sum(point[1] for point in points) / len(points)
    
    dl = dr = ul = ur = (0,0)
    # Determine corner for each point
    for point in points:
        if point[0] > center_x:
            if point[1] > center_y:
                ur = point
                #print("ur")
            else:
                dr = point
                #print("dr")
        else:
            if point[1] > center_y:
                ul = point
                #print("ul")
            else:
                dl = point
                #print("dl")
                
    return dl,dr,ul,ur

#find_square_corners(squares)


def FindGrid(dl,dr,ul,ur):
    Urow = []
    Drow = []
    for i in range(10):
        Urow.append( ( int( (1-(i/9)) * ul[0] + (i/9) * ur[0] ) , int( (1-(i/9)) * ul[1] + (i/9) * ur[1] ) )  )
        Drow.append( ( int( (1-(i/9)) * dl[0] + (i/9) * dr[0] ) , int( (1-(i/9)) * dl[1] + (i/9) * dr[1] ) )  )
        
    #print(Urow)
    #print(Drow)

    GridPoints = []
    
    
    for j in range(10):
        col = []
        for i in range(10):
            col.append( ( int( (1-(i/9)) * Drow[j][0] + (i/9) * Urow[j][0] ) , int( (1-(i/9)) * Drow[j][1] + (i/9) * Urow[j][1] ) )  )
        #print(col)
        GridPoints.append(col)
        
    #print(GridPoints)
    return GridPoints

#FindGrid((400,400),(100,400),(100,100),(400,100))

def solve_sudoku(board):
    # Find empty position, if none, puzzle is solved
    empty_pos = find_empty_position(board)
    if not empty_pos:
        return True  # Puzzle solved

    row, col = empty_pos

    # Try placing numbers from 1 to 9
    for num in range(1, 10):
        if is_valid(board, row, col, num):
            board[row][col] = num

            # Recursively try to solve the puzzle
            if solve_sudoku(board):
                return True  # If successful, return True

            # If not successful, backtrack
            board[row][col] = 0

    return False  # Puzzle cannot be solved

def is_valid(board, row, col, num):
    # Check if the number is already in the current row
    if num in board[row]:
        return False

    # Check if the number is already in the current column
    for i in range(9):
        if board[i][col] == num:
            return False

    # Check if the number is already in the current 3x3 grid
    start_row, start_col = 3 * (row // 3), 3 * (col // 3)
    for i in range(3):
        for j in range(3):
            if board[i + start_row][j + start_col] == num:
                return False

    return True


def find_empty_position(board):
    for i in range(9):
        for j in range(9):
            if board[i][j] == 0:
                return (i, j)
    return None

# for Debugging
def print_board(board):
    for i in range(9):
        if i % 3 == 0 and i != 0:
            print("-" * 21)  # Separate the board into 3x3 blocks
        for j in range(9):
            if j % 3 == 0 and j != 0:
                print("|", end=" ")  # Separate each row into 3x3 blocks
            print(board[i][j], end=" ")
        print()  # Move to the next line after printing each row

def GetBoard(Imgs):
    UnSolved = [
        [7,9,0, 0,2,0, 3,8,0],
        [0,0,4, 0,0,0, 2,0,0],
        [5,0,0, 4,0,0, 0,1,0],
    
        [0,7,0, 3,0,0, 9,0,0],
        [3,5,0, 0,9,0, 7,0,0],
        [0,6,0, 0,0,0, 0,4,0],
 
        [0,0,0, 8,7,0, 0,0,0],
        [2,0,0, 1,0,0, 0,0,0],
        [0,0,1, 0,0,0, 0,9,0]
    ]
    sudoku_board = [[-1 if element > 0 else element for element in row] for row in UnSolved]
    
    if (solve_sudoku(UnSolved)):
        sudoku_board = [[UnSolved[i][j] if sudoku_board[i][j] != -1 else -1 for j in range(len(UnSolved[i]))] for i in range(len(UnSolved))]

    else:
        return -1
    
    return sudoku_board
    


def DrawNums(GridPoints,Imgs):
    sudoku_board = GetBoard(Imgs)
    
    if (sudoku_board == -1):
        print("Yessss")
        cv2.putText(frame,"UnSolved",GridPoints[1][4],cv2.FONT_HERSHEY_COMPLEX,0.5,(255,255,255),0)
        return 0
    
    Middle = []
    for i in range(9):
        col = []
        for j in range(9):
            s = (int(((GridPoints[i][j][0]+GridPoints[i+1][j+1][0])/2)),int(((GridPoints[i][j][1]+GridPoints[i+1][j+1][1])/2)))
            col.append(s)
            if (sudoku_board[j][i] != -1):
                cv2.putText(frame,str(sudoku_board[j][i]),col[j],cv2.FONT_HERSHEY_COMPLEX,0.5,(255,0,0),0)
        Middle.append(col)
        
        
def SavingCells(GridPoints):
    imgs = []
    dd = 5
    for i in range(9):
        col =[]
        for j in range(9):
            cell = frame[GridPoints[i][j][1] + dd :GridPoints[i+1][j+1][1] - dd,GridPoints[i][j][0] + dd:GridPoints[i+1][j+1][0] - dd ]
            #print(cell,i,j)
            col.append(cell)
            cv2.imwrite('Cells/cell['+ str(j) + '][' + str(i) + '].jpg',cell)
        imgs.append(col)
            
    print("saved")
    return imgs

def BigEnough(dl,dr,ul,ur):
    x1, y1 = ul
    x2, y2 = dr
    x3, y3 = dl
    x4, y4 = ur
    distance = math.sqrt((x2 - x1)**2 + (y2 - y1)**2)
    W = math.sqrt((x2 - x3)**2 + (y2 - y3)**2)
    H = math.sqrt((x3 - x1)**2 + (y3 - y1)**2)
    return distance>100 and (-100 <= W-H <= 100)

cap = cv2.VideoCapture(0)
Color = (255,255,255)
while True:
    ret, frame = cap.read()
    if not ret:
        break
    
    squares = detect_squares(frame)

    # Draw the contours
    if squares:  # Check if squares list is not empty
        
        cv2.drawContours(frame, squares, -1, (0, 255, 0), 3)
    
        
        
    
        dl,dr,ul,ur = find_square_corners(squares)
        GridPoints = FindGrid(dl,dr,ul,ur)
        
        for i in range(10):
            for j in range(10):
                cv2.circle(frame,GridPoints[i][j],2,(0,0,0))# Display the image
                
                
        cv2.circle(frame,(GridPoints[0][0][0],GridPoints[0][0][1]),10,(255,255,255))
        cv2.rectangle(frame,GridPoints[0][0],GridPoints[1][1],(255,0,0),2)
        #if(BigEnough(dl,dr,ul,ur)):
            #Imgs = SavingCells(GridPoints)
        Imgs = 0    
        DrawNums(GridPoints,Imgs)
    
    
    cv2.imshow('Squares Detection', frame)
    
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
