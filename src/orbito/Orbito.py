def init_game() :
    """ Initialisation du plateau"""
    L = [[0 for _ in range(4)] for _ in range(4)]
    return L

def print_board_term(board) : 
    """ Affichage graphique du plateau """
    L = [row[:] for row in board]
    a = "+"
    b = "-"
    c = "|"
    col = "     0   1   2   3  "
    for d in range(4) : 
        for q in range(4):
            if L[d][q] == 0 : L[d][q] = "   "
            elif L[d][q] == 1 : L[d][q] =" B "
            elif L[d][q] == 2 : L[d][q] =" N "
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
                elif L[d][q] == 1 : L[d][q] =" B "
                elif L[d][q] == 2 : L[d][q] =" N "

def available_moves(board):
    """ Liste des mouvements possibles"""
    mon_set = set()
    for row in range(0,len(board)):
        for col in range(0,len(board)):
            if board[row][col] == 0:
                mon_set.add((row,col))
            else:pass
    return sorted(mon_set)

def is_valid_move(color, pose_row, pose_col, board):
    """ Détermine si le mouvement est possible ou non """
    if color=="Blanc" and board[pose_row][pose_col]==0:
        if (pose_row, pose_col) in available_moves(board):
            return True
        else: 
            return False
    if color=="Noir" and board[pose_row][pose_col]==0:
        if (pose_row, pose_col) in available_moves(board):
            return True
        else:
            return False
    else:
        return False

import re
def ask_player_mouv(color,board):
    """ Demande au joueur ou il veut poser la bille """
    error = 1
    while error==1 : 
        error = 0
        mouv=input(f"C'est au tour du joueur {color}, où voulez vous poser votre bille ? :\n")
        print("---"*25)
        regex = "[A-Za-z]"
        x = re.search(regex, mouv)
        if x != None :
            print("ERREUR : Vous devez écrire 2 entiers séparés par des espaces")
            print("---"*25)
            error = 1     
        else :
            mouv = mouv.split()
            for j in range(len(mouv)) :
                mouv[j] = int(mouv[j])
            if len(mouv) != 2:
                print("ERREUR : Vous devez écrire 2 entiers séparés par des espaces")
                print("---"*25)
                error = 1
            else : 
                for chiffres in range(len(mouv)) :
                    if mouv[chiffres] < 0 or mouv[chiffres] > 3 :
                        print("ERREUR : Ces coordonées sont en dehors du plateau !")
                        print("---"*25)
                        error = 1
                        break
                if error == 0 :
                    if is_valid_move(color, mouv[0], mouv[1], board)==False :
                        print("ERREUR : Le mouvement doit être possible")
                        print("---"*25)
                        error = 1
                    else:
                        return(tuple(mouv))

def move(color, board):
    """ effectue le mouvement de la bille """
    mouv = ask_player_mouv(color,board)
    if mouv:
        if mouv is None:
            raise ValueError()
        else:
            if color=="Blanc":
                board[mouv[0]][mouv[1]] = 1
            elif color=="Noir":
                board[mouv[0]][mouv[1]] = 2 
        return board

def is_oponent_ball(color,board,pose_row,pose_col):
    """ Vérifie que c'est une bille adverse """
    if color == "Blanc" and board[pose_row][pose_col]==1:
        print("---"*25)
        print("ERREUR : C'est une de vos billes !")
        print("---"*25)
        return False
    elif color == "Noir" and board[pose_row][pose_col]==2:
        print("---"*25)
        print("ERREUR : C'est une de vos billes !")
        print("---"*25)
        return False
    elif board[pose_row][pose_col]==0:
        print("---"*25)
        print("ERREUR : C'est une case vide !")
        print("---"*25)
        return False
    else:
        return True

def check_moves_oponent_ball(color, board, pose_row, pose_col):
    """ Vérifie quels déplacement sont possibles pour la bille adverse """
    mon_set = set()
    if 0 <= pose_col + 1 <= 3 and board[pose_row][pose_col + 1] == 0:
        mon_set.add((pose_row, pose_col + 1))
    if 0 <= pose_col - 1 <= 3 and board[pose_row][pose_col - 1] == 0:
        mon_set.add((pose_row, pose_col - 1))
    if 0 <= pose_row + 1 <= 3 and board[pose_row + 1][pose_col] == 0:
        mon_set.add((pose_row + 1, pose_col))
    if 0 <= pose_row - 1 <= 3 and board[pose_row - 1][pose_col] == 0:
        mon_set.add((pose_row - 1, pose_col))
    return mon_set

