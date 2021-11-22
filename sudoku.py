def isValidPos( board ,x , y ) : 
    for i in range(9):
        if(i!=x and board[i][y]==board[x][y]):
            return False
        if(i!=y and board[x][i]==board[x][y]):
            return False
    gridRow = x//3
    gridCol = y//3
    for i in range(3):
        for j in range(3):
            X = gridRow*3
            Y = gridCol*3
            if(not(X==x and Y==y)):
                if(board[x][y] == board[X][Y]):
                    return False
    return True
def solver( board , x=0,y=0):

    if(x==9):
        return True
    if(y==9):
        return solver(board , x+1,0)
    if(board[x][y] != 0 ):
        return solver(board,x,y+1)
    for i in range(1,10):
        board[x][y] = i
        if(not isValidPos(board,x,y)):
            continue
        else: 
            if(not solver(board,x,y+1)):
                continue
            else:
                return True
    board[x][y] = 0 
    return False

def printBoard( board) : 
    print(type(board))
    for x in range(9) : 
        if(x%3==0 and x!=0):
            print("---------------------------") 
        for y in range(9): 
            if(y%3==0 and y!=0):
                print("|" , end = " ")
            print(board[x][y] , end =  " ")
            if(y!=8):
                print("|" , end="")
        print()
