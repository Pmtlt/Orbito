# Création d'une liste de listes 4x4 remplie de zéros


def init_game() :
    L = [[0 for _ in range(4)] for _ in range(4)]
    return L


def print_board_term(board) : 
    L = board.copy()
    a = "+"
    b = "-"
    c = "|"
    col = "     0   1   2   3  "
    for d in range(4) : 
        for q in range(4):
            if L[d][q] == 0 : L[d][q] = "   "
            elif L[d][q] == 1 : L[d][q] =" W "
            elif L[d][q] == 2 : L[d][q] =" B "
    print(col)
    print ("   " + (a+b*3)*4 + a)
    y=0
    while y<4 :
        z = str(y)
        print (z + "  ", end="")
        for i in range(4):
            print(c + str(L[y][i]),end="")
        print(c)
        print ("   " + (a+b*3)*4 + a, end="\n")
        y = y + 1
    for d in range(4) : 
            for q in range(4):
                if L[d][q] == 0 : L[d][q] = "   "
                elif L[d][q] == 1 : L[d][q] =" W "
                elif L[d][q] == 2 : L[d][q] =" B "
print_board_term(init_game())

# Quels sont les mouvements possibles

def available_moves(board):
    mon_set = set()

    for row in range(0,len(board)):
        for col in range(0,len(board)):
            if board[row][col] == 0:
                mon_set.add((row,col))
            else:pass
    return sorted(mon_set)
available_moves(init_game())

# Est-ce que le mouvement est valide 
def is_valid_move(color, pose_row, pose_col, board):
    if color=="WHITE" and board[pose_row][pose_col]==0:
        if (pose_row, pose_col) in available_moves(board):
            return True
        else: 
            return False
    if color=="BLACK" and board[pose_row][pose_col]==0:
        if (pose_row, pose_col) in available_moves(board):
            return True
        else:
            return False
    else:
        return False
is_valid_move("WHITE",0,0,init_game())
is_valid_move("BLACK",0,0,init_game())
is_valid_move("RED",0,0,init_game())


import re
def ask_player(color,board):
    error = 1
    while error==1 : 
        error = 0
        mouv=input(f"C'est au tour de {color} de jouer, donnez les coordonnées de départ et d'arrivé :\n")
        regex = "[A-Za-z]"
        x = re.search(regex, mouv)
        if x != None :
            print("ERREUR : Vous devez écrire 2 entiers séparés par des espaces")
            error = 1     
        else :
            mouv = mouv.split()
            for j in range(len(mouv)) :
                mouv[j] = int(mouv[j])
            if len(mouv) != 2:
                print("ERREUR : Vous devez écrire 2 entiers séparés par des espaces")
                error = 1
            else : 
                for chiffres in range(len(mouv)) :
                    if mouv[chiffres] < 0 or mouv[chiffres] > 3 :
                        print("ERREUR : Les coordonnées doivent être sur le plateau")
                        error = 1
                        break
                if error == 0 :
                    if is_valid_move(color, mouv[0], mouv[1], board)==False :
                        print("ERREUR : Le mouvement doit être possible")
                        error = 1
    return(tuple(mouv))
ask_player("WHITE",init_game())

# Mouvement effectué

def move(color , pose_row , pose_col, board):
    if not is_valid_move(color, pose_row, pose_col, board):
        raise ValueError()
    else:
        if color=="WHITE":
            board[pose_row][pose_col] = 1
        elif color=="BLACK":
            board[pose_row][pose_col] = 2 
    return board

def is_oponent_ball(color,board,pose_row,pose_col):
    if color == "WHITE" and board[pose_row][pose_col]==1:
        print("ERREUR : C'est une de vos billes !")
        return False
    elif color == "BLACK" and board[pose_row][pose_col]==2:
        print("ERREUR : C'est une de vos billes !")
        return False
    elif board[pose_row][pose_col]==0:
        print("ERREUR : C'est une case vide !")
        return False
    else:
        print("C'est une bille de l'adversaire") 
        return True
is_oponent_ball("BLACK",[[2, 0, 0, 0], [1, 1, 0, 1], [0, 1, 2, 0], [2, 2, 0, 0]],0,0)


def ask_move_opponent_ball(color,board):
    error = 1
    while error==1 : 
        error = 0
        ask=input(f"Joueur {color} voulez vous bouger une bille adverse ? :\n")
        if re.search(r'Oui',ask,re.IGNORECASE):
            mouv=input(f"Donnez les coordonnées de la bille à bouger :\n")
            coord = re.search(r'[A-Za-z]', mouv)
            if coord != None :
                print("ERREUR : Vous devez écrire 2 entiers séparés par des espaces")
                error = 1 
            else :
                if is_oponent_ball:
                    pass
                else:
                    
                
        elif re.search(r'Non',ask,re.IGNORECASE):
            pass
        else :
            print("ERREUR : Veuillez répondre par 'Oui' ou par 'Non'")
    return(tuple(mouv))
ask_move_opponent_ball("WHITE",)

def push_button(board):
    new_board = [[0 for _ in range(4)] for _ in range(4)]
    col_minus_one = [(0,3),(0,1),(0,2),(1,2)]
    col_plus_one = [(3,0),(3,1),(3,2),(2,1)]
    row_minus_one = [(3,3),(2,3),(1,3),(2,2)]
    row_plus_one = [(0,0),(1,0),(2,0),(1,1)]
    for row in range(0,len(new_board)):
        for col in range(0,len(new_board)):
            if (row,col) in col_minus_one :
                new_board[row][col-1] = board[row][col]
            elif (row,col) in col_plus_one :
                new_board[row][col+1] = board[row][col]
            elif (row,col) in row_plus_one :
                new_board[row+1][col] = board[row][col]
            elif (row,col) in row_minus_one :
                new_board[row-1][col] = board[row][col]
    board = new_board
    return board
push_button([[1,2,0,0],[0,1,1,0],[2,2,0,1],[2,0,0,0]])