def is_valid_oponent_ball_move(color, pose_row, pose_col, ball_row, ball_col, board):
    """ Vérifie que le mouvement de la bille adverse est valide """
    if color == "Blanc" or color == "Noir":
        return (pose_row, pose_col) in check_moves_oponent_ball(color, board, ball_row, ball_col)
    else:
        return False

import re
def ask_move_oponent_ball(color, board):
    """ Demande le mouvement à effectuer sur la bille adverse """
    while True:
        ask = input(f"Joueur {color} voulez-vous bouger une bille adverse ? :\n")
        print("---"*25)
        if re.search(r'Oui', ask, re.IGNORECASE):
            coord = input("Quelle bille voulez vous bouger ? :\n")
            print("---"*25)
            regex = re.search(r'[A-Za-z]', coord)
            if regex is not None:
                print("ERREUR : Vous devez écrire 2 entiers séparés par des espaces")
                print("---"*25)
                continue
            coord = coord.split()
            coord = [int(x) for x in coord]
            if len(coord) != 2 or any(x < 0 or x > 3 for x in coord):
                print("ERREUR : Les coordonnées doivent être sur le plateau")
                print("---"*25)
                continue
            if not is_oponent_ball(color, board, coord[0], coord[1]):
                print("ERREUR : Aucune bille adverse à cet endroit")
                print("---"*25)
                continue
            mouv = input("Où est ce que vous voulez bouger cette bille adverse ? :\n")
            print("---"*25)
            mouv = mouv.split()
            mouv = [int(x) for x in mouv]
            if len(mouv) != 2 or any(x < 0 or x > 3 for x in mouv):
                print("ERREUR : Les coordonnées doivent être sur le plateau")
                print("---"*25)
                continue
            if not is_valid_oponent_ball_move(color, mouv[0], mouv[1], coord[0], coord[1], board):
                print("ERREUR : Le mouvement n'est pas possible")
                print("---"*25)
                continue
            return tuple(mouv), tuple(coord)
        elif re.search(r'Non', ask, re.IGNORECASE):
            return None
        else:
            print("ERREUR : Veuillez répondre par 'Oui' ou par 'Non'")
            print("---"*25)

def move_opponent_ball(color, board):
    """ Déplace la bille adverse """
    result = ask_move_oponent_ball(color, board)
    if result is not None:
        mouv, coord = result
        board[mouv[0]][mouv[1]] = board[coord[0]][coord[1]]
        board[coord[0]][coord[1]] = 0
    return board

def push_button(board):
    """ Fait orbiter les billes du plateau """
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

def all_colour_balls(color,board):
    """ Récupère la position de toutes les billes d'un couleur sur le plateau """
    if color=="Blanc":
        mon_set = set()
        for row in range(0,len(board)):
            for col in range(0,len(board)):
                if board[row][col]==1:
                    mon_set.add((row,col))
    if color=="Noir":
        mon_set = set()
        for row in range(0,len(board)):
            for col in range(0,len(board)):
                if board[row][col]==2:
                    mon_set.add((row,col))
    return mon_set

def is_winned(color, board):
    """ Vérifie si un joueur à gagné """
    all_winning_conditions = [[(0,0),(1,1),(2,2),(3,3)],
                              [(0,3),(1,2),(2,1),(3,0)],
                              [(0,0),(1,0),(2,0),(3,0)],
                              [(0,1),(1,1),(2,1),(3,1)],
                              [(0,2),(1,2),(2,2),(3,2)],
                              [(0,3),(1,3),(2,3),(3,3)],
                              [(0,0),(0,1),(0,2),(0,3)],
                              [(1,0),(1,1),(1,2),(1,3)],
                              [(2,0),(2,1),(2,2),(2,3)],
                              [(3,0),(3,1),(3,2),(3,3)]]
    all_balls = all_colour_balls(color, board)
    for condition in all_winning_conditions:
        count = 0
        for pos in condition:
            if pos in all_balls:
                count += 1
            else:
                break
        if count == 4:
            return True
    return False

import re
import time
def rules():
    """ Affichage des règles """
    rules = ["Règles du jeu :\n", 
             "Votre but sera d'aligner 4 billes de votre couleur que ce soit horizontalement, verticalement ou diagonalement\n",
             "Les blancs commencent en premier et pour savoir qui jouera les un lancement de dé sera fait,\ncelui qui a le plus grand chiffre joue les blancs\n",
             "Chaque tour se jour en trois étapes :\n",
             "Etape n°1 (Cette étape ne peut être faite qu'à partir du 2ème tour de chaque joueur !) :\n",
             "Vous pouvez choisir de déplacer une bille adverse :\n",
             "  - ce déplacement ne se fait que dans une case adjacente de la bille sauf en diagonale !\n",
             "Etape n°2 : Placez une de vos billes sur une case vide du plateau\n",
             "Attention, une fois cette bille placée, elle ne peut plus être déplacée sauf par votre adversaire !\n",
             "Etape n°3 : Actionnement du bouton, les billes orbitent !\n",
             "Après orbitage, si quatres billes sont alignées pour vous ou votre adversaire, la partie s'arrête et celui qui à aligné quatre billes gagne\n",
             "Sinon la partie continue !\n"]
    print("---"*25)
    ask = input("Voulez vous lire les règles du jeu ?\n")
    print("---"*25)
    if re.search(r'oui',ask,re.IGNORECASE):
        for elmt in rules:
            print(elmt)
            time.sleep(2)
        print("---"*25)
    elif re.search(r'non',ask,re.IGNORECASE):
        pass
    else:
        print("ERREUR : Veuillez répondre par oui ou pas non !")

import random
import time
def dice_throw():
    """ Lancé de dé """
    error = 1
    while error == 1:
        print("Lancé de dé pour le joueur un !\n")
        nombre_j_un = random.randrange(0,6,1)
        time.sleep(1)
        print(f"Joueur n°1 vous avez fait {nombre_j_un}\n")
        print("---"*25)
        time.sleep(1)
        print("Lancé de dé pour le joueur deux !\n")
        nombre_j_deux = random.randrange(0,6,1)
        time.sleep(1)
        print(f"Joueur n°2 vous avez fait {nombre_j_deux}\n")
        print("---"*25)
        if nombre_j_un > nombre_j_deux :
            time.sleep(1)
            print("Joueur n°1 vous serez les billes blanches !\n")
            error = 0
            break
        if nombre_j_deux > nombre_j_un :
            time.sleep(1)
            print("Joueur n°2 vous serez les billes blanches !\n")
            error = 0
            break
        else:
            time.sleep(1)
            print("Vous avez tiré le même nombre recommençons !\n")

import time
def game():
    """ Fonction de lancement d'une partie """
    # Enoncement des règles
    rules()
    # Détermination du joueur blanc
    dice_throw()
    print("---"*25)
    # Initialisation du plateau de jeu
    board = init_game() 
    color = ["Blanc", "Noir"]
    tour = 0
    win_white = 0
    win_black = 0
    # Boucle principale de la partie
    while win_white == 0 and win_black == 0:
        for i in range(len(color)):
            # Affichage du plateau
            print_board_term(board)
            print("---"*25)
            time.sleep(0.5)
            # Déplacement d'une bille adverse si tour > 2
            if tour < 2 :
                pass
            else :
                board = move_opponent_ball(color[i], board)
                time.sleep(0.5)
                # Affichage du plateau
                print_board_term(board)
                print("---"*25)
            # Placement d'une bille sur le plateau de jeu 
            board = move(color[i], board)
            time.sleep(0.5)
            # Affichage du plateau
            print_board_term(board)
            print("---"*25)
            time.sleep(0.5)
            # Orbitement des billes sur le plateau
            board = push_button(board)
            print("Actionnement du bouton !")
            print("---"*25)
            time.sleep(0.5)
            # Checking des condition de victorie
            for j in range(len(color)):
                if is_winned(color[j], board):
                    if color[j] == "Blanc":
                        win_white += 1
                    else:
                        win_black += 1
            # Match nul
            if win_white > 0 and win_black > 0:
                print("C'est un match nul ! Bravo aux deux joueurs.")
                print_board_term(board)
                break
            # Victoire blanche
            elif win_white > 0 and win_black <= 0:
                print("Bravo au joueur Blanc ! Vous avez aligné 4 billes !" )
                print_board_term(board)
                break
            # Victoire noire
            elif win_white <= 0 and win_black > 0:
                print("Bravo au joueur Noir ! Vous avez aligné 4 billes !" )
                print_board_term(board)
                break
            # Acune victoire
            elif win_white <= 0 and win_black <= 0:
                count = 0
                for row in range(len(board)):
                    for col in range(len(board)):
                        if board[row][col] == 0:
                            break
                        else:
                            count += 1
                # Plateau complet
                if count == 16 :
                    print("Toutes les cases sont remplies et personne n'a aligné 4 billes ! Aucun gagnant pour cette partie !")
                    exit()
                # Plateau non complet
                else:
                    tour += 1
game